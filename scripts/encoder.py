from keras.applications.vgg16 import VGG16
from keras.models import Model
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np

def build_encoder():
    vgg = VGG16(weights='imagenet')
    encoder = Model(inputs=vgg.inputs, outputs=vgg.layers[-2].output)
    return encoder

def encode_images(images, encoder):
    encoded_images = {}
    for img_name, img in images.items():
        img = img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = img / 255.0
        features = encoder.predict(img)
        encoded_images[img_name] = features
    return encoded_images

if __name__ == "__main__":
    images = np.load('../data/images.npy', allow_pickle=True).item()
    encoder = build_encoder()
    encoded_images = encode_images(images, encoder)
    np.save('../data/encoded_images.npy', encoded_images)
