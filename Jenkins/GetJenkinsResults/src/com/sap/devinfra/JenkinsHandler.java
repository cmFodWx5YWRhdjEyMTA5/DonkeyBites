package com.sap.devinfra;

import org.dom4j.io.SAXReader;
import org.dom4j.Document;
import org.dom4j.Element;
import java.net.URL;
import java.util.List;

public class ConnectToJenkins {

	public void getJenkinsStatus(String jenkins_url) throws Exception {

		// every Hudson model object exposes the .../api/xml, but in this example
		// we'll just take the root object as an example
		//URL url = new URL("http://deadlock.netbeans.org/hudson/api/xml");

		URL url = new URL(jenkins_url);

		// if you are calling security-enabled Hudson and
		// need to invoke operations and APIs that are protected,
		// consult the 'SecuredMain" class
		// in this package for an example using HttpClient.

		// read it into DOM.
		Document dom = new SAXReader().read(url);

		for( Element result : (List<Element>)dom.getRootElement().elements("result")) {

			if(result.getText().equals("SUCCESS")){
				
				System.out.println(result.getText());
			}
			
			else {
				
				if(result.getText().equals("FAILURE")){
					
					System.out.println(result.getText());
				}
				
				else {
					
					if(result.getText().equals("NOT_BUILT")){
						
						System.out.println(result.getText());
					}
					
				}
				
			}
			
		}
		
	}
	
}