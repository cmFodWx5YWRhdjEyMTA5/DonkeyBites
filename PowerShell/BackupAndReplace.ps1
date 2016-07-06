 param (
    [Parameter(Mandatory=$true)][string]$fileName,
    [Parameter(Mandatory=$true)][string]$source,
    [Parameter(Mandatory=$true)][string]$filePath,
    [Parameter(Mandatory=$true)][string]$backupFolder,
    [Parameter(Mandatory=$true)][string]$listFile,
    [Parameter(Mandatory=$true)][string]$temp
 )

Write-Host "======================================================="
Write-Host "fileName is - " $fileName
Write-Host "source is - " $source
Write-Host "filePath is - " $filePath
Write-Host "backupFolder is - " $backupFolder
Write-Host "listFile is - " $listFile
Write-Host "temp is - " $temp
Write-Host "======================================================="

#Get list of locations
Get-ChildItem -Recurse -Force $filePath -ErrorAction SilentlyContinue |
Where-Object { ($_.PSIsContainer -eq $false) -and  ( $_.Name -like "*$fileName*") } |
Select-Object Directory| Format-Table -AutoSize -hideTableHeaders * | Out-File $listFile -Width 400 -Verbose

#Remove first empty line
Get-Content $listFile | Select -Skip 1 | Set-Content $temp
Move "temp.tmp" $listFile -Force

#Trim the first line to remove spaces
$lines=(Get-Content $listFile) | foreach{ $_.Trim(" ")}  
$lines > $listFile

#Backup DLL
$firstLine = Get-Content $listFile | select -Index 1 
Copy-Item -Path $firstLine\$fileName -Destination $backupFolder -Recurse -Force

#Replace old DLL with new
$lines = Get-Content $listFile
foreach ($line in $lines) {
	Write-Host "=====================================" $source
	Write-Host "Source      - " $source
	Write-Host "Destination - " $line
	Write-Host "=====================================" $source
    if ($line) {Copy-Item -Path $source -Destination $line -Recurse -Force}
}
