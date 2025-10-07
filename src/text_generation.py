from PIL import Image, ImageDraw, ImageFont
import hashlib
import os
import time


# Texts
def generate_text(text: str, 
                  font_name: str = 'morninggloryandcyrillic.otf', 
                  backgroud_name: str = 'empty_background.jpg',
                  output_dir: str = 'image_outputs',
                  font_size: int = 112, 
                  text_color: tuple[int, int, int] = (200, 29, 156),
                  ) -> str:
    """
    Generate specified text with empty background. 
    font_name is the name of a font file located in the working directory or in C\\Windows\\Fonts.
    """
    # empty background
    image = Image.open(backgroud_name)
    image = image.convert('RGB')

    # Initialize drawing context
    draw = ImageDraw.Draw(image)

    # Configure text properties
    font = ImageFont.truetype(font_name, font_size)  # load Cyrillic-capable font

    # Calculate text position (centered)
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (image.width - text_width) / 2
    y = (image.height - text_height) / 2

    # Draw text on image
    draw.text((x, y), text, fill=text_color, font=font)

    # Save the image
    time_str = str(time.time_ns())
    file_name = hashlib.md5(time_str.encode()).hexdigest()
    file_path = os.path.join(output_dir, str(file_name) + '.png')
    image.save(file_path)

    return file_path

generate_text('Hello world')