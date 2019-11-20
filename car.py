import speech_recognition as sr
from os import path
from pydub import AudioSegment
import cv2 as cv
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
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import StaleElementReferenceException








for i in range(1202,1251):
    service = Service('//usr/bin/chromedriver')
    service.start()
    browser = webdriver.Remote(service.service_url)
    # try:
    browser.get("https://www.receita.fazenda.gov.br/PessoaJuridica/CNPJ/cnpjreva/Cnpjreva_Solicitacao.asp")

    browser.switch_to_frame(browser.find_element_by_xpath('/html/frameset/frame[@name="main"]'))
    button = WebDriverWait(browser, 5).until(
        EC.visibility_of_element_located((By.XPATH, '//input[@name="captchaSonoro"]'))
    )
    button.click()

    image = browser.find_element_by_tag_name('img')


    if browser.save_screenshot("cnpj.png"):
        print("Screenshot saved! %s"%(i))

    image_cv = cv.imread("cnpj.png")
    # crop = image_cv[250:-615,205:380]

    crop = image_cv[261:291,205:380]
    filename = "/home/araketu/Documentos/dev/random/img/%s.png"%(i)

    cv.imwrite(filename, crop)


    browser.quit()
# except:
#     print("oi")