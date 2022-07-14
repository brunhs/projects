from sklearn.metrics.pairwise import cosine_similarity


# Esse cara não precisa necessariamente ser um modelo
# pelo menos não desse jeito (só aplicando 1 função)
# Acho que o que seria interessante seria tipo um ModelScorer(method)
# E aí o "method" seleciona se é cosine_similarity ou alguma outra métrica que vc pode ir adicionando
# assim faria mais sentido tb ser um objeto permanente, pq ele grava o método
#
# E seria legal poder passar X, Y=None
# que nem na própria função
# https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html
# daí pra fazer 1-pra-N ou N-pra-N

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
