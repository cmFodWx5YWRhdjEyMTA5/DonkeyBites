String file = 'c:\\JENKINS\\jobs\\FB_00_Feature_Branch_On_Request\\workspace\\node.properties'
Properties props = new Properties()
boolean fileSuccessfullyDeleted =  new File(file).delete()
boolean fileSuccessfullyCreated =  new File(file).createNewFile()
File propsFile = new File(file)
props.load(propsFile.newDataInputStream())
Boolean flag = false; // This flag will tell us if we already chosen a Node
Boolean noAlowedNode=true; // This flag will tell us if there is no avaialbe Allowed Node to use
Boolean allAreTaken = false; // This flag will tell us if all slaves are taken
String node = null;  

// ILTLVW1476 is used only for Dev Gerrit Flow
// ILTLVW1539 is used only for Dev Veri Flow
// ILTLVW1539 is used only for Input Quallification

// def forbiddenNodes = ["ILTLVW1476","ILTLVW1539","ILTLVW1540"]

// For using only ILTLVW1580 and ILTLVW1580  use this line: (and remark the line above)

def forbiddenNodes = ["ILTLVWSSC220", "ILTLVW1476", "ILTLVW1539", "ILTLVW1540","ILTLVW1684", "ILTLVW1907", "ILTLVW1581", "ILTLVW2392", "ILTLVW2394", "ILTLVW1438"]
 
// For using only ILTLVW1464 use this line: (and remark the line above)
//def forbiddenNodes = ["ILTLVW1476", "ILTLVW1539", "ILTLVW1540", "ILTLVW1438"]

// For using only ILTLVW1438 use this line: (and remark the line above)
//def forbiddenNodes = ["ILTLVW1476", "ILTLVW1539", "ILTLVW1540", "ILTLVW1464"]

// For using only ILTLVW1540 use this line: (and remark the line above)
//def forbiddenNodes = ["ILTLVW1476", "ILTLVW1464", "ILTLVW1539", "ILTLVW1438"] 
 
// Run on all the slaves
for (aSlave in hudson.model.Hudson.instance.slaves)
{
	println('===============================================');

	if (!flag) // Check if we already chosen a Node for this Build
	{ 	
		
		println ('1 ===== DEBUG ===== flag is ' + flag) // DEBUG
		// flag = false
		// Chcek if this slave is Busy = Slave already runs a build

		println ('1.1 ===== DEBUG ===== Black List is ' + forbiddenNodes) // DEBUG
		println ('1.2 ===== DEBUG ===== currnet aSlave is ' + aSlave.name) // DEBUG
		println ('1.3 ===== DEBUG ===== Query Result is ' + forbiddenNodes.find { it ==~ aSlave.name }) // DEBUG
		
		if ((forbiddenNodes.find { it ==~ aSlave.name }) == null)    // Check if the currect aSlave is in the Blacklist
		{

			println ('1.4 ===== DEBUG ===== current aSlave is ' + aSlave.name + ' not in the black list') // DEBUG

			if (aSlave.getComputer().countBusy() == 0) 
			{
				println ('2 ===== DEBUG ===== flag is ' + flag) // DEBUG
				println('IDLE'); // The node is Idle and we can use it for the Build

				node = (aSlave.name); // Save the value of the chosen Node in a Property file
				props.setProperty('NODE_NAME', node.toString())
				props.store(propsFile.newWriter(), null)
				flag = true;
				noAlowedNode=false;

			} else
			{
				println ('3 ===== DEBUG ===== flag is ' + flag) // DEBUG
				println('BUSY'); // The node is Budy and now we have to check with what kind of Build

				String names = (aSlave.getComputer().getExecutors());
				String result = names.substring(47, 50);
				println  (result);
				
				if (result == "FB_") // In case the Slave runs a Build, we want to see if it runs a "FB" Build
					{
						println ('4 ===== DEBUG ===== flag is ' + flag) // DEBUG
						println ('This is a FB Build') 	// In case this is a FB Build then the Node that holds this build
														// will not be the Node that we will want to take the new Build
					} else
					{
						println ('5 ===== DEBUG ===== flag is ' + flag) // DEBUG
						println ('This is NOT a FB Build') // In case this is NOT a FB Build then we want this Node to take the new Build
					  
						node = (aSlave.name); // Save the value of the chosen Node in a Property file
						props.setProperty('NODE_NAME', node.toString())
						props.store(propsFile.newWriter(), null)
						flag = true;
						noAlowedNode=false;
					}
			}
		}	

	} else
	{
		// flag = true
		println ('6 ===== DEBUG ===== flag is ' + flag) // DEBUG
		println ('We have a Slave for the new Buid - ' + node.toString());
	}
}

if (!flag) 	// In case all Slaves (That are not in the Black list) are already Running with FB Jobs,  
			// then this script will choose the first Slave in line for the the new Iteration.
			// This Itteration will wait till the previous Iteration will finish
{
	for (aSlave in hudson.model.Hudson.instance.slaves)
	{
		println ('8.1 ===== DEBUG ===== currnet aSlave is ' + aSlave.name) // DEBUG
		println ('8.2 ===== DEBUG ===== Query Result is ' + forbiddenNodes.find { it ==~ aSlave.name }) // DEBUG

		if ((forbiddenNodes.find { it ==~ aSlave.name }) == null)    // Check if the currect aSlave is in the Blacklist
		{
			node = (aSlave.name); // Save the value of the chosen Node in a Property file
			props.setProperty('NODE_NAME', node.toString())
			props.store(propsFile.newWriter(), null)
			flag = true;			
			noAlowedNode=false;		}
	}

	if (!noAlowedNode) 	//noAlowedNode is False
						// flag is True
	{
		println ('8.3 ===== DEBUG ===== flag is ' + flag) // DEBUG
		props.load(propsFile.newDataInputStream())
		println props.getProperty('NODE_NAME')  		

	} else
	{
		println ('No allowed Slave is avaialbe, the balcklist contains these slaves:')  		
		println (forbiddenNodes) 
		build.setResult(FAILURE)
	}
	

}