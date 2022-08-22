import pytest
from model.data_preparation.data_preparation import readData, cleanTitle
from model.count_vectorizer import ModelCountVectorizer

@pytest.fixture(scope='session')

def dataframe():

    dataframe = cleanTitle(readData(path='datasets', files='UdemyCleanedTitle.csv'), 'course_title', 'clean_title')
    return dataframe


# def cv_mat():   
    
#     cv_mat = ModelCountVectorizer
