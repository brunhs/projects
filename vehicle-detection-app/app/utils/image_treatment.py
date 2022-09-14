# Important imports
from .parameters_parser import AppParameters
from app import app
from PIL import Image
import cv2
import numpy as np
import string
import random
import os
import json

class ImageTreatment():
    
    def __init__(self, image, steps=['img_to_array', 'img_to_gray']):
        self.steps = steps
        self.image = image
        self.bus_cascade_src = AppParameters().load(json.load(open('app/parameters.json')))['bus_cascade_src']
        self.car_cascade_src = AppParameters().load(json.load(open('app/parameters.json')))['car_cascade_src']

    def name_generator(self):
        letters = string.ascii_lowercase
        name = ''.join(random.choice(letters) for i in range(10)) + '.png'
        full_filename =  'uploads/' + name
        
        return {'full_name':full_filename, 'name':name}


    def img_to_array(self, image):
        image_arr = np.array(image.convert('RGB'))
        
        return image_arr


    def img_to_gray(self, image):
        gray_img_arr = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        return gray_img_arr

    def bus_img_count(self, img_array, gray):
        bus_cascade = cv2.CascadeClassifier(self.bus_cascade_src)
        bus = bus_cascade.detectMultiScale(gray, 1.1, 1)

        bcnt = 0
        for (x,y,w,h) in bus:
            cv2.rectangle(img_array,(x,y),(x+w,y+h),(0,255,0),2)
            bcnt += 1
        
        return bcnt

    def car_img_count(self, img_array, gray):
        car_cascade = cv2.CascadeClassifier(self.car_cascade_src)
        cars = car_cascade.detectMultiScale(gray, 1.1, 1)

        ccnt = 0
        for (x,y,w,h) in cars:
            cv2.rectangle(img_array,(x,y),(x+w,y+h),(255,0,0),2)
            ccnt += 1

        return ccnt

    def image_save(self, img_array, name):
        
        img = Image.fromarray(img_array, 'RGB')
        img.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], name))

    def fit_transform(self):
        
        generated_name = self.name_generator()

        img_array = self.img_to_array(self.image)

        self.image_save(self.img_to_array(self.image), generated_name['name'])

        for i in self.steps:
            print(f'Processing {i}')
            self.image = eval('self.{0}(self.image)'.format(i))
        
        car_count = self.car_img_count(gray = self.image, img_array = img_array)
        bus_count = self.bus_img_count(gray = self.image, img_array = img_array)

        result = str(car_count) + ' cars and ' + str(bus_count) + ' buses found'

        return {'result': result, 'full_filename':generated_name['full_name']}
