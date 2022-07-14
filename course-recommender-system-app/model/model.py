import pandas as pd
from model.utils.utils import extractFeatures

class RecommendCourse():
    """
    Recommend courses based on perfect name match.
    """

    def __init__(self, title, numrec):
        self.title = title
        self.numrec = numrec
    
    def transform(self, dataframe, similarity_matrix):
        """
        Transform dataframe into recommendation dataframe.

        Args:
            dataframe (dataframe): Dataframe containing all courses informations.
            similarity_matrix (dataframe): Dataframe containing similarity informations.

        Returns:
            dictionar: Recommended courses dictionary
        """

        course_index = pd.Series(
            dataframe.index, index=dataframe['course_title']).drop_duplicates()

        index = course_index[self.title]

        scores = list(enumerate(similarity_matrix[index]))

        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

        selected_course_index = [i[0] for i in sorted_scores[0:]]

        selected_course_score = [i[1] for i in sorted_scores[0:]]

        # Essa parte daqui pra frente é só ajuste de dado, né? podia ser um método separado
        # daí então teria um método que calcula o score, seleciona os recomendados
        # e outro que prepara pro display
        rec_df = dataframe.iloc[selected_course_index].join(pd.DataFrame(selected_course_score,
             index=selected_course_index, columns=['Similarity_Score']))

        final_recommended_courses = rec_df[[
            'course_title', 'Similarity_Score', 'url', 'price', 'num_subscribers']].head(self.numrec)

        course_url, course_title, course_price = extractFeatures(final_recommended_courses)

        transformed_dict = dict(zip(course_title, course_url))

        return transformed_dict