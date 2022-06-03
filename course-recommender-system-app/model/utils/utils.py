from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def cosineSimMat(dataframe, column:str):
    """_summary_

    Args:
        dataframe (Pandas dataframe): A Pandas dataframe

    Returns:
        Vectorized matrix: Count vectorized matrix
    """
    
    countvect = CountVectorizer()
    cvmat = countvect.fit_transform(dataframe[column])
    return cosine_similarity(cvmat)

def extractFeatures(rec_dataframe):
    """_summary_

    Args:
        rec_dataframe (Pandas dataframe): A Pandas dataframe

    Returns:
        url, title and prie: Returns informations
    """

    course_url = list(rec_dataframe['url'])
    course_title = list(rec_dataframe['course_title'])
    course_price = list(rec_dataframe['price'])

    return course_url, course_title, course_price