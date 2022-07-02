def landing_generator(dataframe, amount, kind:str):
    """
    Loading screen generator

    Args:
        dataframe (dataframe): Dataframe.
        amount (integer): Amount needed for recommendation.
        kind (str): Kind of the recommendation.

    Returns:
        dictionary: Dictionary containing courses informations and links.
    """

    transformed_dataset = dataframe.groupby(
    ['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher',
       'Image-URL-S', 'Image-URL-M', 'Image-URL-L']
       )\
           .agg({'Book-Rating':['mean', 'count']})


    if kind == 'top_rated':
        formated_dataframe = transformed_dataset.sort_values(by=[('Book-Rating', 'mean'),('Book-Rating', 'count'), 'Year-Of-Publication'], ascending=False).head(amount)\
            .droplevel(level=0, axis=1).reset_index().loc[:,['Book-Title', 'Image-URL-L']]
        final_dict = dict(zip(formated_dataframe['Book-Title'], formated_dataframe['Image-URL-L']))
 
    elif kind == 'reviewed':
        formated_dataframe = transformed_dataset.sort_values(by=[('Book-Rating', 'count'),('Book-Rating', 'mean'), 'Year-Of-Publication'], ascending=False).head(amount)\
            .droplevel(level=0, axis=1).reset_index().loc[:,['Book-Title', 'Image-URL-L']]
        final_dict = dict(zip(formated_dataframe['Book-Title'], formated_dataframe['Image-URL-L']))
    return final_dict


def custom_id(database, schema):
    idquery = database.session.query(schema).order_by(schema.user_id.desc()).first()
    last_id = int(idquery.user_id)
    next_id = int(last_id) + 1
    return last_id, next_id
