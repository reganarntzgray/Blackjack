# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 10:02:15 2017

@author: Regan
""" 
import random as rnd
import numpy as np
from multi_key_dict import multi_key_dict
from collections import OrderedDict
import pandas as pd

#load hard table and soft table

hard_rules = pd.read_csv('Hard_table.csv', sep=',')
soft_rules = pd.read_csv('Soft_table.csv', sep=',')
doubles_rules = pd.read_csv('Doubles_table.csv', sep=',')

hard_rules.set_index('Total',inplace=True)
soft_rules.set_index('Total',inplace=True)
doubles_rules.set_index('Total',inplace=True)

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
            bin_dict = multi_key_dict()
            bin_dict['true','t','yes','y','1'] = True
            bin_dict['false','f','no','n','0'] = False
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
            print("You have a pair %s! of %ss the dealer is showing %s " % (player.name, str(hand[0]),str(dealer[1])))
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
        print("Sorry playas, you just got burned - I've got a natural betch")
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
