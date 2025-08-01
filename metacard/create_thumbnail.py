from PIL import Image, ImageDraw, ImageFont

# --- Configuration ---
IMG_WIDTH = 1200
IMG_HEIGHT = 630
BG_COLOR = "#1a1a1a" # A dark background color
AUTHOR_NAME = "Serhii Hrekov" # Your name!

def generate_image(title: str, output_path: str):
    """
    Generates a social media thumbnail for a blog post.
    """
    # 1. Create a blank image
    img = Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT), color=BG_COLOR)
    draw = ImageDraw.Draw(img)

    # 2. Load fonts
    # Make sure you have these .ttf font files in the same directory
    try:
        title_font = ImageFont.truetype("fonts/Poppins/Poppins-Bold.ttf", 60)
        author_font = ImageFont.truetype("fonts/Poppins/Poppins-Regular.ttf", 40)
    except IOError:
        print("Font file not found. Please download Poppins from Google Fonts.")
        return

    # 3. Simple text wrapping for the title
    # This is a basic implementation to handle longer titles
    char_width_avg = 35 # Average character width, adjust as needed
    max_chars_per_line = IMG_WIDTH // char_width_avg
    
    lines = []
    words = title.split()
    current_line = ""
    for word in words:
        if len(current_line + " " + word) < max_chars_per_line:
            current_line += " " + word
        else:
            lines.append(current_line.strip())
            current_line = word
    lines.append(current_line.strip())

    # 4. Draw the text on the image
    # Calculate starting Y position to center the block of text
    total_text_height = (len(lines) * 70) + 50 # (num_lines * line_height) + space for author
    current_y = (IMG_HEIGHT - total_text_height) / 2

    # Draw title lines
    for line in lines:
        draw.text((IMG_WIDTH / 2, current_y), line, font=title_font, fill="#FFFFFF", anchor="ms")
        current_y += 70 # Move to the next line

    # Draw author name
    current_y += 20 # Add a little space before the author
    draw.text((IMG_WIDTH / 2, current_y), f"By {AUTHOR_NAME}", font=author_font, fill="#cccccc", anchor="ms")
    
    # 5. Save the image
    img.save(output_path)
    print(f"Image saved to {output_path}")


# --- Run the script ---
if __name__ == "__main__":
    # Test it with one of your blog post titles!
    example_title = "How to Run Celery Beat in a Docker Container for Django"
    generate_image(title=example_title, output_path="my_first_thumbnail.png")