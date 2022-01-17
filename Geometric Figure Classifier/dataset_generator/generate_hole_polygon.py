from random import randint
import math
import PIL.ImageDraw as ImageDraw
import PIL.Image as Image
import os


def generate_folders():
    if os.path.exists('hole_polygon'):
        os.chdir('hole_polygon')
    else:
        os.mkdir('hole_polygon')
        os.chdir('hole_polygon')


def distance(p1, p2):
    return math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2))


def generate_images(img_no):
    generate_folders()
    for counter in range(img_no):
        A = (randint(10, 190), randint(10, 190))
        B = (randint(10, 190), randint(410, 590))
        C = (randint(410, 590), randint(10, 190))
        D = (randint(410, 590), randint(410, 590))
        border = [A, B, D, C]

        color = (randint(100, 255), randint(100, 255), randint(100, 255))

        image = Image.new("RGB", (600, 600))
        draw = ImageDraw.Draw(image)
        draw.polygon(border, fill=color)

        x_centroid = randint(255, 345)
        y_centroid = randint(255, 345)

        centroid = (x_centroid, y_centroid, randint(30, 80))

        hole_sides = randint(4, 12)

        draw.regular_polygon(centroid,
                             n_sides=hole_sides,
                             fill=(0, 0, 0))

        image.save('hole_polygon_' + str(counter) + '.png')
        print(counter)


generate_images(5)
