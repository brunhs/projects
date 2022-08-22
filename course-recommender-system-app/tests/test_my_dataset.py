from model.count_vectorizer import ModelCountVectorizer

def test_shape_of_dataframe(dataframe):
    assert dataframe.shape == (3683,14)

def test_dataframe_features(dataframe):
    assert dataframe.columns.to_list() == ['course_id', 'course_title', 'url', 'is_paid', 'price',
       'num_subscribers', 'num_reviews', 'num_lectures', 'level',
       'content_duration', 'published_timestamp', 'subject', 'Clean_title', 'clean_title']

def test_count_vectorizer_mat(dataframe):
    assert ModelCountVectorizer('clean_title').fit_transform(dataframe).shape == (3683, 3564)