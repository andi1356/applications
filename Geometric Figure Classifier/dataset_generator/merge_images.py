from random import shuffle
from PIL import Image
import glob
import os


def load_images():
    img_path = glob.glob('train/**/*png')
    shuffle(img_path)
    images = [Image.open(x) for x in img_path]
    return images


def merge_images(width, height):
    total_width = width
    max_height = height
    final_img_index = 0
    new_im = Image.new('RGB', (total_width, max_height))
    x_offset = 0
    y_offset = 0
    for index, im in enumerate(images, 1):
        im = im.resize((200, 200))
        new_im.paste(im, (x_offset, y_offset))
        x_offset += 200
        if index % 3 == 0:
            x_offset = 0
            y_offset += im.size[1]
        if index % 9 == 0:
            new_im.save(f'final/final_' + str(final_img_index) + '.jpg')
            final_img_index += 1
            new_im = Image.new('RGB', (total_width, max_height))
            x_offset = 0
            y_offset = 0


merge_images(600, 600)
