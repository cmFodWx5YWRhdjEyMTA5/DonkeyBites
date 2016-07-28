param (
    [Parameter(Mandatory=$true)][string]$DirectoryBase,
    [Parameter(Mandatory=$true)][string]$RawScriptsFile,
    [Parameter(Mandatory=$true)][string]$List_File,
    [Parameter(Mandatory=$true)][string]$new_temp_file
)

New-Item -ItemType Directory -Force -Path TEST

$DS_Errors = "TEST\DS_Errors.txt"

<#
clear
$DirectoryBase               = "D:\TFS\BRANCH\"
$RawScriptsFile              = "ChangedScriptsName.txt"
$List_File                   = "TEST\DS_New_List.txt"
$new_temp_file               = "TEST\DS_New_Temp.txt"
#>

Write-Host "======================================================="
Write-Host "DirectoryBase is  - " $DirectoryBase
Write-Host "RawScriptsFile is - " $RawScriptsFile
Write-Host "List_File is      - " $List_File
Write-Host "new_temp_file is  - " $new_temp_file
Write-Host "DS_Errors is      - " $DS_Errors
Write-Host "======================================================="

$thisScript = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
. ($thisScript + '.\Utils.ps1')

#$RegexDirectoryBase = $DirectoryBase.Replace("\","\\")
#$RegexDirectoryBase = $RegexDirectoryBase.Replace(":","\:")

Add-PSSnapin SqlServerCmdletSnapin100
Add-PSSnapin SqlServerProviderSnapin100

####################################################################################



$header = "FullName"
$file = Get-Content $RawScriptsFile  | ConvertFrom-Csv -Header $header  |
Where-Object { $_.FullName.Substring($_.FullName.Length -4,1) -like "." } |
select FullName,
    @{n='sortableColumn';e={[string]( "" )}} 

$file | ForEach-Object {
    $_.sortableColumn = $_.Fullname -replace $RegexDirectoryBase
    for($i=1; $i -le 3; $i++)
        {
            $CurrentFirstSlashtIndex = ($_.sortableColumn.IndexOf('\') ) + 1
            $RemainingChars = $_.sortableColumn.Length - $_.sortableColumn.IndexOf('\') -1
            $_.sortableColumn = $_.sortableColumn.Substring( $CurrentFirstSlashtIndex, $RemainingChars)
        }
    $_.sortableColumn = $_.sortableColumn -replace "\\","_"
} 

$file | Sort-Object sortableColumn | Out-File $List_File -Width 400

CleanListFile ($List_File)

$i = 0
$errorCounter = 0

$SEP = "=========================================================================================="  
$SEP | Out-File $DS_Errors

$file | Sort-Object sortableColumn | ForEach-Object {
    
    $i++
    $currentSqlScriptFile = $DirectoryBase + $_.Fullname
    $error.clear()

    #    Write-Host "=========================================================================================="
    #    Write-Host "Script #" $i " is > " $currentSqlScriptFile        

    try {
        Invoke-Sqlcmd -ServerInstance "CI_Database_Slave_1" -Database "Database" -InputFile $currentSqlScriptFile 2>&1 | Out-File $DS_Errors -Append
        
    } catch {
        $errorCounter++
        $MSG                  = "Error Number " + $errorCounter + " ForScript #" + $i + " is > " + $currentSqlScriptFile 
        $MSG                  | Out-File $DS_Errors -Append
        $error                | Out-File $DS_Errors -Append
        $SEP                  | Out-File $DS_Errors -Append
    }
       
    #Write-Host "=========================================================================================="
 } 
