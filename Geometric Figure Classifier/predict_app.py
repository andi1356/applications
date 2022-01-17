"""
### THIS SCRIPT HAS NOT BEEN TESTED YET ###
This is a GUI to predict the Geometric Figures
acordingly to the trained model

author: Andrei-Antonio Robu ( robu.andrei.antonio@gmail.com )
"""
import tensorflow as tf
from keras.models import load_model
import tensorflow_hub as hub
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog as fd
IMG_W, IMG_H = 224, 224
CLASSES = ['empty_polygon', 'empty_triangle', 'full_polygon', 'full_triangle',
           'hole_polygon', 'hole_triangle']


def custom_load_model(fpath):
    model = load_model((fpath), custom_objects={'KerasLayer': hub.KerasLayer})
    model.compile(
        optimizer='adam',
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy'])
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


def gui_init():
    root = tk.Tk()
    root.title('Geometric Figure Predictor')
    root.resizable(False, False)
    root.geometry('300x150')
    f = fd.askopenfile()
    root.mainloop()
    return f


def gui_print(prediction):
    label = tk.Label(
        text=prediction,
        foreground="white",
        background="black"
    )
    label.pack()


if __name__ == '__main__':
    file = gui_init()

    model = custom_load_model('model.h5')
    img = custom_load_image(file.name)
    prediction = predict(model, img)
    print(prediction)

    gui_print(prediction)
