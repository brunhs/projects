from flask import Flask, render_template, request, session, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from model.utils.utils import landing_generator, custom_id, get_google_api_results
import uuid
import pandas as pd

app = Flask(__name__)

app.config.from_object('config.DevConfig')

# book_user_rating = pd.read_csv('datasets/Book_user_rating.csv')

# database
db = SQLAlchemy(app)

# user schema
class User(db.Model):
    __tablename__= 'user'
    user_id=db.Column(db.Integer, primary_key=True)
    location=db.Column(db.String(50))
    age=db.Column(db.Float)
    uuid=db.Column(db.String(50), primary_key=True)
    firstname=db.Column(db.String(50))
    lastname=db.Column(db.String(50))

    def __init__(self, uuid, firstname, lastname, user_id):
        self.uuid = uuid
        self.firstname = firstname
        self.lastname = lastname
        self.user_id = user_id


# rating schema
class Rating(db.Model):
    __tablename__= 'rating'
    user_id=db.Column(db.String(50))
    isbn=db.Column(db.String(50))
    book_rating=db.Column(db.Integer)
    location=db.Column(db.String(50))
    age=db.Column(db.Float)
    uuid=db.Column(db.String(50), primary_key=True)
    rating_uuid=db.Column(db.String(50))
    timestamp=db.Column(db.DateTime)

    def __init__(self,  isbn, book_rating, uuid, rating_uuid, timestamp):
        self.isbn = isbn
        self.book_rating = book_rating
        self.uuid = uuid
        self.rating_uuid = rating_uuid
        self.timestamp = timestamp

# Search schema
class Search(db.Model):
    __tablename__= 'search'
    user_id=db.Column(db.String(50), primary_key=True)
    search=db.Column(db.String(50))
    time=db.Column(db.DateTime)
    def __init__(self, uuid, fname, lname):
        self.uuid = uuid
        self.fname = fname
        self.lname = lname

# rating schema
class Books(db.Model):
    __tablename__= 'book'
    isbn=db.Column(db.String(200), primary_key=True)
    book_title=db.Column(db.String(200))
    book_author=db.Column(db.String(200))
    year_of_publication=db.Column(db.Integer)
    publisher=db.Column(db.String(200))
    image_url_s=db.Column(db.String(200))
    image_url_m=db.Column(db.String(200))
    image_url_l=db.Column(db.String(200))
    rating=db.Column(db.Float)
    rating_count=db.Column(db.Float)

    def __init__(self, isbn, book_title, book_author, year_of_publication, publisher,
     image_url_s, image_url_m, image_url_l, rating, rating_count):
        self.isbn = isbn
        self.book_title = book_title
        self.book_author = book_author
        self.year_of_publication = year_of_publication
        self.publisher = publisher
        self.image_url_s = image_url_s
        self.image_url_m = image_url_m
        self.image_url_l = image_url_l
        self.rating = rating
        self.rating_count = rating_count



# route
@app.route('/')
def index():
    return render_template('register.html')

# user registration
@app.route('/register',methods=['GET','POST'])
def register():

    if request.method == 'POST':
        
        index, user_id = custom_id(database=db, schema=User)
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        user_uuid = uuid.uuid4().hex
        if firstname == '' or lastname == '':
            return render_template('register.html', message='Please include your first name AND your last name.')
      
        if firstname != '' or lastname != '':
            single_user = User(uuid=user_uuid,firstname=firstname,lastname=lastname, user_id=user_id)
            db.session.add(single_user)
            db.session.commit()
            session['firstname'] = firstname
            session['lastname'] = lastname
            session['uuid'] = user_uuid
            return render_template('register.html', message=f'Hi {firstname} {lastname}, welcome back!'), {"Refresh": "5; url=main"}

    return render_template('register.html')

@app.route('/main',methods=['GET','POST'])
def main():
    if request.method == 'GET':
        firstname = session.get('firstname')
        lastname = session.get('lastname')

        # recuperando informação
        ratings = db.session.query(Rating).filter(Rating.user_id == 276725).all()
        ratings_list = []
        for i in ratings:
            ratings_list.append([i.isbn, i.book_rating])

        # salvando informação
        print(session.get('uuid'))
        # user_rating = Rating(isbn=, book_rating=, uuid=, rating_uuid=, timestamp=)

        bookmap = landing_generator(db, Books, 6, 'top_rated')

        # print(bookmap[0]['isbn'])
        return render_template('main.html', firstname=firstname, lastname=lastname, bookmap=bookmap, ratings=ratings_list)

    if request.method == 'POST':
  
        bookmap = landing_generator(db, Books, 6, 'top_rated')

        return render_template('main.html', firstname=firstname, lastname=lastname, bookmap=bookmap)

@app.route('/about')
def about():
    mission = 'Optimizing Data and ML Model'
    return render_template('about.html', mission=mission)

@app.route('/profile/<fname>')
def profile():
    user = User.query.filter_by(fname=fname).first()
    return render_template('profile.html',user=user)

@app.route('/book_view/<isbn>',methods=['POST', 'GET'])
def book_view(isbn):


    ggapi = get_google_api_results(isbn)

    # if request.method == 'POST':
        
    #     user_id = request.form['rating']
    #     user_id = request.form['rating']
    #     user_uuid = uuid.uuid4().hex
    #     book_isbn = isbn
    #     if firstname == '' or lastname == '':
    #         return render_template('register.html', message='Please include your first name AND your last name.')

    return render_template('book_view.html', book=ggapi)



if __name__ == '__main__':
    app.run(debug=True)