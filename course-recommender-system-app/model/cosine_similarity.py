from sklearn.metrics.pairwise import cosine_similarity

class ModelCosineSimilarity():

    def __init__(self):
        pass

    def transform(self, matrix):

        similarity_matrix = cosine_similarity(matrix)
        return similarity_matrix
