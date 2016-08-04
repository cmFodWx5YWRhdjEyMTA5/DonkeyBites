param (
    [Parameter(Mandatory=$true)][string]$DirectoryBase,
    [Parameter(Mandatory=$true)][string]$RawScriptsFile,
    [Parameter(Mandatory=$true)][string]$List_File,
    [Parameter(Mandatory=$true)][string]$new_temp_file
)

<#
clear

$DirectoryBase               = "D:\JenkinsTFS\MCOngoing\"
$RawScriptsFile              = "DBworkingFolder\ChangedScriptsName.txt"
$List_File                   = "DBworkingFolder\DS_New_List.txt"
$new_temp_file               = "DBworkingFolder\DS_New_Temp.txt"

Write-Host "======================================================="
Write-Host "DirectoryBase is      - " $DirectoryBase
Write-Host "RawScriptsFile is     - " $RawScriptsFile
Write-Host "List_File is          - " $List_File
Write-Host "new_temp_file is      - " $new_temp_file
Write-Host "======================================================="
#>

$thisScript = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
. ($thisScript + '.\Utils.ps1')

if (!(Test-Path DBworkingFolder -PathType Container)) {New-Item -ItemType Directory -Force -Path DBworkingFolder}
$Errors_Log = "DBworkingFolder\Errors_Log.txt"

####################################################################################
## Get data from Changedscripts File and Prepare it for sorting
####################################################################################

$header = "FullName"
$fileAA = Get-Content $RawScriptsFile  | ConvertFrom-Csv -Header $header  |
Where-Object { $_.FullName.Substring($_.FullName.Length -4,1) -like "." } |
select FullName,
    @{n='sortableColumn';e={[string]( "" )}} 

####################################################################################
## Manipulate the Script paths so it will be ready to be sorted on digit base
## and the sort it
####################################################################################

$sortedFile= (SortScripts $fileAA $DirectoryBase $List_File)

####################################################################################
## Clean the File so it will not have traling spaces for each line and also
## 8 empty charactes at the end
####################################################################################

CleanListFile ($List_File)

####################################################################################
## Run the Scripts by order that was just created
####################################################################################
#$sortedFile.GetType()
ScriptsRunner $DirectoryBase $sortedFile $Errors_Log "false"
