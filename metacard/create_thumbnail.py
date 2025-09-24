from PIL import Image, ImageDraw, ImageFont
import io 
from pathlib import Path
from . import constants


    


def generate_image(
        title: str,
        footer: bool = False,
        backgroundColor: str = constants.BG_COLOR,
        fontSize: int = constants.FONT_SIZE,
        fontColor: str = constants.FONT_COLOR,
        authorFontColor: str = constants.AUTHOR_FORNT_COLOR,
        authorName: str = constants.AUTHOR_NAME,
        authorWebsite: str = constants.AUTHOR_WEBSITE,
        authorFontSize: int = 40,
        authorWebsiteFontSize: int = 20,
          ) -> bytes:
    """
    Generates a social media thumbnail image for a blog post with a customizable title, background color, font styles, and optional footer containing author information.
        Args:
            title (str): The main text to display as the thumbnail's title.
            footer (bool, optional): Whether to include author information at the bottom of the image. Defaults to False.
            backgroundColor (str, optional): Background color of the image. Defaults to constants.BG_COLOR.
            fontSize (int, optional): Font size for the title text. Defaults to constants.FONT_SIZE.
            fontColor (str, optional): Color of the title text. Defaults to constants.FONT_COLOR.
            authorFontColor (str, optional): Color of the author information text. Defaults to constants.AUTHOR_FORNT_COLOR.
            authorName (str, optional): Name of the author to display in the footer. Defaults to constants.AUTHOR_NAME.
            authorWebsite (str, optional): Website of the author to display in the footer. Defaults to constants.AUTHOR_WEBSITE.
            authorFontSize (int, optional): Font size for the author name. Defaults to 40.
            authorWebsiteFontSize (int, optional): Font size for the author website. Defaults to 20.
        Returns:
            bytes: The generated thumbnail image in PNG format as a bytes object.
    """
    # 1. Create a blank image
    img = Image.new('RGB', (constants.IMG_WIDTH, constants.IMG_HEIGHT), color=backgroundColor)
    draw = ImageDraw.Draw(img)


    # 3. Simple text wrapping for the title
    # This is a basic implementation to handle longer titles

    max_chars_per_line = constants.IMG_WIDTH // constants.CHAR_WIDTH_AVG
    
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
    current_y = (constants.IMG_HEIGHT - total_text_height) / 2

    # Draw title lines
    for line in lines:
        draw.text((constants.IMG_WIDTH / 2, current_y), line, font=constants.load_font("fonts/Poppins/Poppins-Bold.ttf", fontSize), fill=fontColor, anchor="ms")
        current_y += 70 # Move to the next line

    if footer:
        # Draw author name
        current_y += 20 # Add a little space before the author
        draw.text((constants.IMG_WIDTH / 2, current_y), f"By {authorName}", font=constants.load_font("fonts/Poppins/Poppins-Regular.ttf", authorFontSize), fill=authorFontColor, anchor="ms")
        # Draw author domain
        current_y += 40 # Add a little space before the author
        draw.text((constants.IMG_WIDTH / 2, current_y), f"{authorWebsite}", font=constants.load_font("fonts/Poppins/Poppins-Regular.ttf", authorWebsiteFontSize), fill=authorFontColor, anchor="ms")

    # 5. Save the image
    # img.save(output_path)
    # print(f"Image saved to {output_path}")

     # 5. Save the image to an in-memory buffer
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0) # Rewind the buffer to the beginning

    return buffer.getvalue()

# --- Run the script ---
if __name__ == "__main__":
    # Test it with one of your blog post titles!
    example_title = "How to Run Celery Beat in a Docker Container for Django"
    generate_image(title=example_title, output_path="my_first_thumbnail.png")