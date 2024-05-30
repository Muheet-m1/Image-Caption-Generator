import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import Sequential
from keras.callbacks import ModelCheckpoint
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split

from encoder import build_encoder
from decoder import build_decoder

def load_data():
    images = np.load('../data/encoded_images.npy', allow_pickle=True).item()
    captions = np.load('../data/captions.npy', allow_pickle=True).tolist()
    return images, captions

def create_tokenizer(captions):
    tokenizer = tf.keras.preprocessing.text.Tokenizer()
    tokenizer.fit_on_texts(captions)
    return tokenizer

def create_sequences(tokenizer, captions, max_length):
    X1, X2, y = [], [], []
    for caption in captions:
        seq = tokenizer.texts_to_sequences([caption])[0]
        for i in range(1, len(seq)):
            in_seq, out_seq = seq[:i], seq[i]
            in_seq = pad_sequences([in_seq], maxlen=max_length)[0]
            out_seq = tf.keras.utils.to_categorical([out_seq], num_classes=vocab_size)[0]
            X1.append()
            X2.append(in_seq)
            y.append(out_seq)
    return np.array(X1), np.array(X2), np.array(y)

if __name__ == "__main__":
    images, captions = load_data()
    tokenizer = create_tokenizer(captions)
    vocab_size = len(tokenizer.word_index) + 1
    max_length = max(len(caption.split()) for caption in captions)

    X1, X2, y = create_sequences(tokenizer, captions, max_length)
    X1_train, X1_val, X2_train, X2_val, y_train, y_val = train_test_split(X1, X2, y, test_size=0.2)

    encoder = build_encoder()
    decoder = build_decoder(vocab_size, max_length)
    decoder.compile(loss='categorical_crossentropy', optimizer='adam')

    filepath = '../models/weights-improvement-{epoch:02d}-{loss:.4f}.hdf5'
    checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
    callbacks_list = [checkpoint]

    decoder.fit([X1_train, X2_train], y_train, epochs=20, verbose=2, callbacks=callbacks_list, validation_data=([X1_val, X2_val], y_val))
