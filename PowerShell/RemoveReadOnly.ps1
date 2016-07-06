 param (
    [Parameter(Mandatory=$true)][string]$solutionFolder,
    [Parameter(Mandatory=$true)][string]$listFileName,
    [Parameter(Mandatory=$true)][string]$fileToChange,
    [Parameter(Mandatory=$true)][string]$temp
 )

Write-Host "======================================================="
Write-Host "solutionFolder is - " $solutionFolder
Write-Host "listFileName is   - " $listFileName
Write-Host "fileToChange is   - " $fileToChange
Write-Host "temp is           - " $temp
Write-Host "======================================================="

#$solutionFolder="C:\temp\DS_MJ_Build_Solution_Common\CI\Common"
#$listFileName="FilesList.txt"
#$temp="temp.tmp"
#$fileToChange="packages.config"

Get-ChildItem -Path $solutionFolder -Recurse -ErrorAction SilentlyContinue -Include $fileToChange |
Select-Object FullName| Format-Table -AutoSize -hideTableHeaders * | Out-File $solutionFolder\$listFileName -Width 400

#Remove first empty line
Get-Content $solutionFolder\$listFileName | Select -Skip 1 | Set-Content $temp
Move $temp $solutionFolder\$listFileName -Force

#Trim lines to remove spaces
$lines=(Get-Content $solutionFolder\$listFileName) | foreach{ $_.Trim(" ")}  
$lines > $solutionFolder\$listFileName


#Go over the list of files and remove ReadOnly
$files = Get-Content $solutionFolder\$listFileName
foreach ($file in $files)
{
    If ($file.Length -gt 0 )
    {
        Write-Host "=====================================" 
    	Write-Host "Remove read-Only from file - " $file
        Set-ItemProperty $file -name IsReadOnly -value $false
        Write-Host "====================================="         
    }
    
}

