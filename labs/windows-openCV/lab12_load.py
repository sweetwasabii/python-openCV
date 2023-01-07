from tensorflow import keras

model = keras.models.load_model('lab12.h5')

import numpy as np

image_size = 28
img = keras.preprocessing.image.load_img(r'images/digits/4.jpg', target_size=(image_size, image_size), color_mode='grayscale')
img_arr = np.expand_dims(img, axis=0)
img_arr = 1 - img_arr / 255.0
img_arr = img_arr.reshape((1, image_size, image_size))
result = np.argmax(model.predict(img_arr), axis=1)
print(result)
