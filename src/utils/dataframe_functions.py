""" Logic to handle transforming and/or cleaning dataframes using pandas. """
### IMPORTS ###
import pandas as pd
from src.utils.google_functions import update_google_sheet, clear_range

pd.options.mode.copy_on_write = True

def create_dataframe_with_headers(dataframe):
    """
    Takes in a dataframe and returns a dataframe with the first row as the column headers
    """
    first_row = dataframe.iloc[0]
    column_headers = [header.upper() for header in first_row.tolist()]
    dataframe.columns = column_headers
    dataframe = dataframe.drop([0])

    return dataframe

def update_troop_dues_names(tlc_trailmen, troop_dues_df, dues_sheet_range, dues_sheets_id):
    """
    Updates the troop dues names in the Google Sheets with the latest information from the TLC trailmen dataframe.
    Args:
        tlc_trailmen (pd.DataFrame): DataFrame containing the trailmen information with columns ['NAME', 'MEMBER_NUMBER', 'PATROL'].
        troop_dues_df (pd.DataFrame): DataFrame containing the current troop dues information.
        dues_sheet_range (str): The range in the Google Sheet to update.
        dues_sheets_id (str): The ID of the Google Sheet to update.
    Returns:
        None
    """
    
    # Get the tlc_trailmen dataframe with only relevant information
    tlc_trailmen = tlc_trailmen[['NAME', 'MEMBER_NUMBER', 'PATROL']]
    tlc_trailmen.columns = ['TRAILMAN', 'MEMBER_NUMBER', 'TROOP PATROL']

    # Filter the troop_dues_df to only include the tlc_trailmen
    troop_dues_df = troop_dues_df[troop_dues_df['MEMBER_NUMBER'].isin(tlc_trailmen['MEMBER_NUMBER'])]

    # new trailmen information
    to_be_added_df = tlc_trailmen[~tlc_trailmen['MEMBER_NUMBER'].isin(troop_dues_df['MEMBER_NUMBER'])]
    if len(to_be_added_df) > 0:
        to_be_added_df.loc[:, 'DUES PAID'] = 'N'


    # adds new trailmen to dataframe and preps data for Google Sheets update
    titles = ['TRAILMAN', 'MEMBER_NUMBER', 'TROOP PATROL', 'DUES PAID']
    title_row_data = pd.DataFrame([titles], columns=troop_dues_df.columns)
    updated_dues_data = pd.concat([title_row_data,troop_dues_df, to_be_added_df], ignore_index=True)

    # Update the google sheet with the new troop_dues_df
    clear_range(dues_sheets_id, dues_sheet_range)
    update_google_sheet(dues_sheets_id, dues_sheet_range, updated_dues_data.values.tolist())

    return updated_dues_data





    
