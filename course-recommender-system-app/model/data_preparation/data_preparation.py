import pandas as pd
import neattext.functions as nfx


from pathlib import Path

def readData(files: str, extension='.csv', path='datasets'):
    """_summary_

    Args:
        file (str): Required file to read
        extension (str, optional): Extension of the required file. Defaults to '.csv'.

    Returns:
        A Pandas dataframe
    """
    if extension=='.csv':
        courses_dataset = pd.read_csv("%s/%s" %(path, files))
    elif extension=='.yaml':
        dpath = Path(path)

        courses_file = dpath / files
        with courses_file.open() as f:
            courses_dataset = pd.json_normalize(safe_load(f))

    return courses_dataset

# eu chamaria esse cara de "clean_title" :D
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

# Essa função podia estar no simple_recommendation_engine
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
