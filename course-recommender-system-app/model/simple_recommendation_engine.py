from model.utils.utils import extractFeatures
from model.data_preparation.data_preparation import searchTerm

class SimpleSearchEngine():

    def __init__(self, search_term, amount, course):
        self.search_term = search_term.lower()
        self.amount = amount
        self.course = course

    def fit(self, dataframe):
        self.search_dataframe = searchTerm(self.search_term, dataframe, self.amount, self.course)

        return self

    def transform(self):
        if self.search_dataframe.shape[0] >= self.amount:
            course_url, course_title, course_price = extractFeatures(
                self.search_dataframe.head(self.amount))
            transformed_dataframe = dict(zip(course_title, course_url))
            
        else:
            course_url, course_title, course_price = extractFeatures(
                self.search_dataframe.head(self.amount))
            transformed_dataframe = dict(zip(course_title, course_url))

        return transformed_dataframe

    def fit_transform(self, dataframe):
        self.fit(dataframe)
        transformed_dataframe = self.transform()

        return transformed_dataframe
