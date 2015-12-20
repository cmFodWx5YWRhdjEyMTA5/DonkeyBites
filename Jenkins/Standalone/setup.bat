::Manual steps:
::1. Create some temp folder for the installation procedure (can be deleted afterwards)
::2. Copy the ZIP file to this folder
::3. Execute the setup.bat

:: Make sure you have 7z , if not http://www.7-zip.org/a/7z1512-x64.exe

@echo on


cygwin_install.bat
:: PARAMETERS WITH DEFAULT VALUES
::SET DRIVE=C
::SET JRE_INSTALL_PATH="Program Files\java\JenkinsJRE"

:: EXTRACT ZIP
::7z e Standalone.7z -y 

:: INSTALLATION SCRIPT

::msiexec.exe /i jre1.7.0_75.msi /qn /passive /Lv C:\aaa\setup.log INSTALLCFG="params.cfg"
::INSTALLCFG=params.cfg
::start /w jre-7u79-windows-i586.exe /s INSTALLDIR=%DRIVE%:\%JRE_INSTALL_PATH%  

::SET JAVA_HOME=c:\ssdsdsdsdsdsdsdsd
::SET PATH=%PATH%;%JAVA_HOME%


:: INSTALL JENKINS
start "jenkinsStandalone" "java" -jar jenkins.war

::COPY ALL PLUGINS AND STUFF INTO THE JENKNIS FOLDER - check the -t option
ping 127.0.0.1 -n 30 > nul
xcopy /y /h /e /r  jenkins\jobs\* %USERPROFILE%\.jenkins\jobs\*
xcopy /y /h /e /r  jenkins\plugins\* %USERPROFILE%\.jenkins\plugins\*

ping 127.0.0.1 -n 80 > nul

java -jar jenkins-cli.jar -s http://localhost:8080/ reload-configuration

::for %i in (jenkins\plugins\*) do java -jar jenkins-cli.jar -s http://localhost:8080/ install-plugin %i

pause





