import pandas as pd
from model.utils.utils import extractFeatures

class RecommendCourse():
    """
    Recommend courses based on perfect name match.
    """

    def __init__(self, title, numrec):
        self.title = title
        self.numrec = numrec
    
    def _enumerate_courses(self, dataframe, similarity_matrix):
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

        return selected_course_index, selected_course_score
        
    def transform(self, dataframe, similarity_matrix):
        selected_course_index, selected_course_score = self._enumerate_courses(dataframe, similarity_matrix)

        rec_df = dataframe.iloc[selected_course_index].join(pd.DataFrame(selected_course_score,
             index=selected_course_index, columns=['Similarity_Score']))

        final_recommended_courses = rec_df[[
            'course_title', 'Similarity_Score', 'url', 'price', 'num_subscribers']].head(self.numrec)

        course_url, course_title, course_price = extractFeatures(final_recommended_courses)

        transformed_dict = dict(zip(course_title, course_url))

        return transformed_dict