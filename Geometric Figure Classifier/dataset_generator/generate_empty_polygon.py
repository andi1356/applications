from random import randint
import PIL.ImageDraw as ImageDraw
import PIL.Image as Image
import os


def generate_folders():
    if os.path.exists('empty_polygon'):
        os.chdir('empty_polygon')
    else:
        os.mkdir('empty_polygon')
        os.chdir('empty_polygon')


def generate_images(img_no):
    generate_folders()
    for counter in range(img_no):
        A = (randint(10, 190), randint(10, 190))
        B = (randint(10, 190), randint(410, 590))
        C = (randint(410, 590), randint(10, 190))
        D = (randint(410, 590), randint(410, 590))
        border = [A, B, D, C, A]

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

        image.save('empty_polygon' + str(counter) + '.png')


generate_images(3)
