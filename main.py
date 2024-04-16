import os
import time
import test
from PIL import Image
from termcolor import colored
import numpy as np
from colorama import Fore, Style
import matplotlib.pyplot as plt

import winsound
import threading
import ctypes
from ctypes import wintypes

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
    lock_console_position()
    disable_resize_window()
    show_scrollbar()

def display_timer(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    timer = "{:02d}:{:02d}:{:02d}".format(int(hours), int(minutes), int(seconds))
    print("\rThời gian: ", timer, end="")

def count_timer():
    start_time = time.time()
    while timing:
        current_time = time.time()
        elapsed_time = current_time - start_time
        display_timer(elapsed_time)
        time.sleep(1)  # Delay 1 second


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
#----------------------------------------------------#
FixConsole()
# #winsound.PlaySound("music.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
# timing = True
# # Tạo luồng cho đồng hồ đếm thời gian
# timer_thread = threading.Thread(target=count_timer)
# # Bắt đầu chạy luồng đồng hồ đếm thời gian
# timer_thread.start()
# gameMenu()
# # Đợi cho luồng đồng hồ đếm thời gian hoàn thành
# timer_thread.join()
gameMenu()
