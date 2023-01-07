from tensorflow import keras
import ind6

model = keras.models.load_model('ind6.h5')

s_out = ind6.img_to_str(model, "images/car_numbers/cars2_out_img_390.jpg")
print(s_out)