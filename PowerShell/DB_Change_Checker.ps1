$thisScript = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
. ($thisScript + '.\Utils.ps1')sdf

$changeSetId = 701772
$cs = get_TFS_Changeset($changeSetId)
$answer = 'false'

foreach ($line in $cs.Changes) {
    $extn = [IO.Path]::GetExtension($line.Item.ServerItem)

    $fileTypes = @('SQL','UDF','PRC','TRG','TAB','FRK','DAT','MDF','LDF')

    foreach ($type in $fileTypes){
        if ($extn -match "$type$"){$answer = 'true'}
    }
}
Write-Host "###### $answer "  



