""" Main Application file for the Trail Life Automation process """
### IMPORTS ###
import sys
import os
import pandas as pd
import json

from src.utils.file_functions import read_in_latest_file
from src.utils.dataframe_functions import create_dataframe_with_headers, update_troop_dues_names
from src.utils.troop_functions import make_youth_report, print_troop_dues_data, print_youth_report_data
from src.utils.google_functions import update_google_sheet, get_google_sheets_data, clear_range
from src.utils.row_functions import days_until_expiration, finalize_troop_dues


def main(env):
    """ Main function for the Trail Life Automation process """
    
    # read in latest file
    troop_report, file_name = read_in_latest_file()
    
    # adjusts the dataframe to have proper headers
    troop_report = create_dataframe_with_headers(troop_report)
    
    youth_report = make_youth_report(troop_report)
    print_youth_report_data(youth_report)
 
    ### GOOGLE SHEETS UPDATES ###
    # gets the id of the google sheets (prod vs dev)
    with open("google_sheets_id_data.json") as file:
        google_id_data = json.load(file)
    
    attendance_sheets_id = google_id_data[env]["attendance_sheets_id"]
    attendance_sheet_range = "Input Data!A:G"
    roster_sheets_id = google_id_data[env]["roster_sheets_id"]
    roster_sheet_range = "Input Data!A:H"
    dues_sheets_id = google_id_data[env]["dues_sheets_id"]
    dues_sheet_range = "Dues by trailman!A:D"


    # updates troop rosters (google sheets)
    print("# # # # # # TROOP ROSTER # # # # # #")
    update_google_sheet(roster_sheets_id, roster_sheet_range, youth_report.values.tolist())
    print("# # # # # # END OF TROOP ROSTER # # # # # #")
    
    print("\n")
    
    print("# # # # # # TROOP DUES # # # # # #")
    troop_dues_data = get_google_sheets_data(dues_sheets_id, dues_sheet_range)
    troop_dues_df = pd.DataFrame(troop_dues_data[1:], columns=[item.upper() for item in troop_dues_data[0]])
    # clean dues information
    troop_dues_df['DUES PAID'] = troop_dues_df['DUES PAID'].apply(lambda x: x.strip().upper())
    final_troop_df = pd.merge(youth_report, troop_dues_df, on='MEMBER_NUMBER', how='left')
    print("# # # # # # END OF TROOP DUES # # # # # #")

    print("\n")

    print("# # # # # # ATTENDANCE INFORMATION # # # # # #")
    attendance_df = pd.DataFrame()
    attendance_df['NAME'] = final_troop_df['NAME']
    attendance_df['PATROL'] = final_troop_df['PATROL']
    attendance_df['MEMBERSHIP_STATUS'] = final_troop_df.apply(days_until_expiration, axis=1)
    attendance_df['HEALTH FORM'] = final_troop_df['HEALTH_FORM'].apply(lambda x: x.strip().upper())
    attendance_df['TROOP DUES'] = final_troop_df.apply(finalize_troop_dues, axis=1)

    # Check for NaN values in attendance_df
    if attendance_df['TROOP DUES'].isnull().values.any():
        attendance_df = attendance_df.fillna('Missing Data')

    update_google_sheet(attendance_sheets_id, attendance_sheet_range, attendance_df.values.tolist())
    print("# # # # # # END OF ATTENDANCE INFORMATION # # # # # #")

    return None

if __name__ == "__main__":
    main("DEV")


