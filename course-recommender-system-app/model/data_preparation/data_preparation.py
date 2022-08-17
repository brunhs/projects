import pandas as pd
import neattext.functions as nfx


from pathlib import Path

def readData(files: str, extension='.csv', path='datasets'):
    """
    Function responsible to read the data.

    Args:
        file (str): Required file to read.
        extension (str, optional): Extension of the required file. Defaults to '.csv'.

    Returns:
        A Pandas dataframe.
    """
    if extension=='.csv':
        courses_dataset = pd.read_csv("%s/%s" %(path, files))
    elif extension=='.yaml':
        dpath = Path(path)

        courses_file = dpath / files
        with courses_file.open() as f:
            courses_dataset = pd.json_normalize(safe_load(f))

    return courses_dataset

def cleanTitle(dataframe, column:str, new_column:str):
    """_summary_

    Args:
        dataframe (Pandas): Pandas dataframe.
        column (str): Column to be modified.

    Returns:
        Dataframe: Column modified dataframe.
    """
    dataframe[new_column] = dataframe[column].apply(nfx.remove_stopwords)\
    .apply(nfx.remove_special_characters)\
    .apply(nfx.remove_puncts)\
    .apply(nfx.remove_emojis)\
    .apply(str.lower)

    return dataframe