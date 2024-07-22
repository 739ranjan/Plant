from __future__ import division, print_function  
import sys
sys.stdout.reconfigure(encoding='utf-8')
import sys
import os
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

import json
from jinja2 import Environment, FileSystemLoader

from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

#  to configure TensorFlow to allocate GPU memory dynamically
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    except RuntimeError as e:
        print(e)

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_PATH ='alexnet.h5'

# Load your trained model
model = load_model(MODEL_PATH)

# load json file 
with open('new_about_disease.json') as json_file:
    data = json.load(json_file)

# loading disease names in list
disease_list = list(data.keys())

# fetching data about disese from json after prediction
def load_about_disease(preds):
    disease_name = disease_list[preds]
    return data.get(disease_name)

# function for prediction of disease using image
def model_predict(img_path, model):
    print("Hold on predicting ........")
    print(img_path)
    img = Image.open(img_path).resize((224, 224))  

    # Preprocessing the image
    x = image.img_to_array(img)
    x=x/255
    x = np.expand_dims(x, axis=0)

    global preds
    preds = model.predict(x)
    preds=np.argmax(preds, axis=1)
    preds = int(preds)

    predicted_disease = "The plant is diseased with "+disease_list[preds]+"\n"
    print("predicted disease is :" + disease_list[preds])
    return predicted_disease


@app.route('/predict', methods=['POST'])
def upload():
    print("Hold on uploading file ........")
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        
        print("file uploading complete ........")

        # Make prediction
        result = model_predict(file_path, model)
        print(result)
        print("....Prediction = " + result + " ...")
        more = load_about_disease(preds)
        disease = disease_list[preds]
        return [result, more, disease]
    return "Invalid Request"

@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def index():
    # Main page
    print("Inside home page.......... ")
    return render_template('index.html')

@app.route('/know')
def know():
    # Know more page
    print("Inside know More page.......... ")
    return render_template('know.html')

@app.route('/contact')
def contact():
    # Contact us page
    print("Inside contact us page.......... ")
    return render_template('contact.html')


# if __name__ == '__main__':
#     app.run(port=8001, debug=True, host='0.0.0.0')
