from sklearn.metrics.pairwise import cosine_similarity

class ModelCosineSimilarity():
    """
    Cosine similarity calculation of a matrix
    """
    def __init__(self):
        pass

    def transform(self, matrix):
        """
        Transform a vectorized matrix into a cosine similarity matrix

        Args:
            matrix (dataframe): Vectorized dataframe

        Returns:
            dataframe: Cosine similarit dataframe
        """

        similarity_matrix = cosine_similarity(matrix)
        return similarity_matrix
