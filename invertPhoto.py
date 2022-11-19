import os
import re
import shutil

import PIL
from fastapi import File
from PIL import Image, ImageOps


def save_image(file: File(), filename):
    with open(filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        return 0


def move_image(filename):
    shutil.move(os.path.join(filename), os.path.join('images', filename))
    return 0


def invert_photo_colors(filename):
    no_suffix_filename = remove_suffix(filename)
    print(no_suffix_filename)
    image = Image.open('images/' + filename)
    if image.mode == 'RGBA':
        r, g, b, a = image.split()
        rgb_image = Image.merge('RGB', (r, g, b))

        inverted_image = PIL.ImageOps.invert(rgb_image)

        r2, g2, b2 = inverted_image.split()

        final_transparent_image = Image.merge('RGBA', (r2, g2, b2, a))

        final_transparent_image.save('images/images_inverted/' + no_suffix_filename + '.png')

    else:
        inverted_image = PIL.ImageOps.invert(image)
        inverted_image.save('images/images_inverted/' + no_suffix_filename + '.png')
    return 0


def remove_suffix(filename):
    filename = re.sub('\.JPG$', '', filename)
    return filename


def display_image(filename):
    image_to_print = remove_suffix(filename) + ".png"
    with open('images/images_inverted/' + image_to_print, mode="rb") as file_like:
        yield from file_like


from fastapi import File
from PIL import Image
import PIL.ImageOps
import io
from fastapi.responses import StreamingResponse


def invert_picture_colors(file: bytes = File()):
    input = Image.open(io.BytesIO(file))
    inverted = PIL.ImageOps.invert(input)
    response = io.BytesIO()
    inverted.save(response, "JPEG")
    response.seek(0)
    return StreamingResponse(response, media_type="image/jpeg")
