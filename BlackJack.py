#!/usr/bin/env python3
# BlackJack.py
# Milestone Program for Python Bootcamp Course
# Play BlackJack against the Dealer (Computer)

import random


# Set up global vars
curr_pos = 0    # Current position in the deck
game_on = True  # If player wishes to continue play


class Deck(object):
    # Create a virtual deck
    def __init__(self):
        self.deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13] * 4

    def shuffle_deck(self):
        random.shuffle(self.deck)
        global curr_pos
        curr_pos = 0
        return self.deck

    def deal_card(self):
        # Deal a card from the deck and return it
        global curr_pos
        if curr_pos == 52:
            shuffle_deck(self)
        curr_pos += 1
        return self.deck[curr_pos - 1]


class Player(object):
    # Create/update player data
    def __init__(self, bankroll, bet):
        self.bankroll = bankroll
        self.bet = bet


    def add_bankroll(self, amount):
        self.bankroll += amount


    def sub_bankroll(self, amount):
        self.bankroll -= amount


class Hand(object):
    # Create/Update/Show hands
    def __init__(self):
        self.dealer = []
        self.player = []

    def value(self, hand):
        # Add up the value of the hand and return it
        value = 0
        ace = False
        for card in hand:
            temp = int(card_value(card))
            if card_value == 1:
                ace = True
            value += temp
        # if you have an ace that will make BlackJack
        if ace and value + 10 == 21:
            value = value + 10
        return value

    def get_card(self, hand, card_pos):
        # Extract card from hand
        return hand[card_pos]


def play_BlackJack(deck, hand):
    # Play a hand
    # Create fresh deck, shuffle and deal two cards to each play
    deck.shuffle_deck()
    hand.dealer.append(deck.deal_card())
    hand.dealer.append(deck.deal_card())
    hand.player.append(deck.deal_card())
    hand.player.append(deck.deal_card())
    # Check to see if one of the players has BlackJack
    if hand.value(hand.dealer) == 21:
        print("Dealer has the " + show_card(hand.get_card(hand.player, 0)) + " and the " +
              show_card(hand.get_card(hand.dealer, 1)))
        print("Player has the " + show_card(hand.get_card(hand.player, 1)) + " and the " +
              show_card(hand.get_card(hand.player, 0)))
        print("Dealer has BlackJack, Dealer wins.")
    if hand.value(hand.player) == 21:
        print("Dealer has the " + show_card(hand.get_card(hand.dealer, 0)) + " and the " +
              show_card(hand.get_card(hand.dealer, 1)))
        print("Player has the " + show_card(hand.get_card(hand.player, 0)) + " and the " +
              show_card(hand.get_card(hand.player, 0)))
        print("You have BlackJack, You win.")
    # Neither Player has BlackJack so play the game
    while True:
        print("Your cards are: ")
        card_pos = 0
        while card_pos < len(hand.player):
            print(show_card(hand.get_card(hand.player, card_pos)))
            card_pos += 1
        print("Your total is " + str(hand.value(hand.player)))
        print("Dealer is showing the " + show_card(hand.get_card(hand.dealer, 0)))
        try:
            player_move = input("\nHit (H) or Stand (S)? ").upper()
        except:
            if player_move != "H" and player_move != "S":
                print("Please enter H or S")
                continue
        if player_move == "H":
            new_card = deck.deal_card()
            hand.player.append(new_card)
            print("User hits:.")
            print("Your card is the " + show_card(new_card))
            print("Your total is now " + str(hand.value(hand.player)))
            if hand.value(hand.player) > 21:
                print("You busted by going over 21, You lose.")
                print("Dealer's other card was the " + show_card(hand.get_card(hand.dealer, 1)))
                return False
        elif player_move == "S":
                break
    # If we get to this point user has Stood with 21 or less.   Now its the dealers chance to draw
    # Dealer draws cards until the dealer's total is > 16
    print("User stands.\nDealer's cards are")
    print("   " + show_card(card_value(hand.dealer[0])))
    print("   " + show_card(card_value(hand.dealer[1])))
    while hand.value(hand.dealer) <= 16:
        new_card = deck.deal_card()
        print("Dealer his and get the" + show_card(card_value(new_card)))
        hand.dealer.append(new_card)
        print("Dealer's total is " + str(hand.value(hand.dealer)))
    # Now a winner can be declared
    if hand.value(hand.dealer) > 21:
        print("Dealer busted by going over 21.  You win.")
        return True
    if hand.value(hand.dealer) == hand.value(hand.player):
        print("Dealer wins on a tie.  You lose.")
        return False
    if hand.value(hand.dealer) > hand.value(hand.player):
        print("Dealer wins, " + str(hand.value(hand.dealer)) + " points to " + str(hand.value(hand.player)))
        return False
    else:
        print("You win, " + str(hand.value(hand.player)) + " point to " + str(hand.value(hand.dealer)))
        return True


def show_card(card):
    # Convert integer value to display text and return it
    cards = ['', 'Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
    return cards[card]


def card_value(card):
    # Change face card to value of 10
    card = int(card)
    return 10 if card > 10 else card


def ask_player():
    # Get Player info before game starts
    bankroll = 0
    while True:
        try:
            bankroll = int(input("How big is your bankroll? $ "))
        except ValueError:
            print("You must enter a number")
            continue
        try:
            bet_amt = int(input("What is your bet size? $ "))
        except ValueError:
            print("You must enter a number")
            continue
        return Player(bankroll, bet_amt)


# Setup the Game and play until player quits or runs out of money
print('Welcome to BlackJack by Python')
global game_on
deck = Deck()
hand = Hand()
player = ask_player()
while player.bankroll > 0 and game_on:
    player_wins = play_BlackJack(deck, hand)
    if player_wins:
        player.add_bankroll(player.bet)
    else:
        player.sub_bankroll(player.bet)
    if player.bankroll == 0:
        print("You lost all your dough Dude")
        break
    else:
        print("You have $",player.bankroll,"in your bankroll")
        more = input("Continue play? (Y/N")
        if more.upper() != "Y":
            print("Congratulations you walked away with $" + str(player.bankroll))
            game_on = False
        else:
            hand.dealer = []
            hand.player = []