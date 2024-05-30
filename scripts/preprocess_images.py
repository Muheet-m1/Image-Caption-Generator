import os
from PIL import Image
import numpy as np
from tqdm import tqdm

def load_images(image_dir, target_size=(224, 224)):
    images = {}
    for img_name in tqdm(os.listdir(image_dir)):
        if img_name.endswith('.jpg'):
            img_path = os.path.join(image_dir, img_name)
            img = Image.open(img_path)
            img = img.resize(target_size)
            img_array = np.array(img)
            images[img_name] = img_array
    return images

if __name__ == "__main__":
    image_dir = r"C:\Users\khale\Desktop\image caption generator\Images"
    images = load_images(image_dir)
    np.save('../data/images.npy', images)

