from flask import Flask, request, render_template
from dashboard import getvaluecounts, getlevelcount, getsubjectsperlevel, yearwiseprofit
from model.data_preparation.data_preparation import readData, titleManipulation, searchTerm
from model.utils.utils import extractFeatures, dictMapRender
from model.model import recommendCourse
from model.cosine_similarity import ModelCosineSimilarity
from model.count_vectorizer import ModelCountVectorizer

app = Flask(__name__)

df = readData('UdemyCleanedTitle.csv')
df = titleManipulation(df, 'course_title', 'Clean_title')


@app.route('/', methods=['GET', 'POST'])
def hello_world():

    if request.method == 'POST':

        myDict = request.form
        try:
            
            print('Trying first solution')

            titlename = myDict['course']
    
            print(titlename)
            
            #modificar essa parte

            cv_mat = ModelCountVectorizer('Clean_title').fit_transform(dataframe=df)

            cosine_mat = ModelCosineSimilarity().transform(cv_mat)

            recdf = recommendCourse().recommendCourse(df, titlename, cosine_mat, 6)

            if len(recdf) != 0:
                return render_template('index.html', coursemap=recdf, coursename=titlename, showtitle=True)

            else:
                return render_template('index.html', showerror=True, coursename=titlename)

        # modificar essa excessão
        except Exception as e:
            print(e)
            print('Trying second solution')

            titlename = myDict['course'].lower()

        # modificar essa parte
            resultdf = searchTerm(titlename, df, 6, 'Clean_title')
            if resultdf.shape[0] > 6:
                resultdf = resultdf.head(6)
                course_url, course_title, course_price = extractFeatures(
                    resultdf)
                dictmap = dict(zip(course_title, course_url))

                if len(dictmap) != 0:
                    return render_template('index.html', coursemap=dictmap, coursename=titlename, showtitle=True)

                else:
                    return render_template('index.html', showerror=True, coursename=titlename)

        # modificar essa parte
            else:
                course_url, course_title, course_price = extractFeatures(
                    resultdf)
                dictmap = dict(zip(course_title, course_url))

                if len(dictmap) != 0:
                    return render_template('index.html', coursemap=dictmap, coursename=titlename, showtitle=True)

                else:
                    return render_template('index.html', showerror=True, coursename=titlename)

    return render_template('index.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    df = readData('UdemyCleanedTitle.csv')
    valuecounts = getvaluecounts(df)

    levelcounts = getlevelcount(df)

    subjectsperlevel = getsubjectsperlevel(df)

    yearwiseprofitmap, subscriberscountmap, profitmonthwise, monthwisesub = yearwiseprofit(
        df)

    return render_template('dashboard.html', valuecounts=valuecounts, levelcounts=levelcounts,
                           subjectsperlevel=subjectsperlevel, yearwiseprofitmap=yearwiseprofitmap, subscriberscountmap=subscriberscountmap, profitmonthwise=profitmonthwise, monthwisesub=monthwisesub)


if __name__ == '__main__':
    app.run(debug=True)