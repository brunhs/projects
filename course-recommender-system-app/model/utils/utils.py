from flask import render_template

def landing_generator(dataframe, amount, kind:str):
    """
    Loading screen generator.

    Args:
        dataframe (dataframe): Dataframe.
        amount (integer): Amount needed for recommendation.
        kind (str): Kind of the recommendation.

    Returns:
        dictionary: Dictionary containing courses informations and links.
    """
    if kind == 'top_paid':
        formated_dataframe = dataframe.loc[dataframe['is_paid'] == 'True',:].sort_values('num_reviews', ascending=False).head(amount)
        final_dict = dict(zip(formated_dataframe.course_title, formated_dataframe.url))
    elif kind == 'watching':
        formated_dataframe = dataframe.sort_values('num_subscribers', ascending=False).head(6).loc[:,['course_title', 'url']]
        final_dict = dict(zip(formated_dataframe.course_title, formated_dataframe.url))
    return final_dict

def extractFeatures(rec_dataframe):
    """
    Extract dataframe features such as url, title and price.

    Args:
        rec_dataframe (Pandas dataframe): A Pandas dataframe.

    Returns:
        url, title and price: Returns informations.
    """

    course_url = list(rec_dataframe['url'])
    course_title = list(rec_dataframe['course_title'])
    course_price = list(rec_dataframe['price'])

    return course_url, course_title, course_price