import re
import os
import img2pdf 
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from PIL import Image
import wand 
from wand.image import Image
from wand.display import display


service = Service('//usr/bin/chromedriver')
service.start()
driver = webdriver.Remote(service.service_url)
driver.get('http://cnd.dataprev.gov.br/cws/contexto/cnd/cnd.html')


driver.switch_to_frame(driver.find_element_by_xpath('/html/frameset/frame[@name="CORPO"]'))
inputer = driver.find_element_by_name("num")
inputer.send_keys('19161345000155')

consult = driver.find_element_by_xpath("//td/input[@value='Consulta']")
consult.click()

cert = driver.find_element_by_xpath("//font/a")
cert.click()

driver.save_screenshot("/home/araketu/Documentos/dev/CND/cnd.png")


dates = driver.find_elements_by_tag_name('font')
for date in dates:
    print(date.text)
    text = re.search("[0-2][0-9]\/[0-1][0-9]\/\d{4}",date.text)
    print(text)




# driver.quit()