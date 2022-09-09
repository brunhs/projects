# Important imports
from app import app
from flask import request, render_template, url_for
import os
import cv2
import numpy as np
from PIL import Image
import random
import string
import pytesseract
from app.utils.image_treatment import ImageExtract


# Adding path to config
app.config['INITIAL_FILE_UPLOADS'] = 'app/static/uploads'

# Route to home page
@app.route("/", methods=["GET", "POST"])
def index():

	if request.method == "GET":
		full_filename =  'images/white_bg.jpg'
		return render_template("index.html", full_filename = full_filename)

	if request.method == "POST":
		image_extract = ImageExtract(image=Image.open(request.files['image_upload'])).fit_transform()
		
		return render_template('index.html', full_filename = image_extract['full_name'], text = image_extract['image_string'])

# Main function
if __name__ == '__main__':
    app.run(debug=True)
