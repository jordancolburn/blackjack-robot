import os

def speak(message):
	os.system('espeak "' + message + '" | aplay') 

ranks = {
	'1': 'One',
	'2': 'Two',
	'3': 'Three',
	'4': 'Four',
	'5': 'Five',
	'6': 'Six',
	'7': 'Seven',
	'8': 'Eight',
	'9': 'Nine',
	'10': 'Ten',
	'J': 'Jack',
	'Q': 'Queen',
	'K': 'King',
	'A': 'Ace'
}

card_suit = {
	'H': 'Spades',
	'C': 'Clubs',
	'S': 'Spades',
	'D': 'Diamonds',
}

def speak_card(card):
	speak(ranks[card[0]])
	speak("of")
	speak(card_suit[card[1]])

def play_song():
	os.system('mpg123 -n 1 RHODES-HUMORME.mp3 | aplay') 
	
