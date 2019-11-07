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
driver.get('http://aplicacao.jt.jus.br/cndtCertidao/soundCaptcha?x.mp3')