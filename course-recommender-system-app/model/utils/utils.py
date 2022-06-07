from flask import render_template

def extractFeatures(rec_dataframe):
    """_summary_

    Args:
        rec_dataframe (Pandas dataframe): A Pandas dataframe

    Returns:
        url, title and prie: Returns informations
    """

    course_url = list(rec_dataframe['url'])
    course_title = list(rec_dataframe['course_title'])
    course_price = list(rec_dataframe['price'])

    return course_url, course_title, course_price

def dictMapRender(dictmap, titlename):

    if dictmap is None and titlename is None:
        print('first')
        return render_template('index.html')

    elif len(dictmap) != 0:
        print('second')
        return render_template('index.html', coursemap=dictmap, coursename=titlename, showtitle=True)

    else:
        print('third')
        return render_template('index.html', showerror=True, coursename=titlename)
