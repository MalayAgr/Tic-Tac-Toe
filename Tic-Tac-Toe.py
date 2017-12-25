# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import random

board = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
possibilities = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
d = {}


def playerAssignment(player1, player2):
    d['player1'] = player1
    d['player2'] = player2

    print("\nThe players are: ")
    print("Player 1 (X): %s" % player1)
    print("Player 2 (O): %s" % player2)


def playerNames():
    l = []
    for i in range(2):
        l.append(input("Enter player's name: "))

    if random.choice(l) == l[0]:
        playerAssignment(l[0], l[1])
    else:
        playerAssignment(l[1], l[0])


def showBoard():
    print("----------")
    for i in range(len(board)):
        print("| " + board[i], end = '')
        if i in range(2, 9, 3):
            print("|")
            print("|--|--|--|")


def boardInstructions():
    print("This is your board.\n")
    print(
        "To play the game, each player will indicate the position they want to place their symbol in by inputting the corresponding number\n")
    print("After the first player makes his/her move, it will the be the second player's turn.\n")


def displayBoard(value, position):
    """
    Updates the board's values and displays it.
    """

    board[position] = value
    print("Current situation: ")
    showBoard()


def getWinner(value, turn):
    for (j1, j2, j3) in possibilities:
        if board[j1] == value and board[j2] == value and board[j3] == value and value == 'X':
            print(d['player1'] + " has won the match. Congratulations, " + d['player1'] + "!")
            return 1
        elif board[j1] == value and board[j2] == value and board[j3] == value and value == 'O':
            print(d['player2'] + " has won the match. Congratulations, " + d['player2'] + "!")
            return 1
        else:
            continue


def gamePlay():

    i = 0
    turnCount1 = 0
    turnCount2 = 0
    totalTurns = 0
    while i < len(board):

        if i % 2 == 0:

            turn = int(input("\n" + d['player1'] + ", enter the position where you want to make the change: "))

            turnCount1 += 1

            if turnCount1 < 3:

                displayBoard('X', turn - 1)
            else:
                displayBoard('X', turn - 1)
                if getWinner('X', totalTurns) == 1:
                    break


        else:

            turn = int(input("\n" + d['player2'] + ", enter the position where you want to make the change: "))

            turnCount2 += 1

            if turnCount2 < 3:
                displayBoard('O', turn - 1)
            else:
                displayBoard('O', turn - 1)
                if getWinner('O', totalTurns) == 1:
                    break

        i += 1
        totalTurns += 1
    else:
        return totalTurns


print("TIC-TAC-TOE")
print("We'll start by assigning player names. The player number will be selected by the computer")

if (input("Are you ready? (Y/N) ")) == 'Y' or (input("Are you ready? (Y/N) ")) == 'y':
    playerNames()

if (input("Ready to start the game? (Y/N) ")) == 'Y' or (input("Ready to start the game? (Y/N) ")) == 'y':

    showBoard()

    boardInstructions()
    choice = input("Ready to proceed? (Y/N) ")

    if choice == 'Y' or choice == 'y':
        c = gamePlay()
        if c == 9:
            print("It was a draw. Well played, both of you!")


