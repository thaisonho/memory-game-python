import os
import time
import keyboard
from PIL import Image
from termcolor import colored
import numpy as np
from colorama import Fore, Style
import matplotlib.pyplot as plt
import ctypes
from ctypes import wintypes
from pathlib import Path
import msvcrt


TERM_WIDTH       = os.get_terminal_size().columns
TERM_HEIGHT      = os.get_terminal_size().lines
MENU_ART_LEN     = int(68)
MENU_WIDTH       = int(29)
MENU_HEIGHT      = int(6)
NEW_GAME_WIDTH   = 40
SCORE_WIDTH      = 30
GUIDE_WIDTH      = 24
QUIT_WIDTH       = 19
SCORE_BOARD_ART_WIDTH = 86

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
    assets_dir = Path(__file__).parent / "assets"
    show_image(str(assets_dir) + "/friend.jpg")
    print(GotoXY(50, 15) + 'NAME')

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

def filled_rec(x_pos, y_pos, height, width, r, g, b):
    changeTextColor(r, g, b)
    for ix in range(x_pos, x_pos + width + 1):
        for iy in range(y_pos, y_pos + height + 1):
            print(GotoXY(ix, iy) + u'\u2588')
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

    printArtAtPos((TERM_WIDTH - SCORE_BOARD_ART_WIDTH) // 2, 1, score_bo)

    filled_rec(x_menu, y_menu, height, width, 247, 183, 135)
    changeTextColor(245, 245, 245, 247, 183, 135)
    print(GotoXY(x_menu + 8, y_menu) + "<EMPTY>")
    changeTextColor()
    for i in range(2, 8):
        print(GotoXY(x_menu + 8, (y_menu + distance * (i - 1))) + "<EMPTY>")
    changeTextColor()

    while not isESC:
        key = msvcrt.getch().decode('utf-8')
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
            filled_rec(x_menu, y_menu, height, width, 247, 183, 135)
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
        key = msvcrt.getch().decode('utf-8')
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

def gameMenu():
    x_banner = (TERM_WIDTH - MENU_ART_LEN) // 2
    while True:
        os.system("cls")
        changeTextColor(255, 209, 227)
        printListAtPos(x_banner, 1, gradientText(menu_banner, 91, 188, 255, 255, 209, 227))
        user_choice = userChoice_v2()
        if user_choice == 1:
            # startGame()
            print("start game")
        if user_choice == 2:
            score_board()
        if user_choice == 3:
            # Guide()
            print("guide")
        if user_choice == 4:
            # Exit
            break;

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

def FixConsole():
    set_console_position(110,100)
    #lock_console_position()
    disable_resize_window()
    show_scrollbar()

#----------------------------------------------------#
FixConsole()
gameMenu()
# game_match()