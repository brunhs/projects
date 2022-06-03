from sklearn.metrics.pairwise import cosine_similarity

class ModelCosineSimilarity():

    def __init__(self, X, y):
        self.X = X
        self.y = y

    def transform(self):

        similarity_matrix = cosine_similarity(self.X, self.y)
        return similarity_matrix