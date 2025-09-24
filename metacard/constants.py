# --- Configuration ---
from PIL import ImageFont

from pathlib import Path

IMG_WIDTH = 1200
IMG_HEIGHT = 630
BG_COLOR = "#1a1a1a" # A dark background color
AUTHOR_NAME = "Serhii Hrekov" # Your name!
AUTHOR_WEBSITE = "hrekov.com" # Your website URL
AUTHOR_FORNT_COLOR="#cccccc" # Light gray color for author text
FONT_SIZE = 60
FONT_COLOR = "#FFFFFF" # White color
FONT_FAMILY = "Poppins" # Default font family
CHAR_WIDTH_AVG = 35 # Average character width, adjust as needed

BASE_DIR = Path(__file__).resolve().parent

def load_font(path, size):
    try:
        return ImageFont.truetype(str(BASE_DIR / path), size)
    except IOError:
        print(f"Font {path} not found. Using default font.")
        return ImageFont.load_default()

try:
    TITLE_FONT = load_font("fonts/Poppins/Poppins-Bold.ttf", 60)
    AUTHOR_FONT = load_font("fonts/Poppins/Poppins-Regular.ttf", 40)
    AUTHOR_URL_FONT = load_font("fonts/Poppins/Poppins-Regular.ttf", 20)
except IOError:
    print("Font file not found. Please download Poppins from Google Fonts.")