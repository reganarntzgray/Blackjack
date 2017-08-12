# -*- coding: utf-8 -*-
"""
Created on Sat Aug 12 08:03:35 2017

@author: Regan
"""
import random as rnd
import numpy as np
from collections import OrderedDict
import pandas as pd

#load hard table and soft table

hard_np = np.array([['H','H','H','H','H','H','H','H','H','H'],
                   ['H','H','H','H','H','H','H','H','H','H'],
                   ['H','D','D','D','D','H','H','H','H','H'],
                   ['D','D','D','D','D','D','D','D','H','H'],
                   ['D','D','D','D','D','D','D','D','D','H'],
                   ['H','H','S','S','S','H','H','H','H','H'],
                   ['S','S','S','S','S','H','H','H','H','H'],
                   ['S','S','S','S','S','H','H','H','H','H'],
                   ['S','S','S','S','S','H','H','H','H','H'],
                   ['S','S','S','S','S','H','H','H','H','H'],
                   ['S','S','S','S','S','S','S','S','S','S']])

Total = [7,8,9,10,11,12,13,14,15,16,17]
columns = ['2','3','4','5','6','7','8','9','10','1']

hard_rules = pd.DataFrame(hard_np, index=Total,columns=columns)
hard_rules.index.name = 'Total'


soft_np = np.array([['H','H','H','D','H','H','H','H','H','H'],
                   ['H','H','H','D','D','H','H','H','H','H'],
                   ['H','H','H','D','D','H','H','H','H','H'],
                   ['H','H','D','D','D','H','H','H','H','H'],
                   ['H','H','D','D','D','H','H','H','H','H'],
                   ['H','D','D','D','D','H','H','H','H','H'],
                   ['S','DS','DS','DS','DS','S','S','H','H','H'],
                   ['S','S','S','S','S','S','S','S','S','S'],
                   ['S','S','S','S','S','S','S','S','S','S']])

Total = [12,13,14,15,16,17,18,19,20]
columns = ['2','3','4','5','6','7','8','9','10','1']

soft_rules = pd.DataFrame(soft_np, index=Total,columns=columns)
soft_rules.index.name = 'Total'


doubles_np = np.array([['P','P','P','P','P','P','H','H','H','H'],
                   ['P','P','P','P','P','P','H','H','H','H'],
                   ['H','H','H','P','P','H','H','H','H','H'],
                   ['D','D','D','D','D','D','D','D','H','H'],
                   ['P','P','P','P','P','H','H','H','H','H'],
                   ['P','P','P','P','P','P','H','H','H','H'],
                   ['P','P','P','P','P','P','P','P','P','P'],
                   ['P','P','P','P','P','S','P','P','S','S'],
                   ['S','S','S','S','S','S','S','S','S','S'],
                   ['P','P','P','P','P','P','P','P','P','P']])

Total = [4,6,8,10,12,14,16,18,20,2]
columns = ['2','3','4','5','6','7','8','9','10','1']

doubles_rules = pd.DataFrame(doubles_np, index=Total,columns=columns)
doubles_rules.index.name = 'Total'

#defining gambler class and player subclass

class Gambler(object):
    def __init__(self,name,chips):
        self.name = name
        self.win_loss = []
        self.chips = chips
    def add_score(self,score):
        self.win_loss.append(score)

class Player(Gambler):
    def __init__(self,name,win_loss,chips,bet=[1],hand=[[0,0]],complete=[False],completed=False,nat=False,doubled=False,split=False,pair=False):
        Gambler.__init__(self,name,win_loss,chips)
        self.bet = bet
        self.hand = hand
        self.complete = complete
        self.nat = nat
        self.completed = completed
        self.doubled = doubled
        self.split = split
        self.pair = pair

#creating functions

#get input function

def get_input(prompt,type_= None,max=10,min=1):
    if type_ == 'int':
        while True:
            try:
                v = int(input(prompt))
            except ValueError:
                print("That is a psychotic thing to answer - try again asshole")
                continue
            if min<=v<=max:
                return v
                break
            else:
                 print("That's an absurd number to give")
                 continue
    if type_ == 'bin':
        while True:
            bin_dict = {}
            bin_dict['true'] = True
            bin_dict['t'] = True
            bin_dict['yes'] = True
            bin_dict['y'] = True
            bin_dict['1'] = True
            bin_dict['false'] = False
            bin_dict['f'] = False
            bin_dict['no'] = False
            bin_dict['n'] = False
            bin_dict['0'] = False
            tv = str(input(prompt).lower())
            try:
                v = bin_dict[tv]
                return v
                break
            except KeyError:
                print('Invalid answer - there are only 2 options, try again plz')
                continue
    else:
        v = str(input(prompt))
        while v == "":
            print('You need to say something at least ...')
            v = str(input(prompt))
        return v

#Press enter to continue

def enter():
    input('Press Enter to continue ...')

#functions to create deck and to deal a single card and update deck

def create_deck(k):
    deck = np.repeat(np.append(np.arange(1,11),[10,10,10]),4*k)
    rnd.shuffle(deck)
    return deck

def deal_card(deck,k,reshuffle_limit):
    deck
    card = deck[0]
    deck = deck[1:]
    if len(deck)<=52*k*(1-reshuffle_limit):
        deck = create_deck(k)
    return {'card':card,'deck':deck}


#check if hand is a natural blackjack:

def is_natural(hand):
    if len(hand)!=2:
        nat = False
    elif 1 in hand and sum(hand)==11:
        nat = True
    else:
        nat = False
    return nat

#check if hand is a pair

def is_pair(hand):
    if len(hand)!=2:
        pair = False
    elif hand[0]==hand[1]:
        pair=True
    else:
        pair=False
    return pair

#find current total of single hand

def total(hand):
    hard_total = sum(hand)
    soft_total = hard_total+10
    if 1 in hand and soft_total <= 21:
        tot = soft_total
        return tot
    else:
        tot = hard_total
        return tot

#ask players if they want to hit (assuming they don't have a natural)

def advice(hand,dealer,table):
    col = dealer[1]
    if is_pair(hand)==False:
        row = total(hand)
    else:
        row = sum(hand)
    if row>18:
        advice = 'S'
    elif row==sum(hand) and row>17:
        advice = 'S'
    elif row<7 and is_pair(hand)==False:
        advice = 'H'
    else:
        advice = table.loc[row][str(col)]
    return advice

def interpret_advice(advice,give_advice):
    if give_advice==True:
        if advice == 'H':
            print('My advice is to hit')
        elif advice == 'D':
            print('My advice is to double - if not allowed, hit')
        elif advice == 'S':
            print('I would stand if I were you')
        elif advice == 'DS':
            print('My advice is to double - if not allowed, stand')
        elif advice == 'P':
            print('My advice is to split your pair')
        else:
            print('Not sure how to advise you right now, sorry!')
        enter()
    else:
        pass
        
def hit_function(deck,k,reshuffle_limit,hand,player,i_hand_start):
    deal = deal_card(deck,k,reshuffle_limit)
    card = deal['card']
    deck = deal['deck']
    hand.append(card)
    player.hand[i_hand_start] = hand
    tot = total(hand)
    if tot > 21:
        print("Rough man, you got a %s, bringing your total to %s  which means you just busted, try again next time loser!" % (str(card),str(tot)))
        player.complete[i_hand_start] = True
       
    else:
        print("You have been dealt a %s, bringing your total to %s, your hand is now %s" % (str(card),str(tot),str(hand).strip('[]')))
      
        if tot==21:
            player.complete[i_hand_start] = True
    enter()
            
   

def hit_question(player,i_hand_start,hand,dealer,hard_table,soft_table,doubles_table,deck,k,reshuffle_limit,doubling,give_advice):
    tot = total(hand)
    if 1 in hand and sum(hand)<11:
        table = soft_table
        if player.pair==False:
            print("%s, your hand is %s, with a total of %s. The dealer is showing %s " % (player.name,str(hand).strip('[]'),str(tot),str(dealer[1]).strip('[]')))
            enter()
            interpret_advice(advice(hand,dealer,table),give_advice)
           
    else:
        table = hard_table
        if player.pair==False:
            print("%s, your hand is %s, with a total of %s. The dealer is showing %s " % (player.name,str(hand).strip('[]'),str(tot),str(dealer[1]).strip('[]')))
            enter()
            interpret_advice(advice(hand,dealer,table),give_advice)
           
    if doubling>0 and len(hand)==2 and player.doubled==False:
        double = get_input('Would you like to double down? If y you will double your bet and recieve exactly one more card on this hand. Enter y or n: ','bin')
        enter()
        if double:
            player.doubled=True
            bet=2*player.bet[i_hand_start]
            player.bet[i_hand_start]=bet
            hit_function(deck,k,reshuffle_limit,hand,player,i_hand_start)
            player.complete[i_hand_start]=True
            
        else:
            hit = get_input("Would you like to hit? Enter y or n: " ,'bin')
            enter()
            #process the player's choice
            if hit:
                hit_function(deck,k,reshuffle_limit,hand,player,i_hand_start)
            else:
                player.complete[i_hand_start] = True
    else:
        hit = get_input("Would you like to hit? Enter y or n: " ,'bin')
            #process the player's choice
        if hit:
            hit_function(deck,k,reshuffle_limit,hand,player,i_hand_start)
        else:
            player.complete[i_hand_start] = True


 
def ask_hit(dealer,player,deck,k,reshuffle_limit,hard_table,soft_table,doubles_table,splitting_level,doubling,give_advice):
    #check if player has split their hands
    i_hand_start = 0
    for hand in player.hand:
        
        if player.complete[i_hand_start] == True:
            pass
        elif is_natural(hand):
            print("Wow %s, you have a natural blackjack! You win 1.5x your initial bet!" % (player.name))
            enter()
            player.nat = True
            player.complete[i_hand_start]=True
            player.completed=True
            #check for pair
        elif is_pair(hand) and splitting_level>0:
            print("%s you have a pair of %ss! The dealer is showing %s " % (player.name, str(hand[0]),str(dealer[1])))
            enter()
            table = doubles_table
            interpret_advice(advice(hand,dealer,table),give_advice)
            
            player.pair = True
            if 1 in hand:
                print("If you split your aces you can only draw 1 additional card on each")
                enter()
            split = get_input("Would you like to split into 2 hands? This will double your bet. Enter y or n: ",'bin')
            enter()
            
            if split:
                player.split = True
                player.pair = False
                deal1 = deal_card(deck,k,reshuffle_limit)
                deck = deal1['deck']
                hand1 = [hand[0],deal1['card']]
                player.hand[i_hand_start]= hand1
                
                deal2 = deal_card(deck,k,reshuffle_limit)
                deck = deal2['deck']
                hand2 = [hand[1],deal2['card']]
                player.hand.append(hand2)
                bet = player.bet[i_hand_start]
                player.bet.append(bet)
                player.complete.append(False)
                i_hand_end = i_hand_start+1
                
                if 1 in hand:
                    player.completed=True
                    print("%s your first hand is now %s . It is complete with a total of %s" % (player.name,str(hand1).strip('[]'),str(total(hand1))))
                    enter()
                    print("%s your second hand is now %s . It is complete with a total of %s" % (player.name,str(hand2).strip('[]'),str(total(hand2))))
                    enter()
                    break
                else:
                
                    if total(hand1)>20:
                        player.complete[i_hand_start]=True
                        print("%s your first hand is now %s . It is complete with a total of %s" % (player.name,str(hand1).strip('[]'),str(total(hand1))))
                        enter()
                    else:
                        hit_question(player,i_hand_start,hand1,dealer,hard_table,soft_table,doubles_table,deck,k,reshuffle_limit,doubling,give_advice)
                                    
                    if total(hand2)>20:
                        player.complete[i_hand_end]=True
                        print("%s your second hand is now %s . It is complete with a total of %s" % (player.name,str(hand2).strip('[]'),str(total(hand2))))
                        enter()
                        break
                    else:
                        hit_question(player,i_hand_end,hand2,dealer,hard_table,soft_table,doubles_table,deck,k,reshuffle_limit,doubling,give_advice)
                        break
            else:
                hit_question(player,i_hand_start,hand,dealer,hard_table,soft_table,doubles_table,deck,k,reshuffle_limit,doubling,give_advice)
                player.pair=False
                    
            #ask player if they want to hit
        else:
            hit_question(player,i_hand_start,hand,dealer,hard_table,soft_table,doubles_table,deck,k,reshuffle_limit,doubling,give_advice)
        
        i_hand_start += 1    


#decide whether dealer will hit or stand

def dealer_hit(dealer,deck,k,reshuffle_limit):
    tot = total(dealer)
    if tot < 17:
        deal = deal_card(deck,k,reshuffle_limit)
        dealer.append(deal['card'])
        deck = deal['deck']
    else:
        pass


#calculate the score from a complete hand

def score(hand):
    if is_natural(hand)==True:
        score = 22
    else:
        tot = total(hand)
        if tot <= 21:
            score = tot
        else:
            score = 0
    return score

#determine how much the player won/lost this hand

def win_loss(player,dealer_score):
    wl = [0]*len(player.hand)
    i_hand = 0
    for hand in player.hand:
        bet = player.bet[i_hand]
        sp = score(player.hand[i_hand])
        sd = dealer_score
        if sp==22 and player.split==True:
            sp=21
        if sp>sd:
            if sp == 22 and player.split==False:
                wl[i_hand] = 1.5*float(bet)
               
            else:
                wl[i_hand] = bet
               
        elif sp == sd:
            
            wl[i_hand] = 0
          
        else:
            
            wl[i_hand] = -1*bet
        i_hand += 1
        
    return wl
            
        
        

#check if players' hands are all complete

#check if all hands for a single player are complete

def player_complete(player):
    i_hand = 0
    sum=0
    for hand in player.hand:
        complete = player.complete[i_hand]
        if complete==False:
            return False
        else:
            sum+=1
        i_hand += 1
    if sum==len(player.hand):
        player.completed=True
        return True
    

def round_complete(current_players):
    for player in current_players:
        player_complete(player)
    if any(player.completed == False for player in current_players):
        round_done = False
        return round_done
    else:
        round_done = True
        return round_done

#if dealer has a natural - check if other players have naturals

def check_hands(dealer,current_players,deck,k,reshuffle_limit,hard_table,soft_table,doubles_table,splitting_level,doubling,give_advice):
    if is_natural(dealer)==True:
        print("Sorry playas, you just got burned - I've got a natural betches")
        enter()
        for player in current_players:
            player.completed = True
            if is_natural(player.hand[0])==True:
                print("Nice %s! You have one too, you won't lose any $" % (player.name))
            else:
                 print("Sorry %s, your cards were %s, you lose your bet" % (player.name,str(player.hand[0])))
            enter()
    else:
        for player in current_players:
            ask_hit(dealer,player,deck,k,reshuffle_limit,hard_table,soft_table,doubles_table,splitting_level,doubling,give_advice)
            
        dealer_hit(dealer,deck,k,reshuffle_limit)


#############################################################################

play_again = True
dev_mode = False

#player interaction code (for each game)
if  dev_mode:
    n = 1
    k = 2
    c = 100
    reshuffle_limit = 50
    splitting_level=1
    doubling=1
    give_advice=True
else:
    n = get_input("How many people would like to take the gamble?!? (max of 10) ",'int',10)
    k = get_input("How many decks would you like to play with? (max of 6) ",'int',6)
    c = get_input("How many chips would you like to start out with? ",'int',10000)
    reshuffle_limit = get_input("At what percentage into the decks would you like the dealer to reshuffle? ","int",100)
    splits = get_input("Do you want to allow splitting? Enter y or n: " ,'bin')
    if splits:
        splitting_level=1
    else:
        splitting_level=0
    doubles = get_input("Do you want to allow doubling down? Enter y or n: ",'bin')
    if doubles:
        doubling=1
    else:
        doubling=0
    give_advice = get_input("Do you want the Blackjack master to give you strategy advice? Enter y or n: ",'bin')
   


#get player names
if dev_mode:
    deck = create_deck(k)
    deck[1]=5
    deck[3]=5
    gamblers = []
    names = []
    
    i=1
    while i < (n+1):
        name_i = 'reg'
        if name_i not in names:
            gamblers.append(Gambler(name_i,c))
            names.append(name_i)
            i += 1
        else:
            print("Sorry, that name is taken")
            continue
else:
    deck = create_deck(k)
    
    gamblers = []
    names = []
    
    i=1
    while i < (n+1):
        name_i = get_input("player %s, what's your name? " % (str(i)))
        if name_i not in names:
            gamblers.append(Gambler(name_i,c))
            names.append(name_i)
            i += 1
        else:
            print("Sorry, that name is taken")
            continue

#creating shuffled deck


#player interaction code (for each hand)

while play_again == True:

    deal=deal_card(deck,k,reshuffle_limit) #get rid of the burn card
    deck=deal['deck']

    #ask players if they are betting this hand and how much they want to bet
    #deal the first two cards to current players and dealer

    current_players = []

    for gambler in gamblers:
        in_i = get_input("%s, would you like to place a bet this round? Enter: y or n: " % gambler.name,'bin')
        if in_i==True:
            bet = get_input("How many chips would you like to bet? ",'int',gambler.chips)
            gambler.__class__ = Player
            gambler.bet = [bet]
            deal=deal_card(deck,k,reshuffle_limit)
            gambler.hand = [[deal['card']]]
            deck = deal['deck']
            gambler.complete = [False]
            gambler.completed = False
            gambler.nat = False
            gambler.doubled = False
            gambler.split = False
            gambler.pair = False
            current_players.append(gambler)

    deal=deal_card(deck,k,reshuffle_limit)
    dealer = [deal['card']]
    deck = deal['deck']
    
    enter()
    
    for player in current_players:
        deal = deal_card(deck,k,reshuffle_limit)
        card = deal['card']
        deck = deal['deck']
        player.hand[0].append(card)

    deal = deal_card(deck,k,reshuffle_limit)
    dealer.append(deal['card'])
    deck = deal['deck']

    #complete dealer and players hands

    while round_complete(current_players) == False:
        check_hands(dealer,current_players,deck,k,reshuffle_limit,hard_rules,soft_rules,doubles_rules,splitting_level,doubling,give_advice)
  
    while total(dealer) < 17:
        dealer_hit(dealer,deck,k,reshuffle_limit)
 
    #compute and store the win loss results for each player
    
    print("The dealer's cards were %s, totalling %s" % (str(dealer),str(total(dealer))))
    enter()

    dealer_score = score(dealer)
    if dealer_score==0:
        print("Fook me! You're all in luck - I busted")
        enter()
    
    for player in current_players:
        wl = win_loss(player,dealer_score)
        player.__class__ = Gambler
        player.chips += sum(wl)
        player.add_score(wl)
        insert = (player.name,str(sum(wl)),str(player.chips))
        if sum(wl) > 0:
            print("Nice %s, you win %s chips, your new total is %s!" % insert)
        elif sum(wl) == 0:
            print("It all equaled out this time %s, that means you both win and lose %s chips, your total stays constant at %s" % insert)
        else:
            print("Sorry %s, you lose %s chips, your total is now %s" % (player.name,str(-1*sum(wl)),str(player.chips)))
        enter()

    play_again = get_input("Do you gamblers wanna take another chance? Enter y or n: ",'bin')
    if play_again == False:
        chips = []
        for gambler in gamblers:
            chips.append(gambler.chips)
            print("%s your final chip total was %s" % (gambler.name,gambler.chips))
            enter()
        m = max(chips)
        win_ind = [i for i, j in enumerate(chips) if j == m]
        winners = [gamblers[win_ind[j]].name for j, i in enumerate(win_ind)]
        print("That makes the winners: %s with %s chips" % (', '.join(map(str, winners)),m))
        print("Thanks for playing, I look forward to taking more of your money next time!")