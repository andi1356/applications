from random import randint
import PIL.ImageDraw as ImageDraw
import PIL.Image as Image
import os


def generate_folder():
    if os.path.exists('full_triangle'):
        os.chdir('full_triangle')
    else:
        os.mkdir('full_triangle')
        os.chdir('full_triangle')


def generate_images(img_no):
    generate_folder()
    for counter in range(img_no):
        A = (randint(10, 190), randint(10, 190))
        B = (randint(10, 190), randint(410, 590))
        C = (randint(410, 590), randint(210, 390))
        border = (A, B, C)

        color = (randint(100, 255), randint(100, 255), randint(100, 255))
        print(counter)
        image = Image.new("RGB", (600, 600))
        draw = ImageDraw.Draw(image)
        draw.polygon(border, fill=color)

        image.save('full_triangle_' + str(counter) + '.png')


generate_images(5)
