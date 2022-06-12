from flask import render_template

def landing_generator(df, amount, kind:str):
    if kind == 'top_paid':
        formated_df = df.loc[df['is_paid'] == 'True',:].sort_values('num_reviews', ascending=False).head(amount)
        final_dict = dict(zip(formated_df.course_title, formated_df.url))
    elif kind == 'watching':
        formated_df = df.sort_values('num_subscribers', ascending=False).head(6).loc[:,['course_title', 'url']]
        final_dict = dict(zip(formated_df.course_title, formated_df.url))
    return final_dict

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
