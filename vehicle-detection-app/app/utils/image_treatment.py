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
    """
    Image treatment class that brings all the pipeline necessary to perform the vehicle classification.
    """    
    
    def __init__(self, image, steps=['img_to_array', 'img_to_gray']):
        self.steps = steps
        self.image = image
        self.bus_cascade_src = AppParameters().load(json.load(open('app/parameters.json')))['bus_cascade_src']
        self.car_cascade_src = AppParameters().load(json.load(open('app/parameters.json')))['car_cascade_src']

    def name_generator(self):
        """
        Generates a random image name.

        Returns:
            dict: Returns a dict containing both the full file name and the image name.
        """        
        letters = string.ascii_lowercase
        name = ''.join(random.choice(letters) for i in range(10)) + '.png'
        full_filename =  'uploads/' + name
        
        return {'full_name':full_filename, 'name':name}


    def img_to_array(self):
        """
        Convert image to and array of numbers.

        Returns:
            numpy.ndarray: Array containing converted image.
        """        
        image_arr = np.array(self.image.convert('RGB'))
        
        return image_arr


    def img_to_gray(self):
        """
        Convert image array to gray scale image.

        Returns:
            numpy.ndarray: Array containing converted image.
        """        
        gray_img_arr = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        
        return gray_img_arr

    def bus_img_count(self, img_array, gray):
        """
        Load cascade file for bus counting and classyfing, also count the amount of buses in image.

        Args:
            img_array (numpy.ndarray): Array image.
            gray (numpy.ndarray): Gray converted image.

        Returns:
            int: amount of busses counted.
        """        
        bus_cascade = cv2.CascadeClassifier(self.bus_cascade_src)
        bus = bus_cascade.detectMultiScale(gray, 1.1, 1)

        bcnt = 0
        for (x,y,w,h) in bus:
            cv2.rectangle(img_array,(x,y),(x+w,y+h),(0,255,0),2)
            bcnt += 1
        
        return bcnt

    def car_img_count(self, img_array, gray):
        """
        Load cascade file for car counting and classyfing, also count the amount of cars in image.

        Args:
            img_array (numpy.ndarray): Array image.
            gray (numpy.ndarray): Gray converted image.

        Returns:
            int: amount of cars counted.
        """        
        car_cascade = cv2.CascadeClassifier(self.car_cascade_src)
        cars = car_cascade.detectMultiScale(gray, 1.1, 1)

        ccnt = 0
        for (x,y,w,h) in cars:
            cv2.rectangle(img_array,(x,y),(x+w,y+h),(255,0,0),2)
            ccnt += 1

        return ccnt

    def image_save(self, img_array, name):
        """
        Save image based on app configured path.

        Args:
            img_array (numpy.ndarray): image array that's going to be saved.
            name (string): string containing image name.
        """        
        
        img = Image.fromarray(img_array, 'RGB')
        img.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], name))

    def fit_transform(self):
        """
        Fit transform all the necessary functions in the transformation and counting steps for image.

        Returns:
            dictionary: Returns a dictionary containing the amount cars and busses and the full file name.
        """        
        
        generated_name = self.name_generator()

        img_array = self.img_to_array()

        self.image_save(img_array, generated_name['name'])

        for i in self.steps:
            print(f'Processing {i}')
            self.image = eval('self.{0}()'.format(i))
        
        car_count = self.car_img_count(gray = self.image, img_array = img_array)
        bus_count = self.bus_img_count(gray = self.image, img_array = img_array)

        result = str(car_count) + ' cars and ' + str(bus_count) + ' buses found'

        return {'result': result, 'full_filename':generated_name['full_name']}
