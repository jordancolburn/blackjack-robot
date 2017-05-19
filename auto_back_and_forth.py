#!/usr/bin/env python
import RPi.GPIO as GPIO
import video_dir
import car_dir
import motor
import time
from socket import *
from time import ctime          # Import necessary modules   
import distance
import audio
import card_img

ctrl_cmd = ['forward', 'backward', 'left', 'right', 'stop', 'read cpu_temp', 'home', 'distance', 'x+', 'x-', 'y+', 'y-', 'xy_home']

busnum = 1          # Edit busnum to 0, if you uses Raspberry Pi 1 or 0

HOST = ''           # The variable of HOST is null, so the function bind( ) can be bound to all valid addresses.
PORT = 21567
BUFSIZ = 1024       # Size of the buffer
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)    # Create a socket.
tcpSerSock.bind(ADDR)    # Bind the IP address and port number of the server. 
tcpSerSock.listen(5)     # The parameter of listen() defines the number of connections permitted at one time. Once the 
                         # connections are full, others will be rejected. 

audio.speak("hello. Please wait while I count my money.")

video_dir.setup(busnum=busnum)
car_dir.setup(busnum=busnum)
motor.setup(busnum=busnum)     # Initialize the Raspberry Pi GPIO connected to the DC motor. 
video_dir.home_x_y()
car_dir.home()
distance.setup()
card_img.setup()
motor.ctrl(0)

values = {
	'1': 1,
	'2': 2,
	'3': 3,
	'4': 4,
	'5': 5,
	'6': 6,
	'7': 7,
	'8': 8,
	'9': 9,
	'10': 10,
	'J': 10,
	'Q': 10,
	'K': 10,
	'A': 11,
}

speed = 50;

motor.setSpeed(speed)

movement_time = 2

audio.speak("Hello. My Name is Chip")


audio.speak("Starting Game")

print "stop"
motor.ctrl(0)
audio.speak("analyzing your cards.")
time.sleep(2)
cards = card_img.get_cards(2)
if (len(cards) == 2):	
	audio.speak("Your hand has a ")
	audio.speak_card(cards[0])
	audio.speak("and")
	audio.speak_card(cards[1])
	if (values[cards[0][0]] + values[cards[1][0]] == 21):
		audio.speak('You Have 21')
		motor.backward()
		audio.speak('Yay')
		time.sleep(.5)
		audio.speak('Wooooo')
		motor.forward()
		time.sleep(.5)
		motor.backward()
		audio.speak('Great Job')
		time.sleep(.5)
		motor.forward()
		motor.ctrl(0)
		audio.speak('Much Win')
		quit()
else:
	audio.speak("only found " + str(len(cards)) + " number of cards")
	quit()
print cards

while distance.distance() < 88:
	motor.backward()
	time.sleep(.05)

print "stop"
motor.ctrl(0)
audio.speak("analyzing the dealer cards.")
time.sleep(2)
dealer_cards = card_img.get_cards(1)
if dealer_cards:
	audio.speak('the dealer has a ')	
	audio.speak_card(dealer_cards[0])
else:
	audio.speak('I did not find any cards for the dealer')
	quit()


while distance.distance() > 35:
	motor.forward()
	time.sleep(.05)

print "stop"
motor.ctrl(0)

if (values[cards[0][0]] + values[cards[1][0]] < 17):
	audio.speak('You Should Hit')
else:
	audio.speak('You Should Stay')
time.sleep(.5)
audio.speak('Good Luck')

tcpSerSock.close()


