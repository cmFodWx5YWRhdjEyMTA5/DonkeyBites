$connection_Machines = New-Object -TypeName System.Data.SqlClient.SqlConnection
$connection_Machines.ConnectionString = "Server=CI_Database_Slave_1;Database='database';trusted_connection=true;"   
Write-Host "Trying to connect to database"
$connection_Machines.Open(); 
$ErrorActionPreference = 'silentlycontinue'
Write-Host "SQL Connetion is" $connection_Machines.State
while ($connection_Machines.State -ne 'Open')
       {
        Write-Progress -Activity Updating -Status 'Progress->' -PercentComplete 90
        $connection_Machines.Open();
        Write-Host "SQL Connetion is" $connection_Machines.State 
        sleep -Seconds 10        
       }
