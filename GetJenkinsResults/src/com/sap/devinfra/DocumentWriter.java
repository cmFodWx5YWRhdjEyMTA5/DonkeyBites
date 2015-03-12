package com.sap.devinfra;

import java.io.File;
import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;

import org.apache.commons.io.FileUtils;
import org.dom4j.Document;

public class DocumentWriter{

	public final String NOT_BUILT = "NOT_BUILT";

	public final String ERROR_STRING = "FAILED";
	public final String ERROR_STATUS = "FAILURE";

	public final String SUCCESS_STRING = "SUCCEEDED";
	public final String SUCCESS_STATUS = "SUCCESS";


	public String jenkinsServerUrl = "http://panda/jenkins/job/";

	public ArrayList<String> componentsArray = new ArrayList<String>();


	DocumentWriter(){
		componentsArray.add("designer-lib-qunit");
		componentsArray.add("designer-editor-components-qunit");

	}

	//	public String BuildFinalResult (String jenkins_job_name, String jenkins_build_number){
	//		
	//		String finalResultString = null;
	//		
	//		for each component in componenets DO
	//		updateResultHTMLFile(jenkins_component_name,jenkins_complete_url);
	//		System.out.println(finalResultString);
	//
	//	}	


	public ArrayList<URL> getJenkinsURL (String jenkins_job_name, String jenkins_build_number) throws MalformedURLException {

		ArrayList<URL> urlArray = new ArrayList<URL>();
		String stringUrl =null;
		
		for (int i = 0; i < 2; i = i+1) {

			stringUrl = jenkinsServerUrl + jenkins_job_name + "/" + jenkins_build_number + "/com.sap.ushell.ushell-designer$" + componentsArray.get(i) + "/api/xml";
			URL tempURL = new URL(stringUrl);
			urlArray.add(i, tempURL);
		}
		
		return urlArray;
	}


	/**********************************************************
	 * Inject the results into the HTML template 
	 * @throws IOException 
	 *********************************************************/
	public void InjectContent(String htmlText) throws IOException {
		
		File htmlTemplateFile = new File("C:\\Users\\i032517\\git\\panda\\ushell\\designer-utils\\Designer_QBS_dev_SUCCESS.html");
		String htmlString = FileUtils.readFileToString(htmlTemplateFile);
		String body = htmlText;
		htmlString = htmlString.replace("$body", body);
		File newHtmlFile = new File("C:\\Users\\i032517\\git\\panda\\ushell\\designer-utils\\Designer_QBS_dev_SUCCESS.html");
		FileUtils.writeStringToFile(newHtmlFile, htmlString);

	}

	/*************************************************************************
	 * Build the HTML of the build 
	 * Variables that it needs:
	 * component - What is the test component that is being handled?
	 * jenkins_url - what is the jenkins URL that need to be evaluated  
	 * @throws Exception 
	 *************************************************************************/


	public String extractJenkinsJobResult(){

		return "";

	}


	@SuppressWarnings("null")
	public String updateResultHTMLFile(ArrayList<URL> currentURL, Document dom) throws Exception {

		String componentFinalResultString = null;
		String testResult = null;

		JenkinsHandler jenkinsHandler = new JenkinsHandler();
		Boolean testExecuted = false;
		
		for (int i = 0; i < 2; i = i+1) {

			
			testResult = jenkinsHandler.getJenkinsJobResult(currentURL, dom); // Why the ConnectToJenkins.getJenkinsStatus has to be static?

			if (testResult.equals(NOT_BUILT)){

			} else {

				if(testResult.equals(ERROR_STATUS)){

					componentFinalResultString = "The tests of <b>" + componentsArray.get(i) + "</b> component had <b><span style='color:#384C91}'>" + ERROR_STRING + " </span></b>, See <a href=\"${ENV, var=\"HUDSON_URL\"}/job/${ENV, var=\"JOB_NAME\"}/${ENV, var=\"BUILD_NUMBER\"}/testReport/\">Report</a>\n<br>\n";
					testExecuted = true;

				} else {

					if(testResult.equals(SUCCESS_STATUS)){

						componentFinalResultString = "The tests of <b>" + componentsArray.get(i) + "</b> component had <b><span style='color:#384C91}'>" + SUCCESS_STRING + " </span></b>, See <a href=\"${ENV, var=\"HUDSON_URL\"}/job/${ENV, var=\"JOB_NAME\"}/${ENV, var=\"BUILD_NUMBER\"}/testReport/\">Report</a>\n<br>\n";
						testExecuted = true;

					}

				}

			}

			if (testExecuted == false ){

				componentFinalResultString = "No qUnit tests were executed in this build";
				
			}
			
		}

		return componentFinalResultString;
	}


}
