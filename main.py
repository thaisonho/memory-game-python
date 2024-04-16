import os
import time
import test
from PIL import Image
from termcolor import colored
import numpy as np
from colorama import Fore, Style
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


TERM_WIDTH   = os.get_terminal_size().columns
TERM_HEIGHT  = os.get_terminal_size().lines
MENU_ART_LEN = int(68)
MENU_WIDTH   = int(29)
MENU_HEIGHT  = int(6)


def GotoXY(x, y) -> str:
    res = "\x1b[{};{}f".format(y, x)
    return res

def get_ansi_color_code(r, g, b):
    return round((r / 255) * 5) * 36 + round((g / 255) * 5) * 6 + round((b / 255) * 5) + 16

def get_color(r, g, b):
    return "\x1b[48;5;{}m \x1b[0m".format(get_ansi_color_code(r, g, b))

def show_image(img_path):
    try:
        img = Image.open(img_path)
    except FileNotFoundError:
        exit('Image not found.')
    newHeight = 30
    newWidth = 120
    img = img.resize((newWidth, newHeight), Image.LANCZOS)
    img_arr = np.asarray(img)

    for x in range(newHeight):
        for y in range(newWidth):
            pix = img_arr[x][y]
            print(get_color(pix[0], pix[1], pix[2]), end='')
        print()


def game_match():
    show_image("assets/friend.jpg")
    GotoXY(50, 15)
    print('NAME')


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
        # startGame()
        print("start game")
    if user_choice == 2:
        # Scores()
        print("scores")
    if user_choice == 3:
        # Guide()
        print("guide")
    if user_choice == 4:
        # Exit
        return

#hello
#gameMenu()
    

game_match()