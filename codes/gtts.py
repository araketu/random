import speech_recognition as sr
from os import path
from pydub import AudioSegment


# convert mp3 file to wav                                                       
# sound = AudioSegment.from_mp3("soundCaptcha.mp3")
# sound.export("transcript.wav", format="wav")

# Import necessary libraries 


# Input audio file to be sliced 
audio = AudioSegment.from_wav("transcript.wav") 

''' 
Step #1 - Slicing the audio file into smaller chunks. 
'''
# Length of the audiofile in milliseconds 
n = len(audio) 

# Variable to count the number of sliced chunks 
counter = 1

# Text file to write the recognized audio 
fh = open("recognized.txt", "w+") 

# Interval length at which to slice the audio file. 
# If length is 22 seconds, and interval is 5 seconds, 
# The chunks created will be: 
# chunk1 : 0 - 5 seconds 
# chunk2 : 5 - 10 seconds 
# chunk3 : 10 - 15 seconds 
# chunk4 : 15 - 20 seconds 
# chunk5 : 20 - 22 seconds 
interval = 5 * 450

# Length of audio to overlap. 
# If length is 22 seconds, and interval is 5 seconds, 
# With overlap as 1.5 seconds, 
# The chunks created will be: 
# chunk1 : 0 - 5 seconds 
# chunk2 : 3.5 - 8.5 seconds 
# chunk3 : 7 - 12 seconds 
# chunk4 : 10.5 - 15.5 seconds 
# chunk5 : 14 - 19.5 seconds 
# chunk6 : 18 - 22 seconds 
overlap = 1.5 * 450

# Initialize start and end seconds to 0 
start = 0
end = 0

# Flag to keep track of end of file. 
# When audio reaches its end, flag is set to 1 and we break 
flag = 0

# Iterate from 0 to end of the file, 
# with increment = interval 
for i in range(0, 2 * n, interval): 
	
	# During first iteration, 
	# start is 0, end is the interval 
	if i == 0: 
		start = 0
		end = interval 

	# All other iterations, 
	# start is the previous end - overlap 
	# end becomes end + interval 
	else: 
		start = end - overlap 
		end = start + interval 

	# When end becomes greater than the file length, 
	# end is set to the file length 
	# flag is set to 1 to indicate break. 
	if end >= n: 
		end = n 
		flag = 1

	# Storing audio file from the defined start to end 
	chunk = audio[start:end] 

	# Filename / Path to store the sliced audio 
	filename = 'chunk'+str(counter)+'.wav'

	# Store the sliced audio file to the defined path 
	chunk.export(filename, format ="wav") 
	# Print information about the current chunk 
	print("Processing chunk "+str(counter)+". Start = "
						+str(start)+" end = "+str(end)) 

	# Increment counter for the next chunk 
	counter = counter + 1
	
	# Slicing of the audio file is done. 
	# Skip the below steps if there is some other usage 
	# for the sliced audio files. 


''' 
Step #2 - Recognizing the chunk and writing to a file. 
'''

	# Here, Google Speech Recognition is used 
	# to take each chunk and recognize the text in it. 

	# Specify the audio file to recognize 

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

# Check for flag. 
# If flag is 1, end of the whole audio reached. 
# Close the file and break. 



# # use the audio file as the audio source                                        
# r = sr.Recognizer()

# # transcribe audio file                                                         
# audio = 'transcript.wav'
# #audio = "soundCaptcha.mp3"

# with sr.AudioFile(audio) as source:
#     audio = r.record(source)
    
# try:
#     text = r.recognize_google_cloud(audio)
#     print(text)

# except Exception as e:
#     print(e)        