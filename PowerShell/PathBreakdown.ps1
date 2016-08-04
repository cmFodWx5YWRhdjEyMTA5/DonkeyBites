$workspace = "D:\TFS\McKesson\CI\"
$changeSetId = 698616   

$thisScript = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
. ($thisScript + '.\Utils.ps1')

add-pssnapin Microsoft.TeamFoundation.PowerShell
$srv = Get-TfsServer http://tfs_App:8080/tfs/MedconCollection/
[string]::Format(">>> Quering TFS changeSet #{0} to get changed files",$changeSetId) | Write-Host
$cs = Get-TfsChangeset -ChangesetNumber $changeSetId -Server $srv

if(-not (Test-Path -Path "$workspace\artifacts")){ mkdir "$workspace\artifacts"}
Remove-Item "$workspace\artifacts\*" -Recurse -Force

foreach ($item in $cs.Changes| ForEach-Object {$_.Item.ServerItem}){
   get_item_details($item) 
}
