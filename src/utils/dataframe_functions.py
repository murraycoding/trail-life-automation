""" Logic to handle transforming and/or cleaning dataframes using pandas. """
### IMPORTS ###
import pandas as pd

def create_dataframe_with_headers(dataframe):
    """
    Takes in a dataframe and returns a dataframe with the first row as the column headers
    """
    first_row = dataframe.iloc[0]
    column_headers = [header.upper() for header in first_row.tolist()]
    dataframe.columns = column_headers
    dataframe = dataframe.drop([0])

    return dataframe
