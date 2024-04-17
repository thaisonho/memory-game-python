import sys
import os
import msvcrt
import random 
import time
import numpy as np  
from PIL import Image 
import keyboard
from colorama import Fore, Style
import matplotlib.pyplot as plt
import ctypes
from ctypes import wintypes
from pathlib import Path
from pathlib import Path

TERM_WIDTH   = os.get_terminal_size().columns
TERM_HEIGHT  = os.get_terminal_size().lines
MENU_ART_LEN = int(68)
MENU_WIDTH   = int(29)
MENU_HEIGHT  = int(6)

menu = R'''
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃     1. Start New game     ┃
┃     2.     Scores         ┃
┃     3.     Guide          ┃ 
┃     4.     Quit           ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
'''

menu_banner = R'''
• ▌ ▄ ·. ▄▄▄ .• ▌ ▄ ·.       ▄▄▄   ▄· ▄▌   ▄▄ •  ▄▄▄· • ▌ ▄ ·. ▄▄▄ .
·██ ▐███▪▀▄.▀··██ ▐███▪ ▄█▀▄ ▀▄ █·▐█▪██▌  ▐█ ▀ ▪▐█ ▀█ ·██ ▐███▪▀▄.▀·
▐█ ▌▐▌▐█·▐▀▀▪▄▐█ ▌▐▌▐█·▐█▌.▐▌▐▀▀▄ ▐█▌▐█▪  ▄█ ▀█▄▄█▀▀█ ▐█ ▌▐▌▐█·▐▀▀▪▄
██ ██▌▐█▌▐█▄▄▌██ ██▌▐█▌▐█▌.▐▌▐█•█▌ ▐█▀·.  ▐█▄▪▐█▐█▪ ▐▌██ ██▌▐█▌▐█▄▄▌
▀▀  █▪▀▀▀ ▀▀▀ ▀▀  █▪▀▀▀ ▀█▄▀▪.▀  ▀  ▀ •   ·▀▀▀▀  ▀  ▀ ▀▀  █▪▀▀▀ ▀▀▀ 
'''

# without any args: reset color
# with 3 args: red, green, blue for foreground
# with 6 args: rgb for foreground & background
def changeTextColor(*args):
    if len(args) == 0:
        print("\x1b[0m", end='')
    if len(args) == 3:
        print("\x1b[38;2;{};{};{}m".format(args[0], args[1], args[2]), end='')
    if len(args) == 6:
        print("\x1b[38;2;{};{};{};48;2;{};{};{}m".format(args[0], args[1], args[2], args[3], args[4], args[5], args[6]), end='')

def GotoXY(x, y) -> str:
    res = "\x1b[{};{}f".format(y, x)
    return res

def printArtAtPos(x, y, art):
    art_lines = art.split('\n')
    for lines in art_lines:
        print(GotoXY(x, y) + lines)
        y += 1

def getMenuInput(x, y) -> int:
    res: int
    while True:
        try:
            res = int(input(GotoXY(x, y) + 'Please pick your choice: '))
            if res > 0 and res < 5:
                break
            else:
                raise ValueError
        except ValueError:
            print(GotoXY(x, y) + 40 * ' ', end='')
            print(GotoXY(x, y) + 'Error! Please re-enter')
            time.sleep(2)
            print(GotoXY(x, y) + 40 * ' ', end='')
    return res


def gameMenu():
    os.system("cls")
    changeTextColor(255, 209, 227)
    x_banner = (TERM_WIDTH - MENU_ART_LEN) // 2
    x_menu = (TERM_WIDTH - MENU_WIDTH) // 2
    printArtAtPos(x_banner, 1, menu_banner)
    changeTextColor(255, 250, 183)
    printArtAtPos(x_menu, 7, menu)
    changeTextColor()
    user_choice = getMenuInput(x_menu, 14)
    if user_choice == 1:
        os.system("cls")
        startGame()
    if user_choice == 2:
        # Scores()
        print("scores")
    if user_choice == 3:
        # Guide()
        print("guide")
    if user_choice == 4:
        # Exit
        return


# {---------------LOGIC GAME-----------------}

left = 35
top = 5
size = 6
countPair = 0
score = 0
check = False
game_time = time.time()
player = "Player 1"

current_pos = [0, 1]  # Initial position (0, 0)
visited = [False] * (size + 1) * (size + 1) # explanation
icon = np.zeros((7, 7))

answer_list = []
matches = []

first_block = [0, 0]
second_block = [0, 0]

def Random():
    global matches

    for i in range(0, 12):
        matches.append(1)

    for i in range(12, 24):
        matches.append(2)

    for i in range(24, 36):
        matches.append(3)

    random.shuffle(matches)

def gotoXY(x, y):
    sys.stdout.write("\x1b[%d;%df" % (y, x))
    sys.stdout.flush()

def drawGameBoard():
    global left, top, size
    # Draw top line
    gotoXY(left + 1, top)
    sys.stdout.write("┌")
    for i in range(1, size * 8):
        if i % 8 == 0:
            sys.stdout.write("┬")
        else:
            sys.stdout.write("─")
    sys.stdout.write("┐\n")

    # Draw right line
    for i in range(1, size * 4):
        gotoXY(size * 8 + left + 1, i + top)
        if i % 4 != 0:
            sys.stdout.write("│")
        else:
            sys.stdout.write("┤")
    gotoXY(size * 8 + left + 1, size * 4 + top)
    sys.stdout.write("┘\n")

    # Draw bottom line
    for i in range(1, size * 8):
        gotoXY(size * 8 + left - i + 1, size * 4 + top)
        if i % 8 == 0:
            sys.stdout.write("┴")
        else:
            sys.stdout.write("─")

    gotoXY(left + 1, size * 4 + top)
    sys.stdout.write("└")

    # Draw left line
    for i in range(1, size * 4):
        gotoXY(left + 1, size * 4 + top - i)
        if i % 4 != 0:
            sys.stdout.write("│")
        else:
            sys.stdout.write("├")

    # Draw vertical lines
    for i in range(1, size * 4):
        for j in range(8, size * 8, 8):
            if i % 4 != 0:
                gotoXY(j + left + 1, i + top)
                sys.stdout.write("│")

    # Draw horizontal lines
    for i in range(1, size * 8):
        for j in range(4, size * 4, 4):
            gotoXY(i + left + 1, j + top)
            if i % 8 == 0:
                sys.stdout.write("┼")
            else:
                sys.stdout.write("─")

    sys.stdout.flush()

def drawInforBoard():
    global left, top, size, score, player, game_time

    for i in range(4):
        gotoXY(left + size * 8 + 8, top + i * 4 + 3)

        if i == 1:
            sys.stdout.write("Player: {}".format(player))
        elif i == 2:
            sys.stdout.write("Score: {}".format(score))
        elif i == 3:
            elapsed_time = time.time() - game_time
            sys.stdout.write("Time: {:.2f} seconds".format(elapsed_time))

    sys.stdout.flush()

def draw_highlighted_block(x, y):
    global left, top, check, visited

    for i in range(3):  # Vẽ 3 dòng
        gotoXY(left + x * 8 + 2, top + y * 4 + i + 1)
        sys.stdout.write("\033[47m" + " " * 7 + "\033[m")  # Tô màu cho toàn bộ ô
    
    sys.stdout.flush()

def draw_unhighlighted_block(x, y):
    global left, top, visited, icon

    if icon[x, y] == True:
        return
    
    for i in range(3):  # Vẽ 3 dòng
        gotoXY(left + x * 8 + 2, top + y * 4 + i + 1)
        sys.stdout.write(" " * 7)  # Không tô màu

    sys.stdout.flush()

def draw_highlighted_icon(x, y):
    global matches, answer_list, visited, icon
    
    index = x * y
    icon[x, y] = True 

    for i in range(3):
        gotoXY(left + x * 8 + 2, top + y * 4 + i + 1)
        if i == 1: 
            sys.stdout.write("\033[47m" + f"\033[31m{matches[index]: ^7}" + "\033[m")
        else:
            sys.stdout.write("\033[47m" + " " * 7 + "\033[m")  # Tô màu cho toàn bộ ô

    sys.stdout.flush()

def move(direction):
    global current_pos, size, check, visited, icon

    # Calculate the new position based on the direction
    new_pos = current_pos.copy()
    if direction == "left":
        if current_pos[0] > 0:
            new_pos[0] -= 1

        if current_pos[0] == 0:
            new_pos[0] = size - 1    

    elif direction == "right":
        if current_pos[0] < size - 1:
            new_pos[0] += 1
        if current_pos[0] == size - 1:
            new_pos[0] = 0

    elif direction == "up":
        if current_pos[1] > 0:
            new_pos[1] -= 1
        if current_pos[1] == 0:
            new_pos[1] = size - 1

    elif direction == "down":
        if current_pos[1] < size - 1:
            new_pos[1] += 1
        if current_pos[1] == size - 1:
            new_pos[1] = 0

    if new_pos != current_pos:
        if icon[new_pos[0], new_pos[1]] == True:
            draw_highlighted_icon(new_pos[0], new_pos[1])
            draw_unhighlighted_block(current_pos[0], current_pos[1])
            current_pos = new_pos
            return
        if check == True: 
            current_pos = new_pos
            draw_highlighted_block(current_pos[0], current_pos[1])
            check = False
        else:
            draw_unhighlighted_block(current_pos[0], current_pos[1])
            current_pos = new_pos
            draw_highlighted_block(current_pos[0], current_pos[1])

def saveGame():
    global score, player, game_time

    with open("Information.txt", "w") as F:
        F.write(f"Score: {score}\n")
        F.write(f"Player: {player}\n")
        F.write(f"Time: {game_time}\n")

def checkEnter():
    global check
    check = True

    x = current_pos[0]
    y = current_pos[1]

    index = x * y

    draw_unhighlighted_block(x, y)
    draw_highlighted_icon(x, y)

    answer_list.append(index) 

    if len(answer_list) == 1:
        first_block[0] = x
        first_block[1] = y
    
    if len(answer_list) == 2:
        second_block[0] = x
        second_block[1] = y
        checkCorrect()
 
def checkCorrect():
    global answer_list, first_block, second_block, left, top, countPair, visited, score

    if len(answer_list) == 2:   
        if matches[answer_list[0]] == matches[answer_list[1]]:
            icon[first_block[0], first_block[1]] = True
            icon[second_block[0], second_block[1]] = True
            countPair += 1
            score += 50
        else: 
            time.sleep(0.5)
            icon[first_block[0], first_block[1]] = False
            icon[second_block[0], second_block[1]] = False
            draw_unhighlighted_block(first_block[0], first_block[1])
            draw_unhighlighted_block(second_block[0], second_block[1])


    answer_list = []

def checkWin():
    global countPair
    if countPair * 2 == 36:
        gotoXY(58, 32)
        print("YOU WIN")
        return

def moveLoop():
    while True:
        checkWin()
        drawInforBoard()
        key = msvcrt.getch().decode('utf-8') # Don't print any key to console
        if key == "q":
            break
        elif key == "w":
            move("up")
        elif key == "s":
            move("down")
        elif key == "a":
            move("left")
        elif key == "d":
            move("right")
        elif key == "u":
            saveGame()
        elif key == "\r":
            checkEnter()

def startGame():
    # Test the drawGameBoard function
    drawGameBoard()
    drawInforBoard()
    Random()

    # Test the move function
    moveLoop()
    
gameMenu()