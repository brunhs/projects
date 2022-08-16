from sklearn.metrics.pairwise import cosine_similarity

class ModelScorer():
    """
    Scorer method of the search application.
    """
    def __init__(self, method='cosine'):
        self.method=method

    def transform(self, X, y=None):
        """
        Transform a vectorized matrix into a scored matrix.

        Args:
            matrix (dataframe): Vectorized dataframe.

        Returns:
            dataframe: Scored dataframe.
        """
        if self.method=='cosine':

            similarity_matrix = cosine_similarity(X, y)

        return similarity_matrix
