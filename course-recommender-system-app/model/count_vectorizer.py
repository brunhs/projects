from sklearn.feature_extraction.text import CountVectorizer

class ModelCountVectorizer():
    """
    Count vectorize a matrix.
    """

    def __init__(self, column):
        self.column = column
        self.vectorizer = CountVectorizer()
    
    def fit(self, X):
        """
        Fit matrix into the counting method.

        Args:
            dataframe (dataframe): Dataframe to be counted.

        Returns:
            self: object
                Object with fitted matrix.
        """
        self.X=X

        if len(X) > 1:
            self.vectorizer.fit(self.X[self.column])
        else:
            self.vectorizer.fit(self.X)
        return self

    def transform(self, X):
        """
        Transform fit method into count arrays.

        Args:
            dataframe (matrix): Dataframe to be transformed.

        Returns:
            numpy.array: count vectorized numpy.array.
        """
        if len(X) > 1:
            vectorized_matrix = self.vectorizer.transform(X[self.column])
        else:
            vectorized_matrix = self.vectorizer.transform(X)

        return vectorized_matrix

    def fit_transform(self, X):
        """Fit and transform method into count arrays.

        Args:
            dataframe (dataframe): Dataframe to be transformed.

        Returns:
            numpy.array: count vectorized numpy.array.
        """

        self.fit(X)

        vectorized_matrix = self.transform(X)

        return vectorized_matrix