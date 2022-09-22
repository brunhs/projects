import pytest
from PIL import Image

@pytest.fixture(scope='session')

def image_import():

    image_import = Image.open('./sample_data/bus.jpg')
    return image_import