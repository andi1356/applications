from random import randint
import PIL.ImageDraw as ImageDraw
import PIL.Image as Image
import os


def generate_folder():
    if os.path.exists('empty_triangle'):
        os.chdir('empty_triangle')
    else:
        os.mkdir('empty_triangle')
        os.chdir('empty_triangle')


def generate_images(img_no):
    generate_folder()
    for counter in range(img_no):
        A = (randint(10, 190), randint(10, 190))
        B = (randint(10, 190), randint(410, 590))
        C = (randint(410, 590), randint(210, 390))
        border = (A, B, C, A)

        color = (randint(100, 255), randint(100, 255), randint(100, 255))
        line_width = randint(9, 15)
        image = Image.new("RGB", (600, 600))

        draw = ImageDraw.Draw(image)
        draw.line(border, fill=color, width=line_width)
        print(counter)
        for point in border:  # to smudge line corners
            draw.ellipse((point[0] - 4, point[1] - 4, point[0] + 4, point[1] + 4),
                         fill=color,
                         width=line_width)

        image.save('empty_triangle_' + str(counter) + '.png')


generate_images(5)
