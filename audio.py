import os

def speak(message):
	os.system('espeak "' + message + '" | aplay') 
