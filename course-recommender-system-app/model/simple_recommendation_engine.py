from model.utils.utils import extractFeatures


class SimpleSearchEngine():

    def __init__(self, search_term, amount, course):
        self.search_term = search_term.lower()
        self.amount = amount
        self.course = course

    def fit(self, dataframe):
        """
        Fit the data to the search term function.

        Args:
            dataframe (pandas.dataframe): Dataframe containing all the database.

        Returns:
            pandas.dataframe: Returns the fitted dataframe.
        """        
        self.search_dataframe = self.searchTerm(self.search_term, dataframe, self.amount, self.course)

        return self

    def transform(self):
        """
        Transform dataset into recommendations.

        Returns:
            dict: Dictionar containing recommendations.
        """        
        if self.search_dataframe.shape[0] >= self.amount:
            course_url, course_title, course_price = extractFeatures(
                self.search_dataframe.head(self.amount))
            transformed_dataframe = dict(zip(course_title, course_url))
            
        else:
            course_url, course_title, course_price = extractFeatures(
                self.search_dataframe.head(self.amount))
            transformed_dataframe = dict(zip(course_title, course_url))

        return transformed_dataframe

    def searchTerm(self, term:str, dataframe, amount:int, course:str):
        """_summary_

        Args:
            term (str): Term to be searched.
            dataframe (_type_): Pandas dataframe.
            amount (int): Amount of terms to return.

        Returns:
            Dataframe: Sorted amount of terms.
        """
        result_dataframe = dataframe[dataframe[course].str.contains(term)]
        sorted_amount = result_dataframe.sort_values(by='num_subscribers', ascending=False).head(amount)
        return sorted_amount

    def fit_transform(self, dataframe):
        self.fit(dataframe)
        transformed_dataframe = self.transform()

        return transformed_dataframe