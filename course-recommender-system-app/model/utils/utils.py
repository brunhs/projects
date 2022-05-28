from sklearn.feature_extraction.text import CountVectorizer

def cosineMatrix(dataframe):
    """_summary_

    Args:
        dataframe (Pandas dataframe): A Pandas dataframe

    Returns:
        Vectorized matrix: Count vectorized matrix
    """

    countvect = CountVectorizer()
    cvmat = countvect.fit_transform(dataframe['Clean_title'])
    return cvmat

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
