from PIL import Image
from termcolor import colored

# Load the image
image_path = "google.jpg"
img = Image.open(image_path)

# Resize the image to fit the console width
aspect_ratio = img.width / img.height
new_width = 120  # Adjust this value according to your console width
new_height = 30  # Adjust the multiplier for height
img_resized = img.resize((new_width, new_height))

# Convert the image to ASCII art
ascii_art = img_resized.convert("L")

# Define color mapping
def get_color(ascii_value):
    # Map ASCII value to color
    if ascii_value < 50:
        return "white"  # Adjust colors as needed
    elif ascii_value < 200:
        return "cyan"
    elif ascii_value < 300:
        return "blue"
    elif ascii_value < 100:
        return "red"
    else:
        return "white"

# Create colored ASCII art
colored_ascii_art = ""
for y in range(new_height):
    for x in range(new_width):
        # Get ASCII value of pixel
        ascii_value = ascii_art.getpixel((x, y))
        # Get corresponding color
        color = get_color(ascii_value)
        # Add colored character to ASCII art
        colored_ascii_art += colored("█", color)  # Use "█" as a full block character
    colored_ascii_art += "\n"  # Newline after each row

# Print the colored ASCII art
print(colored_ascii_art)

