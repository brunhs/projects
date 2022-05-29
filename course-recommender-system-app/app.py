from flask import Flask, request, render_template
from dashboard import getvaluecounts, getlevelcount, getsubjectsperlevel, yearwiseprofit
from model.data_preparation.data_preparation import readData, titleManipulation, cosineSimMat, searchTerm
from model.utils.utils import extractFeatures
from model.model import recommendCourse

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello_world():

    if request.method == 'POST':

        my_dict = request.form
        titlename = my_dict['course']
        print(titlename)
        try:
            df = readData('UdemyCleanedTitle.csv')
            df = titleManipulation(df)
            cvmat = cosineSimMat(df)

            cosine_mat = cosineSimMat(cvmat)

            recdf = recommendCourse().recommendCourse(df, titlename,
                                     cosine_mat, 6)

            course_url, course_title, course_price = extractFeatures(recdf)

            dictmap = dict(zip(course_title, course_url))

            if len(dictmap) != 0:
                return render_template('index.html', coursemap=dictmap, coursename=titlename, showtitle=True)

            else:
                return render_template('index.html', showerror=True, coursename=titlename)

        except:

            resultdf = searchTerm(titlename, df, 6)
            if resultdf.shape[0] > 6:
                resultdf = resultdf.head(6)
                course_url, course_title, course_price = extractFeatures(
                    resultdf)
                coursemap = dict(zip(course_title, course_url))
                if len(coursemap) != 0:
                    return render_template('index.html', coursemap=coursemap, coursename=titlename, showtitle=True)

                else:
                    return render_template('index.html', showerror=True, coursename=titlename)

            else:
                course_url, course_title, course_price = extractFeatures(
                    resultdf)
                coursemap = dict(zip(course_title, course_url))
                if len(coursemap) != 0:
                    return render_template('index.html', coursemap=coursemap, coursename=titlename, showtitle=True)

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
