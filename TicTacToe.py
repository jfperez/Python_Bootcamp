#!/usr/bin/env python3
# This is a milestone project from Udemy Python Bootcamp Course
# Its a 2 player Tic Tac Toe game

import random
import os

game_on = True
new_game = True


def draw_board(board_disp):
    # Draw board based on contents of board_disp
    print('\nTIC TAC TOE\n')
    print(board_disp[1], ' | ', board_disp[2], ' | ', board_disp[3])
    print('---|-----|---')
    print(board_disp[4], ' | ', board_disp[5], ' | ', board_disp[6])
    print('---|-----|---')
    print(board_disp[7], ' | ', board_disp[8], ' | ', board_disp[9])


def get_move(player):
    # Get input for move
    while True:
        # print(player)
        try:
            move = int(input(('',player_one, player_two)[player] + ' enter cell #:'))
        except ValueError:
            print("Must be a # from 1 to 9")
            continue
        return move


def chk_move(move):
    # Make sure cell is not already taken
    if not board_list[move]:
        return True
    else:
        print('Cell already taken')
        return False


def post_move(move, player):
    # Update board_list for new move
    board_list[move] = player
    board_disp[move] = ('', 'X', 'O')[player]


def chk_win(player):
    # Check if current move wins the game
    if  board_list[1] == board_list[2] == board_list[3] == player:
        return True
    elif board_list[4] == board_list[5] == board_list[6] == player:
        return True
    elif board_list[7] == board_list[8] == board_list[9] == player:
        return True
    elif board_list[1] == board_list[4] == board_list[7] == player:
        return True
    elif board_list[2] == board_list[5] == board_list[8] == player:
        return True
    elif board_list[3] == board_list[6] == board_list[9] == player:
        return True
    elif board_list[1] == board_list[5] == board_list[9] == player:
        return True
    elif board_list[7] == board_list[5] == board_list[3] == player:
        return True
    else:
        return False

def full_board(board_list):
    # See if board_list is full
    if 0 in board_list[1:]:
            return False
    return True


def replay():
    # Ask player if they want to play another game
    return input('Play again? (y/n) ').lower().startswith('y')


def first_play():
    # Get players names and start the game by random choice
    player_one = input('Enter player name: ')
    player_two = input('Enter 2nd player name: ')
    choice = random.choice((player_one, player_two))
    print(choice + " you will start the game")
    if choice != player_one:
        player_one, player_two = player_two, player_one
    return player_one, player_two

def play_turn(player):
    # Process turn for a player
    move = get_move(player)
    chk_move(move)
    post_move(move, player)
    draw_board(board_disp)
    if chk_win(player):
        print('Congratulations ' + ('',player_one, player_two)[player]  + ' you won the game!')
        if not replay():
            return True, False
        else:
            return  True, True
    if full_board(board_list):
        wait = input("It's a draw folks")
        if not replay():
            return True, False
        else:
            return True, True
    return False, False


while True:
    # Main loop for game play
    if not new_game:
        break
    # Do the setup for the game
    os.system('cls')
    board_list = [0] * 10
    board_disp = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    player_one, player_two = first_play()
    draw_board(board_disp)
    # Play the game
    while game_on:
        # Player_one turn
        game_over, new_game = play_turn(1)
        if game_over or new_game:
            break
        # Player_two turn
        game_over, new_game = play_turn(2)
        if game_over or new_game:
            break
