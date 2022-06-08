from sklearn.feature_extraction.text import CountVectorizer

class ModelCountVectorizer():

    def __init__(self, column):
        self.column = column
    
    def fit(self, dataframe):
        
        self.vectorizer_fit = CountVectorizer().fit(dataframe[self.column])
        return self

    def transform(self, dataframe):

        vectorized_matrix = self.vectorizer_fit.transform(dataframe[self.column])
        return vectorized_matrix

    def fit_transform(self, dataframe):

        self.fit(dataframe)

        vectorized_matrix = self.transform(dataframe)

        return vectorized_matrix
