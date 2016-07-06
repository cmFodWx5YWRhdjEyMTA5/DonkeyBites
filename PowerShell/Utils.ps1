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

    $internalPath = $item.Replace("$/aaa/CI/", "")
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

 Function FuncStartAllServices
{
    Get-Service | Where-Object {$_.ServiceName -notlike "EXAMPLE*" -and $_.ServiceName -like "EXAMPLE*"}|
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

Function FuncStopAllServices
{
	                           
    Get-Service | Where-Object {$_.ServiceName -notlike "EXAMPLE*" -and $_.ServiceName -like "EXAMPLE*"}|
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
