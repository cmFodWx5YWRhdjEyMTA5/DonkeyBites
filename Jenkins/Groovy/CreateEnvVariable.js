import hudson.model.*

  
//  This step will set Env html5_deploy to 'true' if the folder '_html5_workdir'
//  (value is set in previous job) is there.

def _html5_workdir = build.getEnvironment(listener).get('html5_workdir')
def _dir = new File(_html5_workdir)

def pa_html5 = new ParametersAction([
	new StringParameterValue("html5_deploy", _dir.exists().toString())
])

  
//  This step will set Env java_deploy to 'true' as default for all flows.
//  In the FB Flow, Only when the Env Profile is not equal to 'html5' then Env java_deploy will be set to 'false'

build.addAction(pa_html5)

def java_deploy = 'true'
def _build_profile = build.getEnvironment(listener).get('Profile')
def pa_java = new ParametersAction([
	new StringParameterValue("java_deploy",(_build_profile != 'html5').toString())
])


build.addAction(pa_java)