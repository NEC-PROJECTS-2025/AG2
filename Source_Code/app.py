from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
import numpy as np
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
 #from tensorflow.keras.applications.vgg16 import preprocess_input

import os
from tensorflow.keras.preprocessing import image

app = Flask(__name__)
model = load_model('go.h5')
target_img = os.path.join(os.getcwd(), 'static/images')

@app.route('/')
def index_view():
    return render_template('index.html')
@app.route('/about')
def about_view():
    return render_template('about.html')
@app.route('/model')
def model_eval():
    return render_template('model.html')
@app.route('/flowchart')
def flowchart_view():
    return render_template('flowchart.html')
    # Allow files with extension png, jpg, and jpeg
ALLOWED_EXT = set(['jpg', 'jpeg', 'png'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXT

# Function to load and prepare the image in the right shape
def read_image(filename):
    img = load_img(filename, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = file.filename
            file_path = os.path.join('static/images', filename)
            file.save(file_path)
            img = read_image(file_path)
            class_prediction = model.predict(img)
            classes_x = np.argmax(class_prediction, axis=1)

            # Map the class to fruit name
            fruit = ""
            quality = ""

            if classes_x == 0:
                fruit = "Apple"
            elif classes_x == 1:
                fruit = "Banana"
            elif classes_x == 2:
                fruit = "Orange"
            elif classes_x == 3:
                fruit = "Lime"
            elif classes_x == 4:
                fruit = "Guava"
            elif classes_x == 5:
                fruit = "Pomogranate"

            # Assign quality based on probabilities
            max_prob = np.max(class_prediction)
            if max_prob > 0.8:
                quality = "Good"
            elif max_prob > 0.5:
                quality = "Mixed"
            else:
                quality = "Bad"

            return render_template('predict.html', fruit=fruit, quality=quality, user_image=file_path)
        else:
            return "Unable to read the file. Please check file extension."
    elif request.method == 'GET':
        # Render the predict.html form page
        return render_template('predict.html')



if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=8000)
