#!/usr/bin/python
# import cv2.cv as cv
# import tesseract
import re, csv
from time import sleep, time
from random import uniform, randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException    
from selenium.webdriver.common.keys import Keys


start = time()	 
url='http://immoney.win/showadv.php?rstr=0.7682405831190879'
driver = webdriver.Firefox(executable_path='/Users/doronshai/code/geckodriver')

driver.get(url)

mainWin = driver.current_window_handle  

driver.find_element_by_id("username").send_keys("doronshai")
driver.find_element_by_id("password").send_keys("Ilmbfvm2018")
driver.find_element_by_name('loginf1').click()
driver.find_element_by_xpath("/html/body/div[@id='outer']/div[@id='main']/h2/div").click()



try:
    while True:
        solved_string=""
        for i in range(1, 5):
            current_number = driver.find_element_by_xpath("/html/body/div[@id='outer']/div[@id='main']/form/div/table/tbody/tr/td/div[@id='cimg" + str(i) + "']/img")
            current_number_value = current_number.get_attribute('src')[-5]
            solved_string+=str(current_number_value)
        driver.find_element_by_name('capcha').send_keys(solved_string)
        sleep(1)
        driver.find_element_by_xpath("/html/body/div[@id='outer']/div[@id='main']/form/div[3]/input").click()
        sleep(2)
except KeyboardInterrupt:
    pass





# print "=========== ", current_number_value, " ============="



# img = driver.find_element_by_xpath('//div[@id="recaptcha_image"]/img')
# src = img.get_attribute('src')


# gray = cv.LoadImage('captcha.jpeg', cv.CV_LOAD_IMAGE_GRAYSCALE)
# cv.Threshold(gray, gray, 231, 255, cv.CV_THRESH_BINARY)
# api = tesseract.TessBaseAPI()
# api.Init(".","eng",tesseract.OEM_DEFAULT)
# api.SetVariable("tessedit_char_whitelist", "0123456789abcdefghijklmnopqrstuvwxyz")
# api.SetPageSegMode(tesseract.PSM_SINGLE_WORD)
# tesseract.SetCvImage(gray,api)
# print api.GetUTF8Text()



sleep(10)

driver.quit();

# # move the driver to the first iFrame 
# driver.switch_to_frame(driver.find_elements_by_tag_name("cimg1"))

