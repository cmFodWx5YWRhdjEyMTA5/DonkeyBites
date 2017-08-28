pipeline {
    agent {
            label 'linux-build-server'
    }
    options {
        buildDiscarder(logRotator(numToKeepStr:'50'))
        disableConcurrentBuilds()
    }    
    stages {
        stage('Checkout SCM') {
            steps {
                addBadge("${env.CMAKE_COMMAND}")
                sh  '''
                    folder=`pwd`/ext
                    if [ -L $folder ]; then
                      echo "-=> Folder is SYMBOLIC"
                    else
                      echo "-=> Folder is not a soft link"
                      rm -rf $folder
                      ln -s /home/ensilo/ext ext  
                    fi
                    '''                
                checkout changelog: true, scm: 
                [   
                    $class: 'SubversionSCM', additionalCredentials: [
                        [credentialsId: '77f7fe1b-a2ce-4903-a459-ce8a6d9138e3', realm: '<https://svn.test.local:443> CollabNet Subversion Repository']
                    ],
                    excludedCommitMessages: '',
                    excludedRegions: '/trunk/Common/test.*\n/trunk/test_doron.*',
                    excludedRevprop: '',
                    excludedUsers: '', 
                    filterChangelog: false,
                    ignoreDirPropChanges: false,
                    includedRegions: '', 
                    locations: [
                        [
                            credentialsId: '77f7fe1b-a2ce-4903-a459-ce8a6d9138e3',
                            depthOption: 'infinity',
                            ignoreExternalsOption: false,
                            local: 'ext',
                            remote: 'https://svn.test.local/svn/test/ext'
                        ]                      
                        ,[
                            credentialsId: '77f7fe1b-a2ce-4903-a459-ce8a6d9138e3',
                            depthOption: 'infinity',
                            ignoreExternalsOption: false,
                            local: 'trunk-OBSOLETE', // I am checking out to have the polling mechanisim to work
                            remote: 'https://svn.test.local/svn/test/trunk'
                        ]
                        ],
                        workspaceUpdater: [$class: 'UpdateUpdater']
                ]
                sh "svn checkout https://svn.test.local/svn/test/trunk trunk"   // Doing this step manually since there is a problem
                                                                                // with doing it the "pipeline" way
            }
        }
        stage('Build') {
            steps {
                echo "-------------======== Build ========--------------"
                sh "env"
                sh '''
                    cd trunk
                    set -e
                    sudo chmod +x $CMAKE_COMMAND
                    ./$CMAKE_COMMAND
                    make
                    '''
            }
        }
        stage('Unit Tests') {
            steps {
                echo "-------------======== Unit Tests ========--------------"
                sh '''
                    cd trunk
                    cd UnitTests
                    ./test_unit_tests
                    '''
            }
        }
    }
    // post {
    //     success {
    //         notifyBuild ('SUCCESS')
    //     }

    //     failure {
    //         notifyBuild ('FAILURE')
    //     }  

    //     unstable {
    //         notifyBuild ('UNSTABLE')
    //     }            
    // }
}

def addBadge(String cmake_type) {
    
    def tagText = ""
    
    if (cmake_type ==~ /^cmake_clang\.sh$/) {
            tagText = "clang"
            print "type found - " + tagText
        } else if (cmake_type ==~ /^cmake_default\.sh$/) {
            tagText = "default"
            print "type found - " + tagText
        } else if (cmake_type ==~ /^cmake_centos_devtoolset2\.sh$/) {
            tagText = "devtoolset2"
            print "type found - " + tagText
        } else if (cmake_type ==~ /^cmake_centos_devtoolset4\.sh$/) {
            tagText = "devtoolset4"
            print "type found - " + tagText
        }
    manager.addShortText(tagText)    
}

def notifyBuild(String buildStatus = 'STARTED') {
    // build status of null means successful
    buildStatus = buildStatus ?: 'SUCCESS'

    // Default values
    def mailSubject = "${buildStatus}: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})"
    def mailContent = readFile 'jenkinsJobs/CI_Test/summary.html'
    def previousResult = currentBuild.previousBuild?.result
	  def toList = "doronshai@gmail.com"
    def slack_channel = '#build'

    // Override default values based on build status
    if (buildStatus == 'UNSTABLE') {
        colorCode = '#E8E8E8'
		wrap([$class: 'BuildUser']) {
			slackSend (channel: slack_channel, color: colorCode, message: "${env.JOB_NAME} #${env.BUILD_NUMBER} - " + buildStatus + " Started By ${env.BUILD_USER} (${env.BUILD_URL})")
			echo "Send Build UNSTALBE Summary HTML Mail..."
			emailext(   to: toList, replyTo: "postman@gorovdude.com",
						mimeType: 'text/html', subject: mailSubject, body: mailContent,
						recipientProviders: [[$class: 'DevelopersRecipientProvider'],[$class: 'CulpritsRecipientProvider']]);
		}        
    } else if (buildStatus == 'SUCCESS') {
        colorCode = '#3EA652'
        mailSubject = "FIXED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})"
        if (previousResult != 'SUCCESS') {
            wrap([$class: 'BuildUser']) {
                slackSend (channel: slack_channel, color: colorCode, message: "${env.JOB_NAME} #${env.BUILD_NUMBER} - FIXED Started By ${env.BUILD_USER} (${env.BUILD_URL})")
                echo "Send Build FIXED Summary HTML Mail..."
                emailext(   to: toList, replyTo: "postman@gorovdude.com",
                            mimeType: 'text/html', subject: mailSubject, body: mailContent,
                            recipientProviders: [[$class: 'DevelopersRecipientProvider'],[$class: 'CulpritsRecipientProvider']]);
            }
        }        
    } else if (buildStatus == 'FAILURE') {
        colorCode = 'CC0012'
		wrap([$class: 'BuildUser']) {
            slackSend (channel: slack_channel, color: colorCode, message: "${env.JOB_NAME} #${env.BUILD_NUMBER} - " + buildStatus + " Started By ${env.BUILD_USER} (${env.BUILD_URL})")
            echo "Send Build FAILURE Summary HTML Mail..."
            emailext(   to: toList, replyTo: "postman@gorovdude.com",
                        mimeType: 'text/html', subject: mailSubject, body: mailContent,
                        recipientProviders: [[$class: 'DevelopersRecipientProvider'],[$class: 'CulpritsRecipientProvider']]);
        }        
    }
}
