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
from selenium.webdriver import ActionChains
from pyvirtualdisplay import Display
import pyautogui
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities





cap = DesiredCapabilities().FIREFOX

options = webdriver.FirefoxProfile()
options.set_preference("driver.download.dir", "/home/araketu/Documentos/dev/random")
options.set_preference("driver.download.useDownloadDir", True)
options.set_preference("driver.helperApps.neverAsk.saveToDisk", "audio/mpeg")

# display = Display(visible=0, size=(800, 600))
# display.start()
cap["marionette"] = True


driver = webdriver.Firefox(firefox_profile=options, executable_path="//usr/local/bin/geckodriver")


print('\nEntrando no site TST...')
driver.get('http://www.tst.jus.br/certidao')

print('\nTrocando de frame') 
driver.switch_to_frame(driver.find_element_by_xpath('//iframe'))

print('\nProcurando o botão de emissão e clicando')
emiti = driver.find_element_by_xpath("//input[@name='j_id_jsp_1384250394_2:j_id_jsp_1384250394_3']")
emiti.click()

print("\nentrou na condição")
WebDriverWait(driver, 10).until(
        
    EC.visibility_of_element_located((By.XPATH, "//input[@name='gerarCertidaoForm:cpfCnpj']"))
    
)

print('\nMandando o cnpj')

inputer = driver.find_element_by_xpath("//input[@name='gerarCertidaoForm:cpfCnpj']")
inputer.send_keys('19161345000155')



print("\nentrou na condição")
WebDriverWait(driver, 10).until(
        
    EC.visibility_of_element_located((By.XPATH, "//a[@href='soundCaptcha?x.mp3']"))
    
)


print("\nProcurando e clicando no  botão para ouvir ")
soundb= driver.find_element_by_xpath("//a[@href='soundCaptcha?x.mp3']")
soundb.click()
actionChain = ActionChains(driver)
actionChain.context_click(soundb).perform()
pyautogui.typewrite(['down','down','down','down','down','enter'])
time.sleep(3) 

pyautogui.typewrite(['enter'])
time.sleep(1)
pyautogui.typewrite(['enter'])

driver.save_screenshot("/home/araketu/Documentos/dev/random/tst.png")

print('\nFazendo o Download do arquivo de som ')
time.sleep(3) 

#convert mp3 file to wav                                                       
sound = AudioSegment.from_mp3("/home/araketu/Downloads/soundCaptcha")
sound.export("transcript.wav", format="wav")


fh = open("recognized.txt", "w+") 

AUDIO_FILE = 'transcript.wav' 

# Initialize the recognizer 
r = sr.Recognizer() 

# Traverse the audio file and listen to the audio 
with sr.AudioFile(AUDIO_FILE) as source: 
    audio_listened = r.listen(source) 

# Try to recognize the listened audio 
# And catch expections. 
try:	 
    rec = r.recognize_google(audio_listened,language='pt-br') 
    
    # If recognized, write into the file. 
    fh.write(rec+" ")
    nums=rec 

# If google could not understand the audio 
except sr.UnknownValueError: 
    print("Could not understand audio") 

# If the results cannot be requested from Google. 
# Probably an internet connection error. 
except sr.RequestError as e: 
    print("Could not request results.") 

inputer2 = driver.find_element_by_xpath("//input[@name='gerarCertidaoForm:textoAudioCaptcha']")
inputer2.send_keys(nums)

emiti = driver.find_element_by_xpath("//input[@name='gerarCertidaoForm:btnEmitirCertidao']")
emiti.click()

time.sleep(3)

pyautogui.typewrite(['enter','enter'])


driver.save_screenshot("/home/araketu/Documentos/dev/random/tst.png")


driver.quit()