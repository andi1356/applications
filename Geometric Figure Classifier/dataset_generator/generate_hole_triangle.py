from random import randint
import math
import PIL.ImageDraw as ImageDraw
import PIL.Image as Image
import os


def generate_folder():
    if os.path.exists('hole_triangle'):
        os.chdir('hole_triangle')
    else:
        os.mkdir('hole_triangle')
        os.chdir('hole_triangle')


def distance(p1, p2):
    return math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2))


def generate_images(img_no):
    generate_folder()
    for counter in range(img_no):
        A = (randint(10, 190), randint(10, 190))
        B = (randint(10, 190), randint(410, 590))
        C = (randint(410, 590), randint(210, 390))
        border = (A, B, C)

        color = (randint(100, 255), randint(100, 255), randint(100, 255))

        image = Image.new("RGB", (600, 600))
        draw = ImageDraw.Draw(image)
        draw.polygon(border, fill=color)

        c = distance(A, B)
        a = distance(B, C)
        b = distance(A, C)
        x_centroid = (a * A[0] + b * B[0] + c * C[0]) / (a + b + c)
        y_centroid = (a * A[1] + b * B[1] + c * C[1]) / (a + b + c)
        centroid = (x_centroid, y_centroid, randint(10, 55))
        hole_sides = randint(3, 6)

        draw.regular_polygon(bounding_circle=(centroid),
                             n_sides=hole_sides,
                             fill=(0, 0, 0))

        image.save('hole_triangle' + str(counter) + '.png')
        print(counter)


generate_images(5)
