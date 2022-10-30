import os
import shutil
from fastapi import File


def save_image(file: File(), filename):
    with open(filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        return 0


def move_image(filename):
    shutil.move(os.path.join(filename), os.path.join('images', filename))
    return 0
