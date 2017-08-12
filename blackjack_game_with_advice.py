import blackjack.blackjack_wa as bj

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
    n = bj.get_input("How many people would like to take the gamble?!? hehahehahaha!! ",'int',5)
    k = bj.get_input("How many decks would you like to play with? ",'int',6)
    c = bj.get_input("How many chips would you like to start out with? ",'int',10000)
    reshuffle_limit = bj.get_input("At what percentage into the decks would you like the dealer to reshuffle? ","int",100)
    splits = bj.get_input("Do you want to allow splitting? Enter y or n: " ,'bin')
    if splits:
        splitting_level=1
    else:
        splitting_level=0
    doubles = bj.get_input("Do you want to allow doubling down? Enter y or n: ",'bin')
    if doubles:
        doubling=1
    else:
        doubling=0
    give_advice = bj.get_input("Do you want the Blackjack master to give you strategy advice? Enter y or n: ",'bin')
   


#get player names
if dev_mode:
    deck = bj.create_deck(k)
    deck[1]=1
    deck[3]=1
    gamblers = []
    names = []
    
    i=1
    while i < (n+1):
        name_i = 'reg'
        if name_i not in names:
            gamblers.append(bj.Gambler(name_i,c))
            names.append(name_i)
            i += 1
        else:
            print("Sorry, that name is taken")
            continue
else:
    deck = bj.create_deck(k)
    
    gamblers = []
    names = []
    
    i=1
    while i < (n+1):
        name_i = bj.get_input("player %s, what's your name? " % (str(i)))
        if name_i not in names:
            gamblers.append(bj.Gambler(name_i,c))
            names.append(name_i)
            i += 1
        else:
            print("Sorry, that name is taken")
            continue

#creating shuffled deck


#player interaction code (for each hand)

while play_again == True:

    deal=bj.deal_card(deck,k,reshuffle_limit) #get rid of the burn card
    deck=deal['deck']

    #ask players if they are betting this hand and how much they want to bet
    #deal the first two cards to current players and dealer

    current_players = []

    for gambler in gamblers:
        in_i = bj.get_input("%s, would you like to place a bet this round? Enter: y or n: " % gambler.name,'bin')
        if in_i==True:
            bet = bj.get_input("How many chips would you like to bet? ",'int',gambler.chips)
            gambler.__class__ = bj.Player
            gambler.bet = [bet]
            deal=bj.deal_card(deck,k,reshuffle_limit)
            gambler.hand = [[deal['card']]]
            deck = deal['deck']
            gambler.complete = [False]
            gambler.completed = False
            gambler.nat = False
            gambler.doubled = False
            gambler.split = False
            gambler.pair = False
            current_players.append(gambler)

    deal=bj.deal_card(deck,k,reshuffle_limit)
    dealer = [deal['card']]
    deck = deal['deck']
    
    bj.enter()
    
    for player in current_players:
        deal = bj.deal_card(deck,k,reshuffle_limit)
        card = deal['card']
        deck = deal['deck']
        player.hand[0].append(card)

    deal = bj.deal_card(deck,k,reshuffle_limit)
    dealer.append(deal['card'])
    deck = deal['deck']

    #complete dealer and players hands

    while bj.round_complete(current_players) == False:
        bj.check_hands(dealer,current_players,deck,k,reshuffle_limit,bj.hard_rules,bj.soft_rules,bj.doubles_rules,splitting_level,doubling,give_advice)
  
    while bj.total(dealer) < 17:
        bj.dealer_hit(dealer,deck,k,reshuffle_limit)
 
    #compute and store the win loss results for each player
    
    print("The dealer's cards were %s, totalling %s" % (str(dealer),str(bj.total(dealer))))
    bj.enter()

    dealer_score = bj.score(dealer)
    if dealer_score==0:
        print("Fook me! You're all in luck - I busted")
        bj.enter()
    
    for player in current_players:
        wl = bj.win_loss(player,dealer_score)
        player.__class__ = bj.Gambler
        player.chips += sum(wl)
        player.add_score(wl)
        insert = (player.name,str(sum(wl)),str(player.chips))
        if sum(wl) > 0:
            print("Nice %s, you win %s chips, your new total is %s!" % insert)
        elif sum(wl) == 0:
            print("It all equaled out this time %s, that means you both win and lose %s chips, your total stays constant at %s" % insert)
        else:
            print("Sorry %s, you lose %s chips, your total is now %s" % (player.name,str(-1*sum(wl)),str(player.chips)))
        bj.enter()

    play_again = bj.get_input("Do you gamblers wanna take another chance? Enter y or n: ",'bin')
    if play_again == False:
        chips = []
        for gambler in gamblers:
            chips.append(gambler.chips)
            print("%s your final chip total was %s" % (gambler.name,gambler.chips))
            bj.enter()
        m = max(chips)
        win_ind = [i for i, j in enumerate(chips) if j == m]
        winners = [gamblers[win_ind[j]].name for j, i in enumerate(win_ind)]
        print("That makes the winners: %s with %s chips" % (', '.join(map(str, winners)),m))
        print("Thanks for playing, I look forward to taking more of your money next time!")