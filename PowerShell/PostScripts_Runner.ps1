param (
    [Parameter(Mandatory=$true)][string]$DirectoryBase_Post_scripts,
    [Parameter(Mandatory=$true)][string]$SortedFile_Post_Scripts
)

<#
clear

$DirectoryBase_Post_scripts = "D:\TFS\MCOngoing\_DBRelease\MajorUpgrade\Post-Installation\Applications\"
$SortedFile_Post_Scripts    = "workingFolder\NEW_POST_ScriptsList.txt"

Write-Host "======================================================="
Write-Host "DirectoryBase_Post_scripts is  - " $DirectoryBase_Post_scripts
Write-Host "SortedFile_Post_Scripts is     - " $SortedFile_Post_Scripts
Write-Host "======================================================="
#>
$thisScript = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
. ($thisScript + '.\Utils.ps1')

if (!(Test-Path POSTworkingFolder -PathType Container)) {New-Item -ItemType Directory -Force -Path POSTworkingFolder}
$Errors_Log = "POSTworkingFolder\Errors_Log.txt"

####################################################################################
## Create File with list of Scripts that we need to sort and run
####################################################################################

$file = Get-ChildItem $DirectoryBase_Post_scripts -Recurse |
Where-Object { $_.FullName.Substring($_.FullName.Length -4,1) -like "." } |
select FullName,
@{n='sortableColumn';e={[string]( "" )}} 


####################################################################################
## Manipulate the Script paths so it will be ready to be sorted on digit base
## and the sort it
####################################################################################

$sortedFile= (SortScripts $file $DirectoryBase_Post_scripts $SortedFile_Post_Scripts)

####################################################################################
## Clean the File so it will not have traling spaces for each line and also
## 8 empty charactes at the end
####################################################################################

CleanListFile ($SortedFile_Post_Scripts) 

####################################################################################
## Run the Scripts by order that was just created
####################################################################################

ScriptsRunner $DirectoryBase_Post_scripts $sortedFile $Errors_Log "true" 
