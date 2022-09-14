# Important imports
from app import app
from flask import request, render_template, url_for
from app.utils.image_treatment import ImageTreatment
import cv2
import numpy as np
from PIL import Image
import string
import random
import os



# Adding path to config
app.config['INITIAL_FILE_UPLOADS'] = 'app/static/uploads'

car_cascade_src = 'app/static/cascade/cars.xml'
bus_cascade_src = 'app/static/cascade/Bus_front.xml'

# Route to home page
@app.route("/", methods=["GET", "POST"])
def index():

	# Execute if request is get
	if request.method == "GET":
		full_filename =  'images/white_bg.jpg'
		return render_template("index.html", full_filename = full_filename)

	# Execute if reuqest is post
	if request.method == "POST":

		image = Image.open(request.files['image_upload']).resize((450,250))
		result = ImageTreatment(image=image, bus_cascade_src=bus_cascade_src, car_cascade_src=car_cascade_src).fit_transform()

		return render_template('index.html', full_filename = result['full_name'], pred = result['result'])

# Main function
if __name__ == '__main__':
    app.run(debug=True)
