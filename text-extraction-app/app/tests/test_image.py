from app.utils.image_treatment import ImageExtract

def test_name_generator(image_import):
    assert ['full_name', 'name'] == list(ImageExtract(image=image_import).name_generator().keys())

def test_image_treatment_funcs(image_import):
    image_extract = ImageExtract(image=image_import)
    assert (image_extract.img_to_array().dtype == 'uint8')
    assert (ImageExtract(image=image_extract.img_to_array()).img_to_gray().dtype == 'uint8')
    assert (type(image_extract.img_text_extract()) == str)