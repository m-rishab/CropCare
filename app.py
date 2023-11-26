from flask import Flask, render_template, request, redirect
from markupsafe import Markup
import numpy as np
import pandas as pd
import pickle
import requests
import config
from utils.fertilizer import fertilizer_dic
from utils.disease import disease_dic
import io
import torch
from torchvision import transforms
from PIL import Image
from utils.model import ResNet9

#------CROP RECOMMENDATION RECOMMENDER-----------------------#

# Loading crop recommendation model
crop_recommendation_model_path = 'models/RandomForest.pkl'
crop_recommendation_model = pickle.load(open(crop_recommendation_model_path, 'rb'))

# Custom functions for calculations
def weather_fetch(city_name):
    """
    Fetch and return the temperature and humidity of a city
    :params: city_name
    :return: temperature, humidity or None if there is an error
    """
    print (city_name)
    api_key = config.weather_api_key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    if api_key is None or city_name is None:
        return None

    complete_url = base_url + "q=" + city_name + "&appid=" + api_key
    response = requests.get(complete_url)

    if response.status_code == 200:
        weather_data = response.json()
        temperature = round(weather_data["main"]["temp"] - 273.15, 2)
        humidity = weather_data["main"]["humidity"]
        return temperature, humidity
    else:
        return None

# ===============================================================================================
# ------------------------------------ FLASK APP -------------------------------------------------
# Creating Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/crop')
def crop():
    return render_template('crop.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/fert_recommend')
def fert_recommend():
    return render_template('fertilizer.html')

# RENDER PREDICTION PAGES

@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        # Extracting input values from the form
        N = int(request.form['nitrogen'])
        P = int(request.form['phosphorous'])
        K = int(request.form['pottasium'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])

        
        city = request.form.get("city")

        # Fetching weather data
        weather_data = weather_fetch(city)

        if weather_data:
            temperature, humidity = weather_data
            # Update the data array with additional features
            data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
            my_prediction = crop_recommendation_model.predict(data)
            final_prediction = my_prediction[0]
            return render_template('crop-result.html', prediction=final_prediction)
        else:
            return render_template('try-again.html', message="Failed to fetch weather data.")

#_--------Fertilizer RECOMMENDER___________________#

@app.route('/fertilizer-predict', methods=['GET', 'POST'])
def fertilizer_predict():
    if request.method == 'POST':
        crop_name = str(request.form['cropname'])
        N = int(request.form['Nitrogen'])
        P = int(request.form['Phosphorous'])
        K = int(request.form['Pottasium'])

        df = pd.read_csv('Datasets/fertilizer.csv')

        nr = df[df['Crop'] == crop_name]['N'].iloc[0]
        pr = df[df['Crop'] == crop_name]['P'].iloc[0]
        kr = df[df['Crop'] == crop_name]['K'].iloc[0]

        n = nr - N
        p = pr - P
        k = kr - K
        temp = {abs(n): "N", abs(p): "P", abs(k): "K"}
        max_value = temp[max(temp.keys())]
        if max_value == "N":
            if n < 0:
                key = 'NHigh'
            else:
                key = "Nlow"
        elif max_value == "P":
            if p < 0:
                key = 'PHigh'
            else:
                key = "Plow"
        else:
            if k < 0:
                key = 'KHigh'
            else:
                key = "Klow"

        response = Markup(str(fertilizer_dic[key]))

        return render_template('fertilizer-result.html', recommendation=response)


# Loading plant disease classification model

disease_classes = ['Apple___Apple_scab',
                   'Apple___Black_rot',
                   'Apple___Cedar_apple_rust',
                   'Apple___healthy',
                   'Blueberry___healthy',
                   'Cherry_(including_sour)___Powdery_mildew',
                   'Cherry_(including_sour)___healthy',
                   'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
                   'Corn_(maize)___Common_rust_',
                   'Corn_(maize)___Northern_Leaf_Blight',
                   'Corn_(maize)___healthy',
                   'Grape___Black_rot',
                   'Grape___Esca_(Black_Measles)',
                   'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
                   'Grape___healthy',
                   'Orange___Haunglongbing_(Citrus_greening)',
                   'Peach___Bacterial_spot',
                   'Peach___healthy',
                   'Pepper,_bell___Bacterial_spot',
                   'Pepper,_bell___healthy',
                   'Potato___Early_blight',
                   'Potato___Late_blight',
                   'Potato___healthy',
                   'Raspberry___healthy',
                   'Soybean___healthy',
                   'Squash___Powdery_mildew',
                   'Strawberry___Leaf_scorch',
                   'Strawberry___healthy',
                   'Tomato___Bacterial_spot',
                   'Tomato___Early_blight',
                   'Tomato___Late_blight',
                   'Tomato___Leaf_Mold',
                   'Tomato___Septoria_leaf_spot',
                   'Tomato___Spider_mites Two-spotted_spider_mite',
                   'Tomato___Target_Spot',
                   'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
                   'Tomato___Tomato_mosaic_virus',
                   'Tomato___healthy']

disease_model_path = 'models/plant_disease_model.pth'
disease_model = ResNet9(3, len(disease_classes))
disease_model.load_state_dict(torch.load(
    disease_model_path, map_location=torch.device('cpu')))
disease_model.eval()        


def predict_image(img, model=disease_model):
    """
    Transforms image to tensor and predicts disease label
    :params: image
    :return: prediction (string)
    """
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.ToTensor(),
    ])
    image = Image.open(io.BytesIO(img))
    img_t = transform(image)
    img_u = torch.unsqueeze(img_t, 0)

    # Get predictions from model
    yb = model(img_u)
    # Pick index with highest probability
    _, preds = torch.max(yb, dim=1)
    prediction = disease_classes[preds[0].item()]
    # Retrieve the class label
    return prediction
    
# render disease prediction result page
@app.route('/disease-predict', methods=['GET', 'POST'])
def disease_prediction():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files.get('file')
        if not file:
            return render_template('try-again.html')
        try:
            img = file.read()

            prediction = predict_image(img)

            prediction = Markup(str(disease_dic[prediction]))
            return render_template('plant_disease-result.html', prediction=prediction)
        except:
            pass
    return render_template('plant-disease.html')    



# Python main
if __name__ == "__main__":
    app.run(debug=True)
