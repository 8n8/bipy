import cv2
import keras
import os
import json
import numpy as np


def make_model():
    c2d = keras.layers.convolutional.Conv2D
    c1 = c2d(5, 5, strides=2, activation='relu')
    c2 = c2d(8, 3, strides=2, activation='relu')
    c3 = c2d(11, 3, strides=2, activation='relu')
    c4 = c2d(14, 3, strides=2, activation='relu')
    c5 = c2d(17, 3, strides=2, activation='relu')
    c6 = c2d(20, 3, strides=2, activation='relu')
    dense1 = keras.layers.Dense(15, activation='relu')
    dense2 = keras.layers.Dense(10, activation='softmax')
    bn = keras.layers.BatchNormalization()
    flat = keras.layers.core.Flatten()
    input_im = keras.layers.Input(shape=(480, 720, 1))
    nn = dense2(dense1(bn(flat(c6(c5(c4(c3(c2(c1(input_im))))))))))
    return keras.models.Model(inputs=input_im, outputs=nn)


model = make_model()
print(model.summary())
model.compile(
    loss='categorical_crossentropy',
    optimizer=keras.optimizers.Adam(lr=0.08),
    metrics=['accuracy'])


def format_label(raw):
    labels = [0 for _ in range(10)]
    for r in raw:
        labels[r] = 1
    arr = np.array(labels)
    return arr


class GetSomeData(keras.utils.Sequence):

    def __init__(self):
        self.filenames = os.listdir('photos')
        with open('labels.json') as f:
            self.labels = json.load(f)

    def __len__(self):
        return len(self.filenames)

    def __getitem__(self, idx):
        filename = self.filenames[idx]
        im = np.expand_dims(
            np.expand_dims(
                cv2.imread('photos/' + filename, cv2.IMREAD_GRAYSCALE), 2), 0)
        labels = format_label(self.labels[filename])
        return (im, np.expand_dims(labels, 0))


model.fit(x=GetSomeData())

model.save('model.h5')
