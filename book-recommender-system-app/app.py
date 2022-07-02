from flask import Flask, render_template, request, session, request
from flask_sqlalchemy import SQLAlchemy
from model.utils.utils import landing_generator, custom_id
import uuid
import pandas as pd

app = Flask(__name__)

app.config.from_object('config.DevConfig')

book_user_rating = pd.read_csv('datasets/Book_user_rating.csv')

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

        single_user = User(uuid=user_uuid,firstname=firstname,lastname=lastname, user_id=user_id)
        db.session.add(single_user)
        db.session.commit()
        session['firstname'] = firstname
        session['lastname'] = lastname
        session['uuid'] = user_uuid
    return render_template('register.html', firstname=firstname, lastname=lastname)

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

        bookmap = landing_generator(book_user_rating, amount=6, kind='top_rated')

        return render_template('main.html', firstname=firstname, lastname=lastname, bookmap=bookmap, ratings=ratings_list)

    if request.method == 'POST':
        star1 = request.form('star')

        print(star1)
        bookmap = landing_generator(book_user_rating, amount=6, kind='top_rated')

        return render_template('main.html', firstname=firstname, lastname=lastname, bookmap=bookmap)

@app.route('/about')
def about():
    mission = 'Optimizing Data and ML Model'
    return render_template('about.html', mission=mission)

@app.route('/profile/<fname>')
def profile():
    user = User.query.filter_by(fname=fname).first()
    return render_template('profile.html',user=user)





if __name__ == '__main__':
    app.run(debug=True)