from flask import Flask, request, render_template
from model.data_preparation.data_preparation import readData, cleanTitle
from model.utils.utils import landing_generator
from model.model import Recommender
from model.count_vectorizer import ModelCountVectorizer
from model.scorer import ModelScorer
from os import environ

app = Flask(__name__)

dataframe = cleanTitle(readData(files='UdemyCleanedTitle.csv'), 'course_title', 'clean_title')
cv_mat = ModelCountVectorizer('clean_title').fit_transform(dataframe)
cv_model = ModelCountVectorizer('clean_title').fit(dataframe)

@app.route('/', methods=['GET', 'POST'])
def courses_app():

    if request.method == 'POST':

        my_dict = request.form
        request_string = my_dict['course']
        recdf = Recommender(cv_model=cv_model, cv_mat=cv_mat, dataframe=dataframe, scorer_class=ModelScorer()).recommend(request_string)

        return render_template('index.html', coursemap=recdf, coursename=request_string, showtitle=True)


    elif request.method == 'GET':

        top_courses_dictmap = landing_generator(dataframe, 6, 'top_paid')
        watching_dictmap = landing_generator(dataframe, 6, 'watching')

        return render_template('prescreen.html', first_coursemap=top_courses_dictmap, second_coursemap=watching_dictmap, showtitle=False)


if __name__ == '__main__':
    app.run(debug=False, port=environ.get("PORT", 5000), host="0.0.0.0")