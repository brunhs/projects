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
        # os .fit do sklearn sempre são inplace, ou seja, aqui vc acaba com um self.vectorizer_fit == self.vectorizer
        # então dá pra rodar só o fit
        return self

    def transform(self, dataframe):
        """
        Transform fit method into count arrays.

        Args:
            dataframe (matrix): Dataframe to be transformed.

        Returns:
            numpy.array: count vectorized numpy.array.
        """
        #############
        # importante!
        # aqui vc só tem a opção de transformar um df, acho que é mais versátil (e necessário pra solução q a gente
        #   conversou) se tiver um jeito de converter uma string tb
        # eu acho que a "api" ideal seria ter um fit_transform q funcionasse pra uma lista, e aí vc passa
        # ou algo tipo transform([query]) ou transform(df[column])
        #############
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
