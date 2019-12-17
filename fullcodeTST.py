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
import re
import PyPDF2 
import textract
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


CNPJ = '19161345000155'


def cert_tst(CNPJ):

    
    for raiz, diretorios, arquivos in os.walk('/home/araketu/Downloads'):
        for arquivo in arquivos:
            if arquivo.endswith('.mp3'):
                os.remove(os.path.join(raiz,arquivo))

    for raiz, diretorios, arquivos in os.walk('/home/araketu/Downloads'):
        for arquivo in arquivos:
            if arquivo.endswith('.pdf'):
                os.remove(os.path.join(raiz,arquivo))        


    driver = webdriver.Chrome()

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
    inputer.send_keys(CNPJ)


    print("\nentrou na condição")
    WebDriverWait(driver, 10).until(
            
        EC.visibility_of_element_located((By.XPATH, "//a[@href='soundCaptcha?x.mp3']"))
        
    )

    soundb= driver.find_element_by_xpath("//a[@href='soundCaptcha?x.mp3']")
    soundb.click()
    time.sleep(3)
    handles = driver.window_handles;
    size = len(handles);
    
        

    actionChain = ActionChains(driver)
    actionChain.context_click(soundb).perform()
    pyautogui.typewrite(['down','down','down','down','enter'])
    time.sleep(3) 

    pyautogui.typewrite(['enter'])
    time.sleep(1)
    pyautogui.typewrite(['enter'])

    print('\nFazendo o Download do arquivo de som ')
    time.sleep(3) 

    try:
        #convert mp3 file to wav                                                       
        sound = AudioSegment.from_mp3("/home/araketu/Downloads/soundCaptcha.mp3")
        sound.export("transcript.wav", format="wav")
    except:
        print('\nNão encontrou o arquivo de som')
        driver.quit()
        cert_tst(CNPJ)    

    fh = open("recognized.txt", "w+") 

    print('\nAnalizando audio')
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
        print("Não foi possível interpretar o audio") 

    # If the results cannot be requested from Google. 
    # Probably an internet connection error. 
    except sr.RequestError as e: 
        print("Não foi possível acessar o serviço do google")
    inputer2 = driver.find_element_by_xpath("//input[@name='gerarCertidaoForm:textoAudioCaptcha']")
    inputer2.send_keys(nums)

    emiti = driver.find_element_by_xpath("//input[@name='gerarCertidaoForm:btnEmitirCertidao']")
    emiti.click()
    time.sleep(3)

    # erro = driver.find_element_by_xpath("//li['Código de validação inválido.']")
    filename ='/home/araketu/Downloads/' + 'certidao_'+ str(CNPJ) +'.pdf'
    erro = os.path.exists(filename)    


    if erro:
        print(erro)
    else:
        print("\nErro ao enviar os núemros")
        print(erro)
        driver.quit()
        cert_tst(CNPJ)

    pyautogui.typewrite(['enter','enter','enter'])
    print('\nCertidão emitida')


    driver.save_screenshot("/home/araketu/Documentos/dev/random/tst.png")


    driver.quit()



    #'rb' for read binary mode
    #write a for-loop to open many files -- leave a comment if you'd #like to learn how
    filename ='/home/araketu/Downloads/' + 'certidao_'+ str(CNPJ) +'.pdf'
   
    
    

    #open allows you to read the file
    pdfFileObj = open(filename,'rb')

    #The pdfReader variable is a readable object that will be parsed
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    #discerning the number of pages will allow us to parse through all #the pages
    num_pages = pdfReader.numPages
    count = 0
    text = ""

    #The while loop will read each page
    while count < num_pages:
        pageObj = pdfReader.getPage(count)
        count +=1
        text += pageObj.extractText()

    #This if statement exists to check if the above library returned #words. It's done because PyPDF2 cannot read scanned files.
    if text != "":
        text = text

    #If the above returns as False, we run the OCR library textract to #convert scanned/image based PDF files into text
    else:
        print('Deu ruim!')

    #Get Status from certidão
    status = re.search("NÃO CONSTA",text)

    print('\n--------------------------------------------------------')
    if status:
        print("\nCertidão: Negativa")
    else:
        print("\nCertidão: Positiva")

    
    list01 = []

    count=0

    for i in text:
        #Search on the ler_text the dates.
        y = re.findall("[0-2][0-9]\/[0-1][0-9]\/\d{4}",text)
        if y:
            j = y
        

    emitida=j[0]
    validade=j[1]

    print('\nCertidão emitida em: '+emitida)
    print('\nCertidão valida até: '+validade) 

      



cert_tst(CNPJ)

 
       
