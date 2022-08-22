from model.utils.utils import extractFeatures
import pandas as pd

class Recommender():
    """
    Recommender class responsible for calculating a recommendation for the user, using it's search interest.
    
    """
    def __init__(self, cv_model, cv_mat, dataframe, scorer_class):
        self.cv_model = cv_model
        self.cv_mat = cv_mat
        self.dataframe = dataframe
        self.scorer = scorer_class

    def _transform_input(self, input_str):
        """
        Receives a search string and returns a vector.

        Args:
            input_str (string): String containing the search.

        Returns:
            array: Returns the vectorized transformed array.
        """        
        return self.cv_model.transform([input_str])

    def _compute_scores(self, input_vec):
        """
        Receives the search vector and computes the similarities with the whole matrix.

        Args:
            input_vec (array): Input of count vector.

        Returns:
            array: Similarity array.
        """        
        return self.scorer.transform(self.cv_mat, input_vec)

    def _score_to_dict(self, dataframe, course_index, course_score):


        rec_df = dataframe.iloc[course_index].join(pd.DataFrame(course_score,
             index=course_index, columns=['similarity_score']))

        final_recommended_courses = rec_df[[
            'course_title', 'similarity_score', 'url', 'price', 'num_subscribers']]

        course_url, course_title, course_price = extractFeatures(final_recommended_courses)

        transformed_dict = dict(zip(course_title, course_url))

        return transformed_dict


    def recommend(self, input_str, n_results=6, column_name='scores'):
        """
        Returns the indexes of the top courses based on their proximity.

        Args:
            input_str (string): User search string.
            n_results (int, optional): Amount of results required by the user. Defaults to 6.
            column_name (str, optional): Column name for proximity scores. Defaults to 'scores'.

        Returns:
            dict: Dict containing user proximal results.
        """
        scores = pd.DataFrame(self._compute_scores(self._transform_input(input_str)), columns=[column_name])
        ordered_scores = scores[scores>0].dropna().sort_values(by=column_name, ascending=False)
        top_indexes = ordered_scores[:n_results].index
        top_scores = ordered_scores[:n_results].values
        recommended_courses = self._score_to_dict(self.dataframe, top_indexes, top_scores)
        
        return recommended_courses