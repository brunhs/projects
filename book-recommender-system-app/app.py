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
    user_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
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


# click schema
class Ratings(db.Model):
    __tablename__= 'rating'
    col_id=db.Column(db.String(50), primary_key=True)
    uuid=db.Column(db.String(50))
    fname=db.Column(db.String(50))
    lname=db.Column(db.String(50))
    book_id=db.Column(db.Integer)
    isbn=db.Column(db.Integer)
    rate=db.Column(db.Integer)

    def __init__(self, col_id, uuid, book_id, isbn, rate, firstname):
        self.col_id = col_id
        self.user_id = user_id
        self.book_id = book_id
        self.isbn = isbn
        self.rate = rate
        self.firstname = firstname


# Search schema
class Searchs(db.Model):
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

        user_id = custom_id()
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        if firstname == '' or lastname == '':
            return render_template('register.html', message='Please include your first name AND your last name.')

        single_user = User(uuid=uuid.uuid4().hex,firstname=firstname,lastname=lastname, user_id=user_id)
        db.session.add(single_user)
        db.session.commit()
        session['firstname'] = firstname
        session['lastname'] = lastname
    return render_template('register.html', firstname=firstname, lastname=lastname)

@app.route('/main',methods=['GET','POST'])
def main():
    if request.method == 'GET':
        firstname = session.get('firstname')
        lastname = session.get('lastname')

        bookmap = landing_generator(book_user_rating, amount=6, kind='top_rated')

        return render_template('main.html', firstname=firstname, lastname=lastname, bookmap=bookmap)

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