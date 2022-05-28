import pandas as pd
import neattext.functions as nfx
from sklearn.metrics.pairwise import cosine_similarity


def readData(file: str, extension='.csv'):
    """_summary_

    Args:
        file (str): Required file to read
        extension (str, optional): Extension of the required file. Defaults to '.csv'.

    Returns:
        A Pandas dataframe
    """
    if extension=='.csv':
        read_func = pd.read_csv

    return read_func(file)

def titleManipulation(dataframe, column:str):
    """_summary_

    Args:
        dataframe (Pandas): Pandas dataframe
        column (str): Column to be modified

    Returns:
        Dataframe: Column modified dataframe
    """
    dataframe[column] = dataframe[column].apply(nfx.remove_stopwords)
    dataframe[column] = dataframe[column].apply(nfx.remove_special_characters)
    dataframe[column] = dataframe[column].apply(nfx.remove_puncts)
    dataframe[column] = dataframe[column].apply(nfx.remove_emojis)

    return dataframe


def cosineSimMat(dataframe):
    """_summary_

    Args:
        dataframe (Pandas): Pandas dataframe

    Returns:
        cosine similarity matrix: Returns cosine similarity matrix
    """

    return cosine_similarity(dataframe)


def searchTerm(term:str, dataframe, amount:int):
    """_summary_

    Args:
        term (str): Term to be searhhed
        dataframe (_type_): Pandas dataframe
        amount (int): Amount of terms to return

    Returns:
        Dataframe: Sorted amount of terms
    """
    result_dataframe = dataframe[dataframe['course_title'].str.contains(term)]
    sorted_amount = result_dataframe.sort_values(by='num_subscribers', ascending=False).head(amount)
    return sorted_amount
