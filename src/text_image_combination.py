import replicate
import time
import os
import hashlib

COMBINATION_PROMPT = "Add an inscription from the second image to the top or to the bottom of the first image. Do not add any extra text " \
"that is not on my images. You can move the text freely to the best location. The result should look like a card my grandmother might send me."


def add_text_to_image(text_image_path: str, 
                      main_image_path: str, 
                      output_dir: str = 'image_outputs',
                      output_size: str = '1K', 
                      aspect_ratio: str = '4:3',
                      save_locally: bool = True) -> str:
    """
    Combine one main image with one text image.
    Must have REPLICATE_API_TOKEN=... in the .env
    """
    #TODO: make async

    # Upload images to replicate to be able to use them
    with open(text_image_path, "rb") as file:
        text_image = replicate.files.create(file)
    with open(main_image_path, 'rb') as file:
        generated_image = replicate.files.create(file)


    input = {
        "size": output_size,
        "prompt": COMBINATION_PROMPT, 
        "aspect_ratio": aspect_ratio,
        "image_input": [generated_image.urls['get'], text_image.urls['get']]
    }

    output = replicate.run(
        "bytedance/seedream-4",
        input=input
    )

    # To write the files to disk:
    if save_locally:
        for index, item in enumerate(output):
            time_str = str(time.time_ns())
            file_name = hashlib.md5(time_str.encode()).hexdigest()
            with open(os.path.join(output_dir, str(file_name) + '.jpg'), "wb") as file:
                file.write(item.read())
            
    return str(output[0])
