"""
### THIS SCRIPT HAS NOT BEEN TESTED YET ###

This is a GUI to predict the Geometric Figures
acordingly to the trained model

author: Andrei-Antonio Robu ( robu.andrei.antonio@gmail.com )
"""
from keras.models import load_model
import tensorflow_hub as hub
import glob
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog as fd
IMG_W, IMG_H = 224, 224
CLASSES = ['empty_polygon', 'empty_triangle', 'full_polygon', 'full_triangle',
           'hole_polygon', 'hole_triangle']

def custom_load_model(fpath):
    model = load_model((fpath), custom_objects={'KerasLayer': hub.KerasLayer})

    return model


def custom_load_image(fpath):
    img = cv2.imread(fpath)
    img = cv2.resize(img, (IMG_W, IMG_H))
    img = np.reshape(img, [1, IMG_W, IMG_H, 3])
    return img


def predict(model, img):
    lista = model.predict(img)
    index = np.argmax(lista)
    return CLASSES[index]


if __name__ == '__main__':
    model = custom_load_model('model.h5')

    img_path = sorted(glob.glob('predict_test/*.png'))
    images = [custom_load_image(img) for img in img_path]
    predictions = [predict(model, img) for img in images]

    for index in range(len(predictions)):
        print(prediction[index], img_path)
