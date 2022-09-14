# Important imports
from app import app
from flask import request, render_template, url_for
import cv2
import numpy as np
from PIL import Image
import string
import random
import os

class ImageTreatment():
    
    def __init__(self, image, bus_cascade_src, car_cascade_src, steps=['img_to_array', 'img_to_gray']):
        self.steps = steps
        self.image = image
        self.bus_cascade_src = bus_cascade_src
        self.car_cascade_src = car_cascade_src

    def name_generator(self):
        # Printing lowercase
        letters = string.ascii_lowercase
        # Generating unique image name for dynamic image display
        name = ''.join(random.choice(letters) for i in range(10)) + '.png'
        full_filename =  'uploads/' + name
        
        return {'full_name':full_filename, 'name':name}


    def img_to_array(self, image):
        # Converting image to array
        image_arr = np.array(image.convert('RGB'))
        
        return image_arr


    def img_to_gray(self, image):
        # Converting image to grayscale
        gray_img_arr = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        return gray_img_arr

    def bus_img_count(self, img_array, gray):
        # bus cascade
        bus_cascade = cv2.CascadeClassifier(self.bus_cascade_src)
        bus = bus_cascade.detectMultiScale(gray, 1.1, 1)

        bcnt = 0
        for (x,y,w,h) in bus:
            cv2.rectangle(img_array,(x,y),(x+w,y+h),(0,255,0),2)
            bcnt += 1
        
        return bcnt

    def car_img_count(self, img_array, gray):
        # car cascade
        car_cascade = cv2.CascadeClassifier(self.car_cascade_src)
        cars = car_cascade.detectMultiScale(gray, 1.1, 1)

        ccnt = 0
        for (x,y,w,h) in cars:
            cv2.rectangle(img_array,(x,y),(x+w,y+h),(255,0,0),2)
            ccnt += 1

        return ccnt

    def image_save(self, img_array, name):
        
        # Saving image to display in html        
        img = Image.fromarray(img_array, 'RGB')
        img.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], name))

    def fit_transform(self):
        
        # instance name
        generated_name = self.name_generator()

        img_array = self.img_to_array(self.image)

        # saving image
        self.image_save(self.img_to_array(self.image), generated_name['name'])

        # image processing steps
        for i in self.steps:
            print(f'Processing {i}')
            self.image = eval('self.{0}(self.image)'.format(i))
        
        car_count = self.car_img_count(gray = self.image, img_array = img_array)
        bus_count = self.bus_img_count(gray = self.image, img_array = img_array)

        # Returning template, filename, extracted text
        result = str(car_count) + ' cars and ' + str(bus_count) + ' buses found'

        return {'result': result, 'full_name':generated_name['full_name']}
