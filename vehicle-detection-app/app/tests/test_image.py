from app.utils.parameters_parser import AppParameters
from app.utils.image_treatment import ImageTreatment
import json

def test_parameters_path():
    assert AppParameters().load(json.load(open('app/parameters.json'))) == {
"car_cascade_src": "app/static/cascade/cars.xml",
"bus_cascade_src": "app/static/cascade/Bus_front.xml",
"full_filename": "images/white_bg.jpg"
}

def test_name_generator(image_import):
    assert ['full_name', 'name'] == list(ImageTreatment(image=image_import).name_generator().keys())

def test_image_treatment_funcs(image_import):
    image_array = ImageTreatment(image=image_import).img_to_array()
    assert (image_array.dtype == 'uint8')
    assert (ImageTreatment(image=image_array).img_to_gray().dtype == 'uint8')