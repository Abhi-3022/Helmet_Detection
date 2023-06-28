# -*- coding: utf-8 -*-
"""HelmetDetection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DfEkYzuu7sZRw-h0x2vQFbwPVrSNG2_l
"""

import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Conv2D,MaxPooling2D,Flatten,Dropout
from tensorflow.keras.activations import relu,sigmoid,linear
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing import image
from google.colab.patches import cv2_imshow
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image

data = pd.read_csv("/content/drive/MyDrive/file/data.csv")
data

from google.colab import drive
drive.mount('/content/drive')

len(data['label'])

img = mpimg.imread('/content/drive/MyDrive/file/'+data['Image'][4]+'.png')
imgplot = plt.imshow(img)
plt.show()
print(img.shape)

type(data['Image'])

x = []

for i in data['Image']:
  #img = cv2.imread('/content/drive/MyDrive/file/'+i+'.png')
  #img = cv2.resize(img,(64,64))
  img = Image.open('/content/drive/MyDrive/file/'+i+'.png')
  img = img.resize((64,64))
  img = img.convert('RGB')
  img = np.array(img)
  x.append(img)

print(x[0].shape)

x = np.array(x)
y = np.array(data['label'])

x_scaled = x/255
x_scaled.shape

x_train,x_test,y_train,y_test = train_test_split(x_scaled,y,test_size = 0.20)

model = Sequential()
model.add(Conv2D(32,kernel_size=(3,3),activation='relu',input_shape=(64,64,3)))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(64,kernel_size=(3,3),activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Flatten())

model.add(Dense(256,activation='relu'))
model.add(Dropout(0.5))

model.add(Dense(128,activation='relu'))
model.add(Dropout(0.5))

model.add(Dense(2,activation='sigmoid'))

model.summary()

model.compile(
    loss = 'sparse_categorical_crossentropy',
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.001),
    metrics = ['acc']
)

history = model.fit(x_train,y_train,validation_split = 0.1,epochs = 10)

loss,accuracy = model.evaluate(x_test,y_test)
print("Test Accuracy: {}".format(accuracy))

h = history
plt.plot(h.history['loss'],label = 'Train loss')
plt.plot(h.history['val_loss'],label = 'Validation loss')
plt.legend()
plt.plot()

plt.plot(h.history['acc'],label = 'Train Accuracy')
plt.plot(h.history['val_acc'],label = 'Validation Accuracy')
plt.legend()
plt.plot()

img_path = input("Enter the image path : ")
inp_img = cv2.imread(img_path)
cv2_imshow(inp_img)

img = Image.open(img_path)
img = img.resize((64,64))
img = img.convert('RGB')
img = np.array(img)

#inp_img = cv2.resize(inp_img,(64,64))
inp_img = img / 255
print(inp_img.shape)
inp_img = np.reshape(inp_img,[1,64,64,3])
inp_prediction = model.predict(inp_img)
print(inp_prediction)

inp_pred_label = np.argmax(inp_prediction)
print(inp_pred_label)

if inp_pred_label == 1:
  print("The person in the image is wearing a helmet.")
else:
  print("The person in the image is not wearing a helmet.")