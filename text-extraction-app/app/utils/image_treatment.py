from PIL import Image
import pytesseract
import cv2
import numpy as np
import string
import random
import os
from app import app

class ImageExtract():

    def __init__(self, image, steps=['img_to_array', 'img_to_gray', 'img_to_rgb', 'img_text_extract', 'text_symbol_remotion']):
        self.steps = steps
        self.image = image

    def img_to_array(self, image):
        """
        Convert image to and array of numbers.

        Returns:
            numpy.ndarray: Array containing converted image.
        """        
        # Converting image to array
        image_arr = np.array(image.convert('RGB'))
        
        return image_arr

    def img_to_gray(self, image):
        """
        Convert image array to gray scale image.

        Returns:
            numpy.ndarray: Array containing converted image.
        """        
        # Converting image to grayscale
        gray_img_arr = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        return gray_img_arr

    def img_to_rgb(self, image):
        """
        Convert image to rgb.

        Args:
            image (numpy.ndarray): numpy array of converted image.

        Returns:
            numpy.ndarray: array of image.
        """        
        #Converting image back to rbg
        rgb_image = Image.fromarray(image)

        return rgb_image

    def name_generator(self):
        """
        Generates a random image name.

        Returns:
            dict: Returns a dict containing both the full file name and the image name.
        """        
        # Printing lowercase
        letters = string.ascii_lowercase
        # Generating unique image name for dynamic image display
        name = ''.join(random.choice(letters) for i in range(10)) + '.png'
        full_filename =  'uploads/' + name
        
        return {'full_name':full_filename, 'name':name}

    def img_text_extract(self, image):
        """
        Extract text from image.

        Args:
            image (numpy.ndarray): Numpy array containing image.

        Returns:
            string: Text in image.
        """        
        # Extracting text from image
        custom_config = r'-l eng --oem 3 --psm 6'
        text = pytesseract.image_to_string(image,config=custom_config)

        return text

    def text_symbol_remotion(self, image_text):
        """
        Removes symbols from extracted text in image.

        Args:
            image_text (string): Text written in image.

        Returns:
            string: Clean string without symbols.
        """        # Remove symbol if any
        characters_to_remove = "!()@—*“>+-/,'|£#%$&^_~"
        new_string = image_text
        for character in characters_to_remove:
            new_string = new_string.replace(character, "")

        # Converting string into list to dislay extracted text in seperate line
        new_string = new_string.split("\n")
        
        return new_string

    def image_save(self, image_arr, name):
        """
        Save image based on app configured path.

        Args:
            img_array (numpy.ndarray): image array that's going to be saved.
            name (string): string containing image name.
        """        
        # Saving image to display in html
        
        img = Image.fromarray(image_arr, 'RGB')
        img.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], name))


    def fit_transform(self):
        """
        Fit transform all the necessary functions in the transformation and counting steps for image.

        Returns:
            dictionary: Returns a dictionary containing the amount cars and busses and the full file name.
        """        
        
        # instance name
        generated_name = self.name_generator()

        # saving image
        self.image_save(self.img_to_array(self.image), generated_name['name'])

        # image processing steps
        for i in self.steps:
            print(f'Processing {i}')
            self.image = eval('self.{0}(self.image)'.format(i))
        
        return {'image_string': self.image, 'full_name':generated_name['full_name']}
