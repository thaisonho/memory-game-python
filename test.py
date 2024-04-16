from PIL import Image
from termcolor import colored
import numpy as np
from colorama import Fore, Style
import matplotlib.pyplot as plt

# Define function to convert RGB to ANSI escape sequence
def rgb_to_ansi(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"



custom_colors = {
    "red": (255, 0, 0),                    # Red
    "green": (0, 255, 0),                  # Green
    "blue": (0, 0, 255),                   # Blue
    "electric lime": (168, 255, 4),        # Electric Lime
    "fresh green": (105, 216, 79),         # Fresh Green
    "light eggplant": (137, 69, 133),      # Light Eggplant
    "nasty green": (112, 178, 63),         # Nasty Green
    "really light blue": (212, 255, 255),  # Really Light Blue
    "tea": (101, 171, 124),                # Tea
    "warm purple": (149, 46, 143),         # Warm Purple
    "yellowish tan": (252, 252, 129),      # Yellowish Tan
    "cement": (165, 163, 145),             # Cement
    "dark grass green": (56, 128, 4),      # Dark Grass Green
    "dusty teal": (76, 144, 133),          # Dusty Teal
    "grey teal": (94, 155, 138),           # Grey Teal
    "macaroni and cheese": (239, 180, 53), # Macaroni and Cheese
    "pinkish tan": (217, 155, 130),        # Pinkish Tan
    "spruce": (10, 95, 56),                # Spruce
    "strong blue": (12, 6, 247),           # Strong Blue
    "toxic green": (97, 222, 42),          # Toxic Green
    "windows blue": (55, 120, 191),        # Windows Blue
    "blue blue": (34, 66, 199),            # Blue Blue
    "blue with a hint of purple": (83, 60, 198), # Blue with a Hint of Purple
    "booger": (155, 181, 60),              # Booger
    "bright sea green": (5, 255, 166),     # Bright Sea Green
    "dark green blue": (31, 99, 87),       # Dark Green Blue
    "deep turquoise": (1, 115, 116),       # Deep Turquoise
    "green teal": (12, 181, 119),          # Green Teal
    "strong pink": (255, 7, 137),          # Strong Pink
    "bland": (175, 168, 139),              # Bland
    "deep aqua": (8, 120, 127),            # Deep Aqua
    "lavender pink": (221, 133, 215),      # Lavender Pink
    "light moss green": (166, 200, 117),   # Light Moss Green
    "light seafoam green": (167, 255, 181),# Light Seafoam Green
    "olive yellow": (194, 183, 9),         # Olive Yellow
    "pig pink": (231, 142, 165),           # Pig Pink
    "deep lilac": (150, 110, 189),         # Deep Lilac
    "desert": (204, 173, 96),              # Desert
    "dusty lavender": (172, 134, 168),     # Dusty Lavender
    "purply grey": (148, 126, 148),        # Purply Grey
    "purply": (152, 63, 178),              # Purply
    "candy pink": (255, 99, 233),          # Candy Pink
    "light pastel green": (178, 251, 165), # Light Pastel Green
    "boring green": (99, 179, 101),        # Boring Green
    "kiwi green": (142, 229, 63),          # Kiwi Green
    "light grey green": (183, 225, 161),   # Light Grey Green
    "orange pink": (255, 111, 82),         # Orange Pink
    "tea green": (189, 248, 163),          # Tea Green
    "very light brown": (211, 182, 131),   # Very Light Brown
    "egg shell": (255, 252, 196),          # Egg Shell
    "eggplant purple": (67, 5, 65),        # Eggplant Purple
    "powder pink": (255, 178, 208),        # Powder Pink
    "reddish grey": (153, 117, 112),       # Reddish Grey
    "baby shit brown": (173, 144, 13),     # Baby Shit Brown
    "lilac": (196, 142, 253),              # Lilac
    "stormy blue": (80, 123, 156),         # Stormy Blue
    "ugly brown": (125, 113, 3),           # Ugly Brown
    "custard": (255, 253, 120),            # Custard
    "darkish pink": (218, 70, 125),        # Darkish Pink
    "deep brown": (65, 2, 0),              # Deep Brown
    "greenish beige": (201, 209, 121),     # Greenish Beige
    "manilla": (255, 250, 134),            # Manilla
    "off blue": (86, 132, 174),            # Off Blue
    "battleship grey": (107, 124, 133),    # Battleship Grey
    "browny green": (111, 108, 10),        # Browny Green
    "bruise": (126, 64, 113),              # Bruise
    "kelley green": (0, 147, 55),          # Kelley Green
    "sickly yellow": (208, 228, 41),       # Sickly Yellow
    "sunny yellow": (255, 249, 23),        # Sunny Yellow
    "azul": (29, 93, 236),                 # Azul
    "darkgreen": (5, 73, 7),               # Darkgreen
    "green/yellow": (181, 206, 8),         # Green/Yellow
    "lichen": (143, 182, 123),             # Lichen
    "light light green": (200, 255, 176),  # Light Light Green
    "pale gold": (253, 222, 108)
}

def generate_username(image_path):
    img = Image.open(image_path)

    new_width = 120 
    new_height = 30
    aspect_ratio = img.width / img.height
    img_resized = img.resize((new_width, new_height))

    ascii_art = img_resized.convert("L")

    # plt.imshow(ascii_art, cmap='gray')
    # plt.axis('off')  # Hide axis
    # plt.show()

    ansi_colors = {name: rgb_to_ansi(*rgb) for name, rgb in custom_colors.items()}

    def get_color(ascii_value):
        if ascii_value < 50:
            return ansi_colors["red"]
        elif ascii_value < 100:
            return Fore.CYAN
        elif ascii_value < 120:
            return ansi_colors["red"]
        elif ascii_value < 140:
            return ansi_colors["light grey green"]
        elif ascii_value < 200:
            return ansi_colors["pig pink"]
        else:
            return Fore.LIGHTBLUE_EX 
        
    colored_ascii_art = ""
    for y in range(new_height):
        for x in range(new_width):
            ascii_value = ascii_art.getpixel((x, y))
            color = get_color(ascii_value)
            colored_ascii_art += color + "█" + Style.RESET_ALL
        colored_ascii_art += "\n"

    return colored_ascii_art

def generate_gamematch(image_path):
    img = Image.open(image_path)

    new_width = 120 
    new_height = 30
    aspect_ratio = img.width / img.height
    img_resized = img.resize((new_width, new_height))

    ascii_art = img_resized.convert("L")

    plt.imshow(ascii_art, cmap='gray')
    plt.axis('off')  # Hide axis
    plt.show()

    ansi_colors = {name: rgb_to_ansi(*rgb) for name, rgb in custom_colors.items()}

    def get_color(ascii_value):
        if ascii_value < 140:
            return ansi_colors["light grey green"]
        #elif ascii_value < 195:
            #return ansi_colors["grey teal"]
        elif ascii_value < 220:
            return ansi_colors["pig pink"]
        #elif ascii_value < 220:
            #return ansi_colors["deep aqua"]
        else:
            return ansi_colors["light grey green"] 
        
    colored_ascii_art = ""
    for y in range(new_height):
        for x in range(new_width):
            ascii_value = ascii_art.getpixel((x, y))
            color = get_color(ascii_value)
            colored_ascii_art += color + "█" + Style.RESET_ALL
        colored_ascii_art += "\n"

    return colored_ascii_art

# Example usage:
image_path = "assets/friend.jpg"
username_art = generate_gamematch(image_path)
print(username_art)
