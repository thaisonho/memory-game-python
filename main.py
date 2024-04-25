import sys
import os
import msvcrt
import random 
import time
import threading
import keyboard
from termcolor import colored
from colorama import init, Fore, Back, Style
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import ctypes
from ctypes import wintypes
from pathlib import Path
import msvcrt

# Global variables

left = 35
top = 4
size = 6
countPair = 0
score = 0
timer = "00:00:00"
check = False
timing = True
elapsed_time = 0
time_thread = threading.Thread()
player = "Player 1"
player_snake = {}
id = 0
name_player = ""

current_pos = [0, 1]  # Initial position (0, 0)
visited = [False] * (size + 1) * (size + 1) # explanation
icon = np.zeros((7, 7))

answer_list = []
matches = []

first_block = [0, 0]
second_block = [0, 0]
# Global variables

left = 35
top = 4
size = 6
countPair = 0
score = 0
timer = 0
check = False
timing = True
time_thread = threading.Thread()
player = "Player 1"
player_snake = {}
id = 0
name_player = ""

current_pos = [0, 1]  # Initial position (0, 0)
visited = [False] * (size + 1) * (size + 1) # explanation
icon = np.zeros((7, 7))

answer_list = []
matches = []

first_block = [0, 0]
second_block = [0, 0]

TERM_WIDTH       = os.get_terminal_size().columns
TERM_HEIGHT      = os.get_terminal_size().lines
MENU_ART_LEN     = int(68)
MENU_WIDTH       = int(29)
MENU_HEIGHT      = int(6)
NEW_GAME_WIDTH   = 40
SCORE_WIDTH      = 30
GUIDE_WIDTH      = 24
QUIT_WIDTH       = 19
SCORE_BOARD_WIDTH = 86

menu_banner = R'''
• ▌ ▄ ·. ▄▄▄ .• ▌ ▄ ·.       ▄▄▄   ▄· ▄▌   ▄▄ •  ▄▄▄· • ▌ ▄ ·. ▄▄▄ .
·██ ▐███▪▀▄.▀··██ ▐███▪ ▄█▀▄ ▀▄ █·▐█▪██▌  ▐█ ▀ ▪▐█ ▀█ ·██ ▐███▪▀▄.▀·
▐█ ▌▐▌▐█·▐▀▀▪▄▐█ ▌▐▌▐█·▐█▌.▐▌▐▀▀▄ ▐█▌▐█▪  ▄█ ▀█▄▄█▀▀█ ▐█ ▌▐▌▐█·▐▀▀▪▄
██ ██▌▐█▌▐█▄▄▌██ ██▌▐█▌▐█▌.▐▌▐█•█▌ ▐█▀·.  ▐█▄▪▐█▐█▪ ▐▌██ ██▌▐█▌▐█▄▄▌
▀▀  █▪▀▀▀ ▀▀▀ ▀▀  █▪▀▀▀ ▀█▄▀▪.▀  ▀  ▀ •   ·▀▀▀▀  ▀  ▀ ▀▀  █▪▀▀▀ ▀▀▀ 
'''

new_game_banner = """▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
██ ▀██ █ ▄▄█ ███ ███ ▄▄▄█ ▄▄▀█ ▄▀▄ █ ▄▄█
██ █ █ █ ▄▄█▄▀ ▀▄███ █▄▀█ ▀▀ █ █▄█ █ ▄▄█
██ ██▄ █▄▄▄██▄█▄████▄▄▄▄█▄██▄█▄███▄█▄▄▄█
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
"""

scores_banner = """▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
██ ▄▄▄ █▀▄▀█▀▄▄▀█ ▄▄▀█ ▄▄█ ▄▄█
██▄▄▄▀▀█ █▀█ ██ █ ▀▀▄█ ▄▄█▄▄▀█
██ ▀▀▀ ██▄███▄▄██▄█▄▄█▄▄▄█▄▄▄█
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
"""

guide_banner = """▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
██ ▄▄ █ ██ ██▄██ ▄▀█ ▄▄█
██ █▀▀█ ██ ██ ▄█ █ █ ▄▄█
██ ▀▀▄██▄▄▄█▄▄▄█▄▄██▄▄▄█
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
"""

quit_banner = """▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
█ ▄▄ █ ██ ██▄██▄ ▄█
█ ▀▀ █ ██ ██ ▄██ ██
████ ██▄▄▄█▄▄▄██▄██
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
"""

score_bo = R'''
███████╗ ██████╗ ██████╗ ██████╗ ███████╗    ██████╗  ██████╗  █████╗ ██████╗ ██████╗ 
██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔════╝    ██╔══██╗██╔═══██╗██╔══██╗██╔══██╗██╔══██╗
███████╗██║     ██║   ██║██████╔╝█████╗      ██████╔╝██║   ██║███████║██████╔╝██║  ██║
╚════██║██║     ██║   ██║██╔══██╗██╔══╝      ██╔══██╗██║   ██║██╔══██║██╔══██╗██║  ██║
███████║╚██████╗╚██████╔╝██║  ██║███████╗    ██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝
╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝    ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ 
'''

guideline_art = """
 ██████╗ ██╗   ██╗██╗██████╗ ███████╗██╗     ██╗███╗   ██╗███████╗
██╔════╝ ██║   ██║██║██╔══██╗██╔════╝██║     ██║████╗  ██║██╔════╝
██║  ███╗██║   ██║██║██║  ██║█████╗  ██║     ██║██╔██╗ ██║█████╗  
██║   ██║██║   ██║██║██║  ██║██╔══╝  ██║     ██║██║╚██╗██║██╔══╝  
╚██████╔╝╚██████╔╝██║██████╔╝███████╗███████╗██║██║ ╚████║███████╗
 ╚═════╝  ╚═════╝ ╚═╝╚═════╝ ╚══════╝╚══════╝╚═╝╚═╝  ╚═══╝╚══════╝
 """

def GotoXY(x, y) -> str:
    res = "\x1b[{};{}f".format(y, x)
    return res

def get_ansi_color_code(r, g, b):
    if r == g == b:
        if r < 8:
            return 16
        if r > 248:
            return 231
        return round(((r - 8) / 247) * 24) + 232
    return 16 + (36 * round(r / 255 * 5)) + (6 * round(g / 255 * 5)) + round(b / 255 * 5)

def get_color(r, g, b):
    return "\x1b[48;5;{}m \x1b[0m".format(int(get_ansi_color_code(r,g,b)))

def show_image(img_path):
    try:
        img = Image.open(img_path)
    except FileNotFoundError:
        exit('Image not found.')
    h = 30
    w = 120
    img = img.resize((w, h), Image.LANCZOS)
    img_arr = np.asarray(img)

    for x in range(0, h):
        for y in range(0, w):
            pix = img_arr[x][y]
            print(get_color(pix[0], pix[1], pix[2]), sep='', end='')
        print()


def game_match():
    gotoXY(0, 0)
    init(autoreset=True)
    assets_dir = Path(__file__).parent / "assets"
    show_image(str(assets_dir) + "/friend.jpg")
    filled_rec(left + 1, top, 24, 48, 0, 0, 0, 0, 0, 0)

# without any args: reset color
# with 3 args: red, green, blue for foreground
# with 6 args: rgb for foreground & background
def changeTextColor(*args):
    if len(args) == 0:
        print("\x1b[0m", end='')
    if len(args) == 3:
        print("\x1b[38;2;{};{};{}m".format(args[0], args[1], args[2]), end='')
    if len(args) == 6:
        print("\x1b[38;2;{};{};{};48;2;{};{};{}m".format(args[0], args[1], args[2], args[3], args[4], args[5]), end='')

def GotoXY(x, y) -> str:
    res = "\x1b[{};{}f".format(y, x)
    return res

def printArtAtPos(x, y, art):
    art_lines = art.split('\n')
    for lines in art_lines:
        print(GotoXY(x, y) + lines)
        y += 1

def filled_rec(x_pos, y_pos, height, width, f_r, f_g, f_b, b_r, b_g, b_b):
    changeTextColor(f_r, f_g, f_b, b_r, b_g, b_b)
    for ix in range(x_pos, x_pos + width + 1):
        for iy in range(y_pos, y_pos + height + 1):
            print(GotoXY(ix, iy) + " ")
    changeTextColor()


def filled_rec_with_text(x_pos, y_pos, height, width, r, g, b, text, r_t, g_t, b_t):
    filled_rec(x_pos, y_pos, height, width, r, g, b)
    changeTextColor(r_t, g_t, b_t)
    text_x = x_pos + (width - len(text)) // 2
    text_y = y_pos + height // 2
    print(GotoXY(text_x, text_y) + text)
    changeTextColor()


def delete_rec(x_pos, y_pos, height, width):
    for ix in range(x_pos, x_pos + width + 1):
        for iy in range(y_pos, y_pos + height + 1):
            print(GotoXY(ix, iy) + " ")
    changeTextColor()


def score_board():
    os.system('cls')
    x_menu = (TERM_WIDTH - 80) // 2
    y_menu = 10
    y_prev: int
    height = 0
    distance = 2
    width = 80
    isESC = False
    check = False

    printArtAtPos((TERM_WIDTH - SCORE_BOARD_WIDTH) // 2, 1, score_bo)

    filled_rec(x_menu, y_menu, height, width, 0, 0, 0, 247, 183, 135)
    changeTextColor(245, 245, 245, 247, 183, 135)
    print(GotoXY(x_menu + 8, y_menu) + "<EMPTY>")
    changeTextColor()
    for i in range(2, 8):
        print(GotoXY(x_menu + 8, (y_menu + distance * (i - 1))) + "<EMPTY>")
    changeTextColor()

    while not isESC:
        key = get_input() 
        if key == 's':
            check = True
            y_prev = y_menu
            y_menu += distance
            if (y_menu > 10 + 6 * 2):
                y_menu = 10

        if key == 'w':
            check = True
            y_prev = y_menu
            y_menu -= distance
            if (y_menu < 10):
                y_menu = 10 + 6 * 2

        if keyboard.is_pressed('esc'):
            isESC = True
            # go to MENU
        if check == True:
            delete_rec(x_menu, y_prev, height, width)
            print(GotoXY(x_menu + 8, y_prev) + "<EMPTY>")
            y_prev = y_menu
            filled_rec(x_menu, y_menu, height, width, 0, 0, 0, 247, 183, 135)
            changeTextColor(245, 245, 245, 247, 183, 135)
            print(GotoXY(x_menu + 8, y_menu) + "<EMPTY>")
            changeTextColor()
            check = False

        time.sleep(0.05)

def gradientText(text, r_from, g_from, b_from, r_to, g_to, b_to):
    res = []
    for line in text.splitlines():
        red = r_from
        green = g_from
        blue = b_from
        res_line = ""
        for char in line:
            red += (r_to - r_from) / len(line)
            green += (g_to - g_from) / len(line)
            blue += (b_to - b_from) / len(line)
            res_line += (f"\x1b[38;2;{round(red)};{round(green)};{round(blue)}m{char}\x1b[0m")
        res.append(res_line)

    return res

def printListAtPos(x_pos, y_pos, _src):
    for line in _src:
        print(GotoXY(x_pos, y_pos) + line)
        y_pos += 1

def printSpace(x_pos, y_pos, lines, cols):
    for i in range(0, lines):
        print(GotoXY(x_pos, y_pos) + cols * ' ')
        y_pos += 1

def userChoice_v2():
    choice = 1
    check = False
    prev_choice: int

    print(GotoXY(TERM_WIDTH // 2, 8) + '˄')
    print(GotoXY(TERM_WIDTH // 2, 14) + '˅')

    new_game_gradient = gradientText(new_game_banner, 255, 209, 227, 255, 250, 183)
    score_gradient = gradientText(scores_banner, 255, 209, 227, 255, 250, 183)
    guide_gradient = gradientText(guide_banner, 255, 209, 227, 255, 250, 183)
    quit_gradient = gradientText(quit_banner, 255, 209, 227, 255, 250, 183)

    printListAtPos((TERM_WIDTH - NEW_GAME_WIDTH) // 2, 9, new_game_gradient)

    while True:
        key = get_input()
        if keyboard.is_pressed('w'):
            prev_choice = choice
            choice -= 1
            if choice < 1:
                choice = 4
            check = True
            
        if keyboard.is_pressed('s'):
            prev_choice = choice
            choice += 1
            if choice > 4:
                choice = 1
            check = True

        if keyboard.is_pressed('enter'):
            break
        
        if check == True:
            if prev_choice == 1:
                printSpace((TERM_WIDTH - NEW_GAME_WIDTH) // 2, 9, 5, NEW_GAME_WIDTH)
            elif prev_choice == 2:
                printSpace((TERM_WIDTH - SCORE_WIDTH) // 2, 9, 5, SCORE_WIDTH)
            elif prev_choice == 3:
                printSpace((TERM_WIDTH - GUIDE_WIDTH) // 2, 9, 5, GUIDE_WIDTH)
            elif prev_choice == 4:
                printSpace((TERM_WIDTH - QUIT_WIDTH) // 2, 9, 5, QUIT_WIDTH)
            time.sleep(0.05)
            if choice == 1:
                printListAtPos((TERM_WIDTH - NEW_GAME_WIDTH) // 2, 9, new_game_gradient)
            elif choice == 2:
                printListAtPos((TERM_WIDTH - SCORE_WIDTH) // 2, 9, score_gradient)
            elif choice == 3:
                printListAtPos((TERM_WIDTH - GUIDE_WIDTH) // 2, 9, guide_gradient)
            elif choice == 4:
                printListAtPos((TERM_WIDTH - QUIT_WIDTH) // 2, 9, quit_gradient)
            check = False
    return choice


# {---------------LOGIC GAME-----------------}

def Random():
    global matches

    for i in range(0, 18):
        matches.append(i + 1)
        matches.append(i + 1)

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
    global left, top, size, score, player, timer
      
    for i in range(4):
        gotoXY(left + size * 8 + 9, top + i * 4 + 3)

        changeTextColor(207, 235, 199)
        if i == 1:
            print("Player: {}".format(player))
        elif i == 2:
            print("Score: {}".format(score))
        elif i == 3:
            print("Time: {}".format(timer))
        #changeTextColor()

    #sys.stdout.flush()

def change_Terminal_background_color(r, g, b):
    color_code = get_ansi_color_code(r, g, b)
    print(f"Generated ANSI color code: {color_code}")
    
    # Construct ANSI escape sequence to set background color
    escape_sequence = f"\033[48;5;{color_code}m"
    
    # Send escape sequence to stdout to set background color
    os.sys.stdout.write(escape_sequence)
    os.sys.stdout.flush()
    
    # Move cursor to top-left corner of the screen
    os.system("printf '\033[H'")

def display_timer(seconds):
    global timer
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    timer = "{:02d}:{:02d}:{:02d}".format(int(hours), int(minutes), int(seconds))
    #print("\rThời gian: ", timer, end="")

def count_timer():
    global timing, elapsed_time
    start_time = time.time()
    while timing:
        current_time = time.time()
        elapsed_time = current_time - start_time
        display_timer(elapsed_time)
        time.sleep(1)  # Delay 1 second

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

def draw_highlighted_number(x, y):
    global matches, answer_list, visited, icon
    
    index = 6 * x + y
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
            draw_highlighted_number(new_pos[0], new_pos[1])
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
    global score, player

    with open("Information.txt", "w") as F:
        F.write(f"Score: {score}\n")
        F.write(f"Player: {player}\n")

def checkEnter():
    global check
    check = True

    x = current_pos[0]
    y = current_pos[1]

    index = (6 * y) + x 

    draw_unhighlighted_block(x, y)
    draw_highlighted_number(x, y)

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

def get_input():
    try:
        key = msvcrt.getch().decode('utf-8') # W, S, A, D, U, Enter
        return key
    except UnicodeDecodeError: # Avoid press another key 
        return None
    
def moveLoop():
    global timing

    while timing == True:
        checkWin()
        drawInforBoard()
        key = get_input() # Don't print any key to console
        if key == "w":
            move("up")
        elif key == "s":
            move("down")
        elif key == "a":
            move("left")
        elif key == "d":
            move("right")
        elif key == "u":
            timing = False
            saveGame() 
            break 
        elif key == "\r":
            checkEnter()
        else:
            pass
            
def startGame():
    # Test the drawGameBoard function
    new_game(player_snake, id, name_player)
    game_match()
    global timing
    timing = True
    # Tạo luồng cho đồng hồ đếm thời gian
    timer_thread = threading.Thread(target=count_timer)
    # Bắt đầu chạy luồng đồng hồ đếm thời gian
    timer_thread.start()
    # Đợi cho luồng đồng hồ đếm thời gian hoàn thành

    Random()

    drawGameBoard()
    #drawInforBoard()

    # Test the move function
    moveLoop()
    
def set_console_position(x, y):
    # Get the handle of the console window
    console_window = ctypes.windll.kernel32.GetConsoleWindow()
    # Set the position of the console window
    SWP_NOSIZE = 0x0001
    SWP_NOZORDER = 0x0004
    ctypes.windll.user32.SetWindowPos(console_window, 0, x, y, 0, 0, SWP_NOSIZE | SWP_NOZORDER)

def lock_console_position():
    # Get the handle of the console window
    console_window = ctypes.windll.kernel32.GetConsoleWindow()

    # Get the window style
    GWL_STYLE = -16
    window_style = ctypes.windll.user32.GetWindowLongPtrW(console_window, GWL_STYLE)

    # Remove the WS_CAPTION flag from the window style
    WS_CAPTION = 0x00C00000
    window_style = ctypes.wintypes.LONG(window_style & ~WS_CAPTION)

    # Set the modified window style
    ctypes.windll.user32.SetWindowLongPtrW(console_window, GWL_STYLE, window_style)

    # Update the window size and appearance
    SWP_NOSIZE = 0x0001
    SWP_NOMOVE = 0x0002
    SWP_FRAMECHANGED = 0x0020
    ctypes.windll.user32.SetWindowPos(console_window, None, 0, 0, 0, 0, SWP_NOSIZE | SWP_NOMOVE | SWP_FRAMECHANGED)

def disable_resize_window():
    # Get the handle of the console window
    console_window = ctypes.windll.kernel32.GetConsoleWindow()

    # Disable the resizing of the console window
    GWL_STYLE = -16
    WS_SIZEBOX = 0x00040000
    window_style = ctypes.windll.user32.GetWindowLongW(console_window, GWL_STYLE)
    window_style = ctypes.wintypes.LONG(window_style & ~WS_SIZEBOX)
    ctypes.windll.user32.SetWindowLongW(console_window, GWL_STYLE, window_style)

def show_scrollbar():
    # Get the handle of the console window
    console_window = ctypes.windll.kernel32.GetConsoleWindow()

    # Show or hide the scrollbars
    SB_BOTH = 3
    ShowScrollBar = ctypes.windll.user32.ShowScrollBar
    ShowScrollBar(console_window, SB_BOTH, False)

def set_window_size(width, height):
    kernel32 = ctypes.windll.kernel32
    hStdout = kernel32.GetStdHandle(-11)  
    rect = ctypes.wintypes.SMALL_RECT(0, 0, width - 1, height - 1)
    kernel32.SetConsoleWindowInfo(hStdout, True, ctypes.byref(rect))
    
def set_screen_buffer_size(width, height):
    kernel32 = ctypes.windll.kernel32
    hStdout = kernel32.GetStdHandle(-11)  
    coord = ctypes.wintypes._COORD(width, height)
    kernel32.SetConsoleScreenBufferSize(hStdout, coord)

# {---------------------Name Player-----------------------}
def is_valid_name(player_snake, id, st):
    for i in range(1, id + 1):
        if st == player_snake[i].name:
            return False
    return True

def not_valid():
    print("This name is not valid. Please enter the name again!!!")

def refill():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console

    print(" " * 58)  # Clear the line at row 14
    print(" " * 24, end="")  # Clear the line at row 12

def user_name():
    init(autoreset=True)
    show_image("assets/user.jpg")

def new_game(player_snake, id, name_player):
    os.system('cls' if os.name == 'nt' else 'clear')

    user_name()

    gotoXY(58, 15)
    print("NAME PLAYER: ", end="")
    name_player = input()

    while True:
        if is_valid_name(player_snake, id, name_player) and len(name_player) <= 10 and name_player != "":
            break

        not_valid()
        time.sleep(1.5)
        refill()
        
        gotoXY(58, 15)
        print("NAME PLAYER: ", end="")
        name_player = input()

    id += 1

def guideline():
    filled_rec(0, 0, 30, 120, 0, 0, 0, 126, 233, 208)

    #printArtAtPos(40, 1, guideline_art)

    # draw guideline
    changeTextColor(0, 0, 0, 126, 233, 208)
    print(GotoXY(28, 9) + "GUIDELINE")
    print(GotoXY(10, 11) + "Trò chơi bao gồm 1 bàn chơi 6x6, đầu tiên các")
    print(GotoXY(10, 13) + "lá bài sẽ được úp xuống, mỗi lá bài sẽ giữ cho")
    print(GotoXY(10, 15) + "mình một con số riêng của mình. Ở mỗi lượt chơi,")
    print(GotoXY(10, 17) + "người chơi sẽ chọn LẦN LƯỢT 2 lá bài khác nhau")
    print(GotoXY(10, 19) + "trên bàn chơi, trò chơi sẽ kết thúc khi các lá ")
    print(GotoXY(10, 21) + "bài đều được mở.")
 

    # draw button
    print(GotoXY(85, 9) + "BUTTON")
    filled_rec(75, 11, 1, 4, 0, 0, 0, 245, 245, 245)
    changeTextColor(0, 0, 0, 245, 245, 245)
    print(GotoXY(76, 12) + "W")
    changeTextColor(0, 0, 0, 126, 233, 208)
    print(GotoXY(90, 12) + "Move Right")

    filled_rec(75, 14, 1, 4, 0, 0, 0, 245, 245, 245)
    changeTextColor(0, 0, 0, 245, 245, 245)
    print(GotoXY(76, 15) + "A")
    changeTextColor(0, 0, 0, 126, 233, 208)
    print(GotoXY(90, 15) + "Move Left")

    filled_rec(75, 17, 1, 4, 0, 0, 0, 245, 245, 245)
    changeTextColor(0, 0, 0, 245, 245, 245)
    print(GotoXY(76, 18) + "S")
    changeTextColor(0, 0, 0, 126, 233, 208)
    print(GotoXY(90, 18) + "Move Down")

    filled_rec(75, 20, 1, 4, 0, 0, 0, 245, 245, 245)
    changeTextColor(0, 0, 0, 245, 245, 245)
    print(GotoXY(76, 21) + "D")
    changeTextColor(0, 0, 0, 126, 233, 208)
    print(GotoXY(90, 21) + "Move Left")

    filled_rec(75, 23, 1, 4, 0, 0, 0, 245, 245, 245)
    changeTextColor(0, 0, 0, 245, 245, 245)
    print(GotoXY(76, 24) + "U")
    changeTextColor(0, 0, 0, 126, 233, 208)
    print(GotoXY(90, 24) + "Save Game")
    changeTextColor()
    os.system("pause")
    for i in range(1, 31):
        print(" " * 120)
#----------------------------------------------------#
def gameMenu():
    os.system("cls")
    changeTextColor(255, 209, 227)
    x_banner = (TERM_WIDTH - MENU_ART_LEN) // 2
    while True:
        os.system("cls")
        changeTextColor(255, 209, 227)
        printListAtPos(x_banner, 1, gradientText(menu_banner, 91, 188, 255, 255, 209, 227))
        user_choice = userChoice_v2()
        if user_choice == 1:
            os.system("cls")
            startGame()
        if user_choice == 2:
            score_board()
        if user_choice == 3:
            guideline()
        if user_choice == 4:
            # Exit
            break;

def FixConsole():
    set_window_size(120,30)
    set_screen_buffer_size(120,30)
    set_console_position(110,100)
    lock_console_position()
    disable_resize_window()
    show_scrollbar()

FixConsole()
#winsound.PlaySound("music.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)

gameMenu()