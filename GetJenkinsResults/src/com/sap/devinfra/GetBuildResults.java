package com.sap.devinfra;

public class GetJenkinsBuildResult {
	
	public static void main(String[] args) throws Exception {
		
	
		// [0] - http://panda/jenkins/view/NG_QBS/job/
		// [1] - NG_Designer_ALL_QBS_Dev
		// /
		// [2] - 171
		// /com.sap.fiori$
		// [3] - sap.ushell.designer.apps.appConfigEditor
		// /api/xml

		String jenkins_server_url = args[0];
		String jenkins_job_name = args[1];
		String jenkins_build_number = args[2];
		String jenkins_artifact_name = args[3];

		String jenkins_complete_url = jenkins_server_url + jenkins_job_name + "/" + jenkins_build_number + "/com.sap.fiori$" + jenkins_artifact_name + "/api/xml";
		ConnectToJenkins connecttojenkins = new ConnectToJenkins();
		connecttojenkins.getJenkinsStatus(jenkins_complete_url);
			
	}

}
