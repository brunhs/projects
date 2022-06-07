import pandas as pd
from model.utils.utils import extractFeatures

# class recommendCourse():

#     def __init__(self):
#         pass

#     def recommendCourse(self, dataframe, title, cosine_sim_mat, numrec):

#         course_index = pd.Series(
#             dataframe.index, index=dataframe['course_title']).drop_duplicates()

#         index = course_index[title]

#         scores = list(enumerate(cosine_sim_mat[index]))

#         sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

#         selected_course_index = [i[0] for i in sorted_scores[0:]]

#         selected_course_score = [i[1] for i in sorted_scores[0:]]

#         rec_df = dataframe.iloc[selected_course_index].join(pd.DataFrame(selected_course_score,
#  index=selected_course_index, columns=['Similarity_Score']))

#         final_recommended_courses = rec_df[[
#             'course_title', 'Similarity_Score', 'url', 'price', 'num_subscribers']]

#         return final_recommended_courses.head(numrec)

class recommendCourse():

    def __init__(self):
        # self.course_dict = None
        pass
    
    def recommendCourse(self, dataframe, title, mat, numrec):

        course_index = pd.Series(
            dataframe.index, index=dataframe['course_title']).drop_duplicates()

        index = course_index[title]

        scores = list(enumerate(mat[index]))

        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

        selected_course_index = [i[0] for i in sorted_scores[0:]]

        selected_course_score = [i[1] for i in sorted_scores[0:]]

        rec_df = dataframe.iloc[selected_course_index].join(pd.DataFrame(selected_course_score,
 index=selected_course_index, columns=['Similarity_Score']))

        final_recommended_courses = rec_df[[
            'course_title', 'Similarity_Score', 'url', 'price', 'num_subscribers']].head(numrec)

        course_url, course_title, course_price = extractFeatures(final_recommended_courses)

        self.course_dict = dict(zip(course_title, course_url))

        return self.course_dict