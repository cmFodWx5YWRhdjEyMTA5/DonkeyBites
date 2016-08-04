
$changeSetId =  698616 #697177
$base_file_path = "D:\TFS\MCOngoing\"
$projectPath_regex = "\$/McKesson/CI/"

clear

add-pssnapin Microsoft.TeamFoundation.PowerShell
$srv = Get-TfsServer http://tfs_App:8080/tfs/MedconCollection/
[string]::Format(">>> Quering TFS changeSet #{0} to get changed files",$changeSetId) | Write-Host
$cs = Get-TfsChangeset -ChangesetNumber $changeSetId -Server $srv

foreach ($item in $cs.Changes) {
    
    Write-Host "String Before : " $item.Item.ServerItem
    $itemLocation = $item.Item.ServerItem -replace $projectPath_regex, ""
    $full_item_path=$base_file_path + $itemLocation
    Write-Host "String After  : " $full_item_path

    #Write-Host $item.Item.ServerItem
    get_csproj_folder($full_item_path)
}

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
            $projectFiles = Get-ChildItem $path_x -filter *.csproj

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
