from flask import Flask, render_template, request, session, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from model.utils.utils import landing_generator, custom_id, isbn_information_parser
import uuid
from sqlalchemy import func
import datetime

app = Flask(__name__)

app.config.from_object('config.DevConfig')

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

    def __init__(self, user_id,  isbn, book_rating, uuid, rating_uuid, timestamp):
        self.user_id = user_id
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
class Book(db.Model):
    __tablename__= 'book'
    index=db.Column(db.Integer)
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

    def __init__(self, index, isbn, book_title, book_author, year_of_publication, publisher,
     image_url_s, image_url_m, image_url_l, rating, rating_count):
        self.index=index
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
            session['user_id'] = user_id
            return render_template('register.html', message=f'Hi {firstname} {lastname}, welcome back!'), {"Refresh": "3; url=main"}

    return render_template('register.html')

@app.route('/main',methods=['GET','POST'])
def main():
    if request.method == 'GET':
        firstname = session.get('firstname')
        lastname = session.get('lastname')

        # recuperando informação
        # ajustar isso para que recuperemos informação de maneira diferente
        ratings = db.session.query(Rating).filter(Rating.user_id == 276725).all()
        ratings_list = []
        for i in ratings:
            ratings_list.append([i.isbn, i.book_rating])

        # salvando informação
        print(session.get('uuid'))

        bookmap = landing_generator(db, Book, 6, 'top_rated')

        return render_template('main.html', firstname=firstname, lastname=lastname, bookmap=bookmap)

    if request.method == 'POST':
  
        bookmap = landing_generator(db, Book, 6, 'top_rated')

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

    # ajustar isso para recuperar informação do datalake caso a api não funcione
    isbn_information=isbn_information_parser(isbn, database=db, schema=Book)


    if request.method == 'POST':
        
        rating=int(request.form['rating'])*2
        user_uuid=session.get('uuid')
        book_isbn=isbn
        rating_uuid=uuid.uuid4().hex
        timestamp=datetime.datetime.now()
        user_id=session.get('user_id')

        print(rating, user_uuid, book_isbn, rating_uuid, timestamp, user_id)
        
        # agora precisamos salvar a nova avaliação baseado no uuid, isbn
        book_rates = Rating(user_id = user_id, isbn=book_isbn, book_rating=rating, uuid=user_uuid, rating_uuid=rating_uuid, timestamp=timestamp)
        db.session.add(book_rates)
        db.session.commit()

        # get altered isbn number
        altered_isbn = db.session.query(Rating).order_by(Rating.timestamp.desc()).first().isbn

        # bring all the data from that isbn number
        new_book_rate = db.session.query(Rating.isbn, func.avg(Rating.book_rating), func.count(Rating.book_rating))\
            .filter(Rating.isbn == altered_isbn).first()

        # bring all book data based on last isbn
        book_to_update = db.session.query(Book)\
            .filter(Book.isbn == book_isbn)

        book_to_update.update({"rating":round(new_book_rate[1],0), "rating_count":new_book_rate[2]})

        db.session.commit() 

        return render_template('book_view.html', message=f"Thank you for your vote! You'll be redirected in 3 seconds", book=isbn_information), {"Refresh": "3; url=../main"}

    return render_template('book_view.html', book=isbn_information)



if __name__ == '__main__':
    app.run(debug=True)