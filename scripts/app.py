from flask import Flask, request, jsonify, send_from_directory
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
import numpy as np
import pickle
import os
import tensorflow as tf

# Initialize the Flask application
app = Flask(__name__)

# Load the VGG model for feature extraction
vgg_model = VGG16(include_top=False, pooling='avg')

# Load the captioning model
model_path = os.path.join(os.getcwd(), 'best_model.keras')
model = load_model(model_path, custom_objects={'NotEqual': tf.keras.layers.Layer}, compile=False)


# Load the tokenizer
tokenizer_path = os.path.join(os.getcwd(), 'tokenizer.pkl')
with open(tokenizer_path, 'rb') as file:
    tokenizer = pickle.load(file)

# Function to generate caption
def generate_caption(model, image_feature, tokenizer, max_length):
    in_text = 'startseq'
    for _ in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], maxlen=max_length)
        
        # Ensure image_feature is expanded correctly
        image_feature = np.expand_dims(image_feature, axis=0)

        # Predict next word using model
        yhat = model.predict([image_feature, sequence], verbose=0)
        yhat = np.argmax(yhat)

        # Convert index to word
        word = tokenizer.index_word.get(yhat)
        if word is None:
            break
        in_text += ' ' + word
        if word == 'endseq':
            break
    return in_text

# Home route to serve the front-end application
@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')

# Route to serve other front-end assets
@app.route('/frontend/<path:path>')
def send_frontend(path):
    return send_from_directory('frontend', path)

# Route for image caption generation
@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image file provided'}), 400
    
    # Save the uploaded image to a temporary directory
    image_path = os.path.join(os.getcwd(), 'temp', file.filename)
    file.save(image_path)
    
    # Preprocess the image
    image = load_img(image_path, target_size=(224, 224))
    image = img_to_array(image)
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    image = preprocess_input(image)
    
    # Extract features using VGG model
    feature = vgg_model.predict(image, verbose=0)
    
    # Generate caption
    max_length = 50  # Adjust according to your model's max sequence length
    caption = generate_caption(model, feature, tokenizer, max_length)
    
    # Clean up temporary image file
    os.remove(image_path)
    
    return jsonify({'caption': caption})

# Create temp directory if it doesn't exist
if not os.path.exists('temp'):
    os.makedirs('temp')

if __name__ == '__main__':
    app.run(debug=True)
