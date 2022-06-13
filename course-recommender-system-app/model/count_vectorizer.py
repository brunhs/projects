from sklearn.feature_extraction.text import CountVectorizer

class ModelCountVectorizer():
    """
    Count vectorize a matrix.
    """

    def __init__(self, column):
        self.column = column
        self.vectorizer = CountVectorizer()
    
    def fit(self, dataframe):
        """
        Fit matrix into the counting method.

        Args:
            dataframe (dataframe): Dataframe to be counted.

        Returns:
            self: object
                Object with fitted matrix.
        """
        
        self.vectorizer_fit = self.vectorizer.fit(dataframe[self.column])
        return self

    def transform(self, dataframe):
        """
        Transform fit method into count arrays.

        Args:
            dataframe (matrix): Dataframe to be transformed.

        Returns:
            numpy.array: count vectorized numpy.array.
        """

        vectorized_matrix = self.vectorizer_fit.transform(dataframe[self.column])
        return vectorized_matrix

    def fit_transform(self, dataframe):
        """Fit and transform method into count arrays.

        Args:
            dataframe (dataframe): Dataframe to be transformed.

        Returns:
            numpy.array: count vectorized numpy.array.
        """

        self.fit(dataframe)

        vectorized_matrix = self.transform(dataframe)

        return vectorized_matrix
