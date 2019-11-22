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
    print(rec) 

# If google could not understand the audio 
except sr.UnknownValueError: 
    print("Could not understand audio") 

# If the results cannot be requested from Google. 
# Probably an internet connection error. 
except sr.RequestError as e: 
    print("Could not request results.") 