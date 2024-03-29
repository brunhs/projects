import json
import urllib.request as urllib2

def landing_generator(database, schema, amount, kind:str):
    """
    Loading screen generator

    Args:
        dataframe (dataframe): Dataframe.
        amount (integer): Amount needed for recommendation.
        kind (str): Kind of the recommendation.

    Returns:
        dictionary: Dictionary containing courses informations and links.
    """
    
    if kind == 'top_rated':
        list_dict = {}
        formated_dataframe = database.session.query(schema).order_by(schema.rating.desc(), schema.rating_count.desc()).limit(amount)
                
        for i in formated_dataframe.all():
            list_dict[i.isbn]={'book_title':i.book_title,'image':i.image_url_l} 
    elif kind == 'reviewed':
        list_of_dict = {}
        formated_dataframe = database.session.query(schema).order_by(schema.rating_count.desc()).limit(amount)
        
        for i in formated_dataframe.all():
            list_dict[i.isbn]={'book_title':i.book_title,'image':i.image_url_l}
    return list_dict

def custom_id(database, schema):
    idquery = database.session.query(schema).order_by(schema.user_id.desc()).first()
    last_id = int(idquery.user_id)
    next_id = int(last_id) + 1
    return last_id, next_id

def isbn_information_parser(isbn, database, schema):
    response_string = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}'
    xml = urllib2.urlopen(response_string)
    book_data = json.load(xml)

    results = dict()
    if 'items' in book_data:
        results['isbn'] = isbn
        try:
            results['title'] = book_data.get('items')[0].get('volumeInfo').get('title')
            results['publication_date'] = book_data.get('items')[0].get('volumeInfo').get('publishedDate')
            results['authors'] = book_data.get('items')[0].get('volumeInfo').get('authors')
            results['description'] = book_data.get('items')[0].get('volumeInfo').get('description')
            results['image_url'] = book_data.get('items')[0].get('volumeInfo').get('imageLinks').get('thumbnail')
        except:
            pass
    else:
        book_query=database.session.query(schema).filter(schema.isbn == isbn).first()
        results['isbn'] = isbn
        results['title'] = book_query.book_title
        results['publication_date'] = book_query.year_of_publication
        results['authors'] = book_query.book_author
        results['image_url'] = book_query.image_url_l

    return results