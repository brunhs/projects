from flask import Flask, request, render_template
from model.data_preparation.data_preparation import readData, titleManipulation
from model.utils.utils import landing_generator
from model.model import RecommendCourse
from model.cosine_similarity import ModelCosineSimilarity
from model.count_vectorizer import ModelCountVectorizer
from model.simple_recommendation_engine import SimpleSearchEngine
from os import environ

app = Flask(__name__)

df = titleManipulation(readData(files='UdemyCleanedTitle.csv'), 'course_title', 'Clean_title')
cv_mat = ModelCountVectorizer('Clean_title').fit_transform(dataframe=df)
cosine_mat = ModelCosineSimilarity().transform(cv_mat)


@app.route('/', methods=['GET', 'POST'])
def hello_world():

    if request.method == 'POST':

        myDict = request.form
        titlename = myDict['course']
        try:
            print('Trying first solution')                

            recdf = RecommendCourse(titlename, 6).transform(df, cosine_mat)

            return render_template('index.html', coursemap=recdf, coursename=titlename, showtitle=True)

        except Exception as e:
            print('Trying second solution')

            dictmap = SimpleSearchEngine(titlename, 6, 'Clean_title').fit(df).transform()

            return render_template('index.html', coursemap=dictmap, coursename=titlename, showtitle=True)


    elif request.method == 'GET':

        top_courses_dictmap = landing_generator(df, 6, 'top_paid')
        watching_dictmap = landing_generator(df, 6, 'watching')

        return render_template('prescreen.html', first_coursemap=top_courses_dictmap, second_coursemap=watching_dictmap, showtitle=False)


if __name__ == '__main__':
    app.run(debug=True, port=environ.get("PORT", 5000), host="0.0.0.0")