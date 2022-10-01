import pytest
from PIL import Image

@pytest.fixture(scope='session')

def image_import():

    image_import = Image.open('sample.png')
    return image_import