import speech_recognition as sr
from os import path
from pydub import AudioSegment

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
driver.get('http://www.tst.jus.br/certidao')

driver.switch_to_frame(driver.find_element_by_xpath('//iframe'))
emiti = driver.find_element_by_xpath("//input[@name='j_id_jsp_1384250394_2:j_id_jsp_1384250394_3']")
emiti.click()

driver.switch_to_frame(driver.find_element_by_css_selector('//iframe'))
play = driver.find_elements_by_name("//tbody/tr/td/ul/li/a")
# play.click()
for pla in play:
    print(play)


# for emit in emiti:
#     print(emiti)


#cjjjonvert mp3 file to wav                                                       
sound = AudioSegment.from_mp3("soundCaptcha (2).mp3")
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
    rec = r.recognize_google(audio_listened,language='pt') 
    
    # If recognized, write into the file. 
    fh.write(rec+" ")
    print(rec) 

# If google could not understand the audio 
except sr.UnknownValueError: 
    print("Could not understand audio") 

# If the results cannot be requested from Google. 
# Probably an internet connection error. 
except sr.RequestError as e: 
    print("Could not request results.") 