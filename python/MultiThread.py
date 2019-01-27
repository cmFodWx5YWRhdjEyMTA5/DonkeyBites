import os
import shutil
import time
import threading
from selenium import webdriver
from selenium.webdriver.common.keys import Keys



def SignCabFileWithMicrosoft(build, arch, filename, locationPath, customer):
    try:
        driver = webdriver.Chrome(os.getcwd() + '\\chromedriver.exe')
        driver.maximize_window()
        time.sleep(3)
        driver.get("https://developer.microsoft.com/en-us/dashboard/hardware/Driver/")
        time.sleep(3)
        driver.find_element_by_id("cred_userid_inputtext").send_keys("tomer@ggg.com")
        time.sleep(3)
        driver.find_element_by_id("cred_userid_inputtext").send_keys(Keys.TAB)
        time.sleep(3)

        while True:
            try:
                driver.find_element_by_id("mso_account_tile").click()
                time.sleep(5)
                if driver.find_element_by_css_selector("input[name=passwd"):
                    break
            except Exception as e:
                print "Could not navigate to password screen"
                print str(e)
                time.sleep(10)

        while True:
            try:
                driver.find_element_by_css_selector("input[name=passwd").send_keys("ggg")
                time.sleep(3)
                driver.find_element_by_css_selector("input[type=submit]").click()
                time.sleep(10)
                if driver.find_element_by_css_selector("a[uitestid='newDriverButton']"):
                    break
            except Exception as e:
                print "Could not pass the password screen"
                print str(e)
                time.sleep(10)

        driver.find_element_by_css_selector("a[uitestid='newDriverButton']").click()
        time.sleep(10)
        driver.find_element_by_id("inputDriverName").send_keys(
            "enSilo" + "-" + "32" + "-" + "ggg.cab")
        time.sleep(10)
        cabFileName = "C:\Users\dorons\PycharmProjects\devopsTools\cabs" + "\\" + "32" + "\\" + "ggg.cab"

        while True:
            try:
                print "============== cabFileName - " + cabFileName
                driver.find_element_by_id("file").send_keys(cabFileName)
                time.sleep(10)
                if driver.find_element_by_css_selector("div[class='ng-scope step complete']"):
                    break
            except Exception as e:
                print "Could not upload cab file"
                print str(e)
                time.sleep(10)

        if arch == "64":
            buttontext = "spanRequestedSignature_WINDOWS_v100_X64_TH2_FULL"
        else:
            buttontext = "spanRequestedSignature_WINDOWS_v100_TH2_FULL"
        driver.quit();




    except Exception as e:
        print str(e)


def CopyFile(source, target):
    print "Copy " + source + " file"
    shutil.copy(source, target)



if __name__ == "__main__":
    print "Start Signing"

    threads = []
    print "1"
    path = "\\\\sdfsdfsdf-fs01\\Versions"
    customer = "sdfsdfsdfsdf"
    build="2.2.2.222"
    arch = "32"
    i=0
    print "2"
    major_version = float(build.split(".")[0] + "." + build.split(".")[1])

    while True:
        i += 1
        driver = "dddddd.cab"
        t = threading.Thread(target=SignCabFileWithMicrosoft,args=(build, arch, driver, path, customer))
        threads.append(t)
        t.start()
        print "===== Fire Thread for - [" + str(i) + "] - " + str(driver)
        time.sleep(15)

    for t in threads:
        t.join()
