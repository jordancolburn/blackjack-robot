#!/usr/bin/env python
import time
import audio
import re

def get_value_of_facecard(card):
	c = card[0:1]
	if c == 'J':
		return 10
	elif c == 'Q':
		return 10
	elif c == 'K':
		return 10
	elif c == 'A':
		return [1,11]

def get_value(card): 
	numbers = re.findall('\d+', card[0])
	if len(numbers) != 0:
		return int(numbers[0])
	else:
		return get_value_of_facecard(card[0])

def get_score(cards):
	total = 0
	is_soft_score = False
	for card in cards:
		value = get_value(card)

		if isinstance(value, list):
			if total + value[1] > 21:
				total += value[0]
			else:
				total += value[1]
				is_soft_score = True
		else:
			total += value
	
	print 'total ' + str(total)
	return [total, is_soft_score]

# gets the score

def car_pullup():
	audio.speak("Let the game begin, please deal player cards")
#Car pulls up and says let the game begin

def car_pullup2():
	audio.speak("Let the game continue, please deal dealer cards")


def read_dealer_cards():
	print("Reading dealer cards")
	return [('10','H'), ('K','D')]
# reads the initial dealer cards
# returns an array of strings. each string identifies a card (Stephen knows format)

def read_player_cards():
	print("Reading player cards")
	return [('10','H'), ('10','D')]
# reads the initial dealer cards
# returns an array of strings. each string identifies a card (Stephen knows format)


def car_reads_extra_card():
	print("Reading extra card")
	return [('5','H')]
#read one extra card

def car_says_tie():
	audio.speak("Tie!")
# just say tie.


def car_says_player_wins(player_score, dealer_score):
	audio.speak("player wins, " + str(player_score) + " beats " + str(dealer_score))
	
#car declares player as winner

def car_says_dealer_wins(player_score, dealer_score):
	audio.speak("dealer wins, "+ str(dealer_score) + " beats " + str(player_score))
#car declares dealer as winner

def car_asks_for_player_card():
	audio.speak("Extra player card, please")
	#car asks for an extra player card

def car_signals_player_stand():
	audio.speak("player stand")
#signal player stand

def car_asks_for_dealer_card():
	audio.speak("Extra dealer card, please")
# ask for extra dealer card

def car_acknowledges_push(score):
	audio.speak("Push " + str(score) + " both")
#achknowledge push 

#constants
WAIT_FOR_DEAL_SECS=3
WAIT_FOR_EXTRA_CARD_SECS=1

#bank := $50
#bet := $5
bank = 50
bet=5
soft_score=False
 
#Car pulls up and sets. Car notify its ready
car_pullup()

#Waits X seconds for 2 player and 2 dealer cards to be dealt
time.sleep(WAIT_FOR_DEAL_SECS)

#Car reads player cards, drives over and reads dealer cards
player_cards=read_player_cards()
print player_cards

car_pullup2()
time.sleep(WAIT_FOR_DEAL_SECS)

dealer_cards=read_dealer_cards()
print dealer_cards


player_score_and_soft_score = get_score(player_cards)
player_score = player_score_and_soft_score[0]
player_soft_score = player_score_and_soft_score[1]

print "playerscore"
print player_score
print player_soft_score

dealer_scoreand_soft_score = get_score(dealer_cards)
dealer_score=dealer_scoreand_soft_score[0]
dealer_soft_score=dealer_scoreand_soft_score[1]

print "dealerscore"
print dealer_score
print dealer_soft_score


if player_score==21 and dealer_score == 21:
	car_says_tie()
	
elif player_score==21:
	bank=bank+bet
	car_says_player_wins(player_score, dealer_score)
	

elif dealer_score==21:
	bank=bank-bet
	car_says_dealer_wins()
else:
	#Decide if the player should hit or stand. NTD: Will the car notify us to hit?
	player_score_calc = True
	while player_score_calc:
		if player_score <= 11 or (player_soft_score==False and ((player_score==12 and not dealer_score in range (4,6))or (player_score in range(13,16) and dealer_score in range (7,11)))) or (player_soft_score==True and (player_score in range(13,17) or player_score == 18 and dealer_score >= 9)):
			car_asks_for_player_card()
			time.sleep(WAIT_FOR_EXTRA_CARD_SECS)
			card = car_reads_extra_card() 
			player_cards.extend(card)
			print 'recalculating player cards :' + str(player_cards)
			player_score_and_soft_score  = get_score(player_cards)
			player_score = player_score_and_soft_score[0]
			player_soft_score = player_score_and_soft_score[1]
		else:
			car_signals_player_stand()
			player_score_calc = False
	
	#Decide if the dealer should hit or stand.  Car will give X seconds for this to happen.
	dealer_score_calc = True
	while dealer_score_calc:
	    
		if dealer_score < 16 or (dealer_soft_score==True and dealer_score == 17):
			car_asks_for_dealer_card()
			time.sleep(WAIT_FOR_EXTRA_CARD_SECS)
			card = car_reads_extra_card()				
			dealer_cards.extend(card)
			print 'recalculating dealer cards :' + str(dealer_cards)
			dealer_scoreand_soft_score = get_score(dealer_cards)
			dealer_score=dealer_scoreand_soft_score[0]
			dealer_soft_score=dealer_scoreand_soft_score[1]
		else:
			car_signals_player_stand()
			dealer_score_calc = False
		
	#Car goes and reads all of the dealer cards.
	if player_score > dealer_score:
		bank = bank + bet
		car_says_player_wins(player_score, dealer_score)
	elif player_score < dealer_score:
		bank=bank-bet
		car_says_dealer_wins(player_score, dealer_score)
	else:
		car_acknowledges_push(player_score)

	  
	