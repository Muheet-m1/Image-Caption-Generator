import os
import string
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

nltk.download('punkt')
nltk.download('stopwords')

def load_captions(caption_file):
    with open(caption_file, 'r') as file:
        captions = file.read()
    return captions

def preprocess_captions(captions):
    table = str.maketrans('', '', string.punctuation)
    stop_words = set(stopwords.words('english'))
    
    processed_captions = []
    for line in captions.strip().split('\n'):
        tokens = word_tokenize(line.lower())
        tokens = [word.translate(table) for word in tokens]
        tokens = [word for word in tokens if word.isalpha()]
        tokens = [word for word in tokens if word not in stop_words]
        processed_captions.append(' '.join(tokens))
    
    return processed_captions

if __name__ == "__main__":
    caption_file = r"C:\Users\khale\Desktop\image caption generator\captions.txt"
    captions = load_captions(caption_file)
    processed_captions = preprocess_captions(captions)
    np.save('../data/captions.npy', processed_captions)
