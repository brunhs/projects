import pandas as pd
import neattext.functions as nfx

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

def titleManipulation(dataframe, column:str, new_column:str):
    """_summary_

    Args:
        dataframe (Pandas): Pandas dataframe
        column (str): Column to be modified

    Returns:
        Dataframe: Column modified dataframe
    """
    dataframe[new_column] = dataframe[column].apply(nfx.remove_stopwords)\
    .apply(nfx.remove_special_characters)\
    .apply(nfx.remove_puncts)\
    .apply(nfx.remove_emojis)\
    .apply(str.lower)

    return dataframe

def searchTerm(term:str, dataframe, amount:int, course:str):
    """_summary_

    Args:
        term (str): Term to be searhhed
        dataframe (_type_): Pandas dataframe
        amount (int): Amount of terms to return

    Returns:
        Dataframe: Sorted amount of terms
    """
    result_dataframe = dataframe[dataframe[course].str.contains(term)]
    sorted_amount = result_dataframe.sort_values(by='num_subscribers', ascending=False).head(amount)
    return sorted_amount
