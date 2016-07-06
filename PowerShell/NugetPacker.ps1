 param (
    [Parameter(Mandatory=$true)][string]$workspace = "D:\TFS\",
    [Parameter(Mandatory=$true)][string]$changeSetId = "698616"
 )


$thisScript = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
. ($thisScript + '.\Utils.ps1')

#################################
#####    ACTUAL CODE
#################################

add-pssnapin Microsoft.TeamFoundation.PowerShell
$srv = Get-TfsServer http://tfs_App:8080/tfs/Repo/
[string]::Format(">>> Quering TFS changeSet #{0} to get changed files",$changeSetId) | Write-Host
$cs = Get-TfsChangeset -ChangesetNumber $changeSetId -Server $srv

foreach ($item in $cs.Changes| ForEach-Object {$_.Item.ServerItem}){
  
    $itemLocation = $item.Item.ServerItem -replace $projectPath_regex, ""

    $itemObject = get_item_details($item)
    $currentSolution = $itemObject.solution
    $currentComponent = $itemObject.component

#    Write-Host "component  " $itemObject.component
#    Write-Host "solution   " $itemObject.solution

    if(-not (Test-Path -Path "$workspace\$env:BRANCH\$env:VERSION\$currentSolution\$currentComponent\artifacts")){ mkdir "$workspace\$env:BRANCH\$env:VERSION\$currentSolution\$currentComponent\artifacts"}
        Remove-Item "$workspace\$env:BRANCH\$env:VERSION\$currentSolution\$currentComponent\artifacts\*" -Recurse -Force

    $proj = get_csproj_folder([System.IO.Path]::GetDirectoryName($item.Replace("$/McKesson",$workspace)))
    
    Invoke-Expression "nuget pack $proj -OutputDirectory $workspace\$env:BRANCH\$env:VERSION\$currentSolution\$currentComponent\artifacts -Version $env:VERSION.$env:BUILD_NUMBER"
    Write-Host $proj
}
