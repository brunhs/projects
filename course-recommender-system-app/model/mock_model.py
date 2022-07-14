from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class Recommender():
    """
    Esse cara substituiria a parte de calcular os recomendados tanto do model quanto do simple_recommendation_engine
    Ele recebe a query e retorna os indices do dataframe, teria q ter uma outra lógica pra ajeitar essas infos
    """
    def __init__(self, cv_model, cv_mat):
        self.cv_model = cv_model  # modelo pra transformar string de input
        self.cv_mat = cv_mat  # vetores dos cursos disponiveis

    def _transform_input(self, input_str):
        """Recebe uma string que é uma busca e transforma num vetor"""
        return cv_model.transform(input_str)  # Teria que mudar o código do modelo pra aceitar string além de coluna!

    def _compute_scores(self, input_vec):
        """
        Recebe o vetor de uma busca e retorna os scores de proximidade de cada curso
        Assim a gente só precisa calcular a distancia 1-pra-N (uma entrada pra N cursos) em vez de N-pra-N
        """
        return cosine_similarity(input_vec, self.cv_mat)

    def recommend(self, input_str, n_results=6):
        """
        retorna os índices dos top 6 cursos pela proximidade com a query/input
        outra função ou classe cuidaria de pegar as informações certinho do DF
        """
        scores = self._compute_scores(self._transform_input(input_str))
        indices = np.argsort(scores[::-1][:n_results])  # essa linha é meio estranha, mas é pra pegar os top N indices
        return indices

