Function get_csproj_folder($path_x)
{
    $str= ""
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
    Return "$path_x\$str" 
}

Function get_item_details($item)
{
    #Create an Object
    [object] $itemDetails = @{} 

    #Write-Host "   "     
    #Write-Host "Item is             " $item

    $internalPath = $item.Replace("$/McKesson/CI/", "")
    #Write-Host "internalPath is     " $internalPath

    $solution = $internalPath.Substring(0,$internalPath.IndexOf("/"))
    #Write-Host "Solution is         " $solution
    
    $tempComponent = $internalPath.Replace("$solution/","")
    
    $last = $tempComponent.LastIndexOf("/")
    $component = $tempComponent.Substring(0,$last)

    #Write-Host "Component is        " $component    
       
    #Assign all return values in to an Object
    $itemDetails.solution = $solution 
    $itemDetails.component = $component 
    
    #Return the hashtable
	Return $itemDetails 
}

Function FuncStartService
{
	param($ServiceName)
	$arrService = Get-Service -Name $ServiceName
	if ($arrService.Status -ne "Running"){
	Start-Service $ServiceName
	Write-Host "Starting " $ServiceName " service" 
	" ---------------------- " 
	" Service is now started"
	}
	if ($arrService.Status -eq "running"){ 
	Write-Host "$ServiceName service is already started"
	}
 }

Function FuncStopService
 {
	param($ServiceName)
	$arrService = Get-Service -Name $ServiceName
	if ($arrService.Status -ne "Stopped"){
	Stop-Service $ServiceName
	Write-Host "Stopping " $ServiceName " service" 
	" ---------------------- " 
	" Service is now stopped"
	}
	if ($arrService.Status -eq "stopped"){ 
	Write-Host "$ServiceName service is already stopped"
	}
 }

 Function FuncStartAllMedconServices
{
    Get-Service | Where-Object {$_.ServiceName -notlike "Medcon*PHI*" -and $_.ServiceName -like "Medcon*"}|
    Foreach-Object {
	    if ($_.Status -ne "Running"){
	    Start-Service $_.ServiceName
	    Write-Host "Starting " $_.ServiceName " service" 
	    " ---------------------- " 
	    " Service is now started"
	    }
	    if ($_.Status -eq "running"){ 
	    Write-Host $_.ServiceName" service is already started"
	    }
    
    }
}

Function FuncStopAllMedconServices
{
	                           
    Get-Service | Where-Object {$_.ServiceName -notlike "Medcon*PHI*" -and $_.ServiceName -like "Medcon*"}|
    Foreach-Object {
	    if ($_.Status -ne "stopped"){
        Stop-Service $_.ServiceName
	    Write-Host "Stopping " $_.ServiceName " service" 
	    " ---------------------- " 
	    " Service is now stopped"
	    }
	    if ($_.Status -eq "stopped"){ 
	    Write-Host $_.ServiceName" service is already stopped"
	    }
    
    }
}

Function CleanListFile
{
	param (
    [Parameter(Mandatory=$true)][string]$File
    )
        $temp="temp.tmp" 
        
        if (!(Test-Path $temp )){ new-item -name $temp -type "file"}
    
        #Remove first empty line
        Get-Content $File| Select -Skip 1 | Set-Content $temp
        Move $temp $File -Force

        #Trim lines to remove spaces
        $lines=(Get-Content $File) | foreach{ $_.Trim(" ")}  
        $lines > $File

        #Remove last 8 blank characters
        $stream = [IO.File]::OpenWrite($File)
        $stream.Length -lt 8
        $stream.SetLength($stream.Length - 8)
        $stream.Close()
        $stream.Dispose()
 }

Function SortScripts
{
	param (
    [Parameter(Mandatory=$true)][array]$file_x,
    [Parameter(Mandatory=$true)][string]$DirectoryBase,
    [Parameter(Mandatory=$true)][string]$List_File
    )
 
    $RegexDirectoryBase = $DirectoryBase.Replace("\","\\")
    $RegexDirectoryBase = $RegexDirectoryBase.Replace(":","\:")

    $file_x | ForEach-Object {
        
        $_.sortableColumn = $_.Fullname -replace $RegexDirectoryBase

        while (!($_.sortableColumn -match "^[0-9].*"))
        {
            $CurrentFirstSlashtIndex = ($_.sortableColumn.IndexOf('\') ) + 1
            $RemainingChars = $_.sortableColumn.Length - $_.sortableColumn.IndexOf('\') -1
            $_.sortableColumn = $_.sortableColumn.Substring( $CurrentFirstSlashtIndex, $RemainingChars)
        }

        $_.sortableColumn = $_.sortableColumn -replace "\\","_"
    } 
    
    $file_x | Sort-Object sortableColumn | Out-File $List_File -Width 400

    Return $file_x 
}


Function ScriptsRunner
{
	param (
    [Parameter(Mandatory=$true)][string]$DirectoryBase,
    [Parameter(Mandatory=$true)][array]$file,
    [Parameter(Mandatory=$true)][string]$Errors_Log,
    [Parameter(Mandatory=$true)][string]$HasFullPath 

    )
        
    Add-PSSnapin SqlServerCmdletSnapin100
    Add-PSSnapin SqlServerProviderSnapin100
        
    $i = 0
    $errorCounter = 0

    $SEP = "=========================================================================================="  
    $SEP | Out-File $Errors_Log
    
    #Write-Host "-------------- RUNNER IS ON - Will Invoke SQL  --------------" 
    
    $file | ForEach-Object {
    
        $i++
        
        #Write-Host "1111 currentSqlScriptFile --- " $currentSqlScriptFile
        $currentFullName = $_.Fullname
        if ($HasFullPath -eq "true" ) {$currentSqlScriptFile = $_.Fullname} else {$currentSqlScriptFile = $DirectoryBase + $currentFullName}

        #Write-Host " ----- currentSqlScriptFile --- " $currentSqlScriptFile
        #Write-Host "3333 DirectoryBase        --- " $DirectoryBase
        #Write-Host "4444 _.Fullname           --- " $_.Fullname
        #Write-Host "5555 currentFullName      --- " $currentFullName

        $error.clear()

        #    Write-Host "=========================================================================================="
        #    Write-Host "Script #" $i " is > " $currentSqlScriptFile        

        try {
       #    Write-Host "-------------- Invoke SQL ---------------" 
            Invoke-Sqlcmd -ServerInstance "CI_Database_Slave_1" -Database "Medcon" -InputFile $currentSqlScriptFile 2>&1 | Out-File $Errors_Log -Append
        
        } catch {
       #    Write-Host "-------------- Catch Error --------------" 
            $errorCounter++
            $MSG                  = "Error Number " + $errorCounter + " ForScript #" + $i + " is > " + $currentSqlScriptFile 
       #    Write-Host "-------------- MSG is --------------- "  $MSG
            $MSG                  | Out-File $Errors_Log -Append
            $error                | Out-File $Errors_Log -Append
            $SEP                  | Out-File $Errors_Log -Append
        }
       
        #Write-Host "=========================================================================================="
     } 
}
