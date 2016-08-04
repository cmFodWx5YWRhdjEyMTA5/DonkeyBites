Function get_csproj_folder($path_x)
#-------------------------------------------------------------------------------------------------------------------
#  Get Path csproj Filename for a givven path
#-------------------------------------------------------------------------------------------------------------------
{
    $str= ""
    #Create an hashtable variable 
    [hashtable] $Details = @{} 

    while ($str -eq "" )
        {
            $projectFiles = Get-ChildItem $path_x -filter *.csproj -Recurse

            if ($projectFiles -ne $null)
                {
                    $str = $projectFiles.Name
                }
                else
                {
                    $path_x = [System.IO.Path]::GetDirectoryName($path_x)
                }
        } 
    #Assign all return values in to hashtable
    $Details.Name = $str 
    $Details.Path = $path_x 
    #Return the hashtable
    Return $Details 
}

Function get_TFS_Changeset($changeSetId)
#-------------------------------------------------------------------------------------------------------------------
#  Get ChangeSet from TFS
#-------------------------------------------------------------------------------------------------------------------
{
    add-pssnapin Microsoft.TeamFoundation.PowerShell
    $srv = Get-TfsServer http://tfs_App:8080/tfs/MedconCollection/
    [string]::Format(">>> Quering TFS changeSet #{0} to get changed files",$changeSetId) | Write-Host
    $cs = Get-TfsChangeset -ChangesetNumber $changeSetId -Server $srv
    Return $cs
}


Function get_CS_Components($cs,$currentBranch,$currentSolution)
#-------------------------------------------------------------------------------------------------------------------
#  Get component names included in the ChangeSet
#-------------------------------------------------------------------------------------------------------------------
{
    
    $Components = $cs | Select-Object -Expand "Changes" |
    Select-Object -Expand "Item" |
    Where-Object { $_.ContentLength -gt 0} |

    #    Where-Object { $_.ServerItem -notlike '*/sql/*' } |
    #    Where-Object { $_.ServerItem -notlike '*.publish.xml'} |

    Select -Unique ServerItem | Sort ServerItem |
    Format-Table -Property * -AutoSize

    #Out-String -Width 4096 |
    #Out-File FILE.txt #-append

    ###################################################################
    
    foreach ($comp in $Components ){   
    
    $tempPath = $comp.Replace("$/McKesson/$currentBranch/$currentSolution/", "")
    }
}
# Parametes for Jenkins  
#Param(
#    [string]$workspace=(Get-Item env:WORKSPACE).Value,
#    [string]$build=(Get-Item env:BUILD_NUMBER).Value,
#    [string]$projectPath=(Get-Item env:TFS_PROJECTPATH).Value,
#    [string]$changeSetId=(Get-Item env:TFS_CHANGESET).Value
#)

# Parameters for stanalone execution
#$file = "D:\TFS\MCOngoing\InterfaceServer\CustomMappingFiles\InterfaceServer.CustomMappingFiles.csproj"
#$projectPath="$/McKesson/MCOngoing/InterfaceServer/CustomMappingFiles"

# VARS to be givven
$repo_root =  "C:\Jenkins\workspace\DS_MJ_Build_Solution_InterfaceServer"
$currentSolution = "InterfaceServer" # Will be taken from jenkins job context
$currentBranch = "CI"
$solutionTFSPath="$/McKesson/MCOngoing/InterfaceServer/"
$build = 36
$changeSetId = 700062

# VARS to be calculated
$currentCompoenents = "" # will be calculated
$file = "C:\Jenkins\workspace\DS_MJ_Build_Solution_InterfaceServer\CI\InterfaceServer\CustomMappingFiles\InterfaceServer.CustomMappingFiles.csproj"
      
$path = Get-ChildItem $file

$workspace=$path.DirectoryName

[string]::Format(">>> INFO:`r`n>>>`t`tWORKSPACE:{0}`r`n>>>`t`tBUILD_NUMBER:{1}`r`n>>>`t`tPROJECT:{2}`r`n>>>`t`tCHANGESET:{3}",$workspace,$build,$projectPath,$changeSetId)

$excludes = "Services.csproj","Utilities.csproj","Tests.csproj"

$cs = get_TFS_Changeset($changeSetId)

get_CS_Components($cs,$currentBranch)

$UserName = $cs.CommitterDisplayName

#-------------------------------------------------------------------------------------------------------------------
#  Get the root folder of csproj files in order to create the artifact folder in it (only if is not there anlready)
#-------------------------------------------------------------------------------------------------------------------
$csprojDetails = get_csproj_folder($workspace)
$root_folder=$csprojDetails.Path

if(-not (Test-Path -Path "$root_folder\artifacts")){
    mkdir "$root_folder\artifacts"
    } else {Remove-Item "$root_folder\artifacts\*" -Recurse -Force
    }
    
foreach ($folder in $cs.Changes| get_csproj_folder($workspace) | Get-Unique){
    $dir = [string]::Format("{0}",$folder.Path)

    if(!((get-Item $dir) -is [System.IO.DirectoryInfo])){continue}
    $tmp = $excludes | where{$_.Split(".")[0] -eq $folder.path} 

    if($tmp -And $tmp.Length -gt 0) {
        [string]::Format(">>> Change #{0}: change was made to {1} which is marked as 'ignored' when packaging",$changeSetId,$tmp)
        continue
    }

    #-------------------------------------------------------------------------------------------------------------------
    #  When the changes are in real projects, the spec generation will apply
    #-------------------------------------------------------------------------------------------------------------------

    [string]::Format(">>> Changes were made to {0}, packing relevant project",$dir) | Write-Host
    
    Write-host ">>> Creating Nuget spec"
    cd $dir
    Invoke-Expression "nuget spec -Force"
    $specFile = get-childitem $dir -recurse | where {$_.extension -eq ".nuspec"} | Select-Object -index 0
    
    #-------------------------------------------------------------------------------------------------------------------
    #  Remove unessecery entires in the generated Spec file 
    #-------------------------------------------------------------------------------------------------------------------
    Write-host ">>> Editing spec before packaging"
    $spec = [xml](Get-Content $specFile.FullName)
    foreach($r in "licenseUrl","iconUrl","projectUrl","tags","releaseNotes"){
        $spec.package.metadata.ChildNodes | ? { $r -eq $_.Name  } | % {$spec.package.metadata.RemoveChild($_)}
    }

    #-------------------------------------------------------------------------------------------------------------------
    #  Populating XML with relevant data
    #-------------------------------------------------------------------------------------------------------------------
    $spec.SelectSingleNode("//id").InnerText = [string]::Format("MC_{0}",$specFile.Name.Split(".")[0])
    $spec.SelectSingleNode("//version").InnerText = [string]::Format("1.0.0.{0}",$build)
    $spec.SelectSingleNode("//authors").InnerText = $UserName
    $spec.SelectSingleNode("//owners").InnerText = $UserName
    $spec.SelectSingleNode("//title").InnerText = "Automation "+ $specFile.Name.Split(".")[0]
    $spec.SelectSingleNode("//authors").InnerText = $UserName
    $spec.SelectSingleNode("//description").InnerText = "McKesson IWS "+ $specFile.Name.Split(".")[0]
    
    #-------------------------------------------------------------------------------------------------------------------
    #  Save the spec file
    #-------------------------------------------------------------------------------------------------------------------
    $spec.Save($specFile.FullName)
    Write-host ">>> Packaging artifact to $workspace\artifacts directory"

    #-------------------------------------------------------------------------------------------------------------------
    #  Perform packing using created spec
    #-------------------------------------------------------------------------------------------------------------------
    [string]::Format("nuget pack {0} -IncludeReferencedProjects -OutputDirectory {1}\artifacts",$folder.Name,$folder.Path) | Invoke-Expression 
}

Write-host ">>> D-O-N-E <<<" 
