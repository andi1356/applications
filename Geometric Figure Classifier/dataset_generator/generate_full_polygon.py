import math
from random import randint, shuffle
import PIL.ImageDraw as ImageDraw
import PIL.Image as Image
class_name = 'full_polygon'
import os


def generate_folder():
    if os.path.exists(class_name):
        os.chdir(class_name)
    else:
        os.mkdir(class_name)
        os.chdir(class_name)


def generate_images(img_no):
    generate_folder()
    for counter in range(1000):
        A = (randint(10, 190), randint(10, 190))
        B = (randint(10, 190), randint(410, 590))
        C = (randint(410, 590), randint(10, 190))
        D = (randint(410, 590), randint(410, 590))
        border = [A, B, D, C]
        # shuffle(border)
        print(counter)
        color = (randint(100, 255), randint(100, 255), randint(100, 255))

        image = Image.new("RGB", (600, 600))
        draw = ImageDraw.Draw(image)
        draw.polygon(border, fill=color)

        image.save('full_polygon_' + str(counter) + '.png')


generate_images(5)
