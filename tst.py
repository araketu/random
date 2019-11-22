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

driver.save_screenshot("/home/araketu/Documentos/dev/random/tst.png")

print('\nFazendo o Download do arquivo de som ')
time.sleep(3) 

# driver.get('http://aplicacao.jt.jus.br/cndtCertidao/soundCaptcha?x.mp3')
# driver.switch_to_window(driver.window_handles[0])

# import time, sys
# import urllib.request as us

# url ='http://aplicacao.jt.jus.br/cndtCertidao/soundCaptcha?x.mp3'

# print ("Connecting to "+url)
# response = us.urlopen(url, timeout=10.0)
# fname = "Sample"+str(time.clock())[2:]+".mp3"
# f = open(fname, 'wb')
# block_size = 1024
# print ("Recording roughly 10 seconds of audio Now - Please wait")
# limit = 10
# start = time.time()
# while time.time() - start < limit:
#     try:
#         audio = response.read(block_size)
#         if not audio:
#             break
#         f.write(audio)
#         sys.stdout.write('.')
#         sys.stdout.flush()
#     except Exception as e:
#         print ("Error "+str(e))
# f.close()
# sys.stdout.flush()
# driver.quit()
# print("")
# print ("10 seconds from "+url+" have been recorded in "+fname)




import sounddevice as sd
from scipy.io.wavfile import write
import os

fs = 44100  # this is the frequency sampling; also: 4999, 64000
seconds = 12  # Duration of recording

# sd.default.device = sd.query_devices()[8]["name"]
print(sd.query_devices())
sd.default.device = 0


myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
print("Starting: Speak now!")
sd.wait()  # Wait until recording is finished
print("finished")
write('output.wav', fs, myrecording)  # Save as WAV file
# # os.startfile("output.wav")



time.sleep(10) 
driver.quit()