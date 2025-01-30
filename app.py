""" Main Application file for the Trail Life Automation process """
### IMPORTS ###
import sys
import os
import pandas as pd
from src.utils.file_functions import read_in_latest_file
from src.utils.dataframe_functions import create_dataframe_with_headers
from src.utils.troop_functions import make_youth_report, print_troop_dues_data, print_youth_report_data
from src.utils.google_functions import update_google_sheet, get_google_sheets_data
from src.utils.row_functions import days_until_expiration, finalize_troop_dues


def main():
    """ Main function for the Trail Life Automation process """
    
    # read in latest file
    troop_report, file_name = read_in_latest_file()
    
    # adjusts the dataframe to have proper headers
    troop_report = create_dataframe_with_headers(troop_report)
    
    youth_report = make_youth_report(troop_report)
    print_youth_report_data(youth_report)
 
    ### GOOGLE SHEETS UPDATES ###
    # updates troop rosters (google sheets)
    troop_roster_sheet_id = "1Ga4N7JoCFzdQPiks6xqPdu3jrMYmpjgToOLwGesL6uE" # check this
    troop_roster_range = "Input Data!A:H" # check this
    print("Updating Troop Roster")
    update_google_sheet(troop_roster_sheet_id, troop_roster_range, youth_report.values.tolist())

    # get troop dues info (google sheets)
    troop_dues_sheet_id = "1BGJGcjv5_nICYkfDltZgWyEPm--zX5UBjOx6JSdzftw"
    troop_dues_range = "Dues by trailman!A:D"
    troop_dues_data = get_google_sheets_data(troop_dues_sheet_id, troop_dues_range)
    troop_dues_df = pd.DataFrame(troop_dues_data[1:], columns=[item.upper() for item in troop_dues_data[0]])
    # clean dues information
    troop_dues_df['DUES PAID'] = troop_dues_df['DUES PAID'].apply(lambda x: x.strip().upper())
    print_troop_dues_data(troop_dues_df)

    # join troop dues data with youth report
    final_troop_df = pd.merge(youth_report, troop_dues_df, on='MEMBER_NUMBER', how='left')
    
    # update attendance data
    attendance_df = pd.DataFrame()
    attendance_df['NAME'] = final_troop_df['NAME']
    attendance_df['PATROL'] = final_troop_df['PATROL']
    attendance_df['MEMBERSHIP_STATUS'] = final_troop_df.apply(days_until_expiration, axis=1)
    attendance_df['HEALTH FORM'] = final_troop_df['HEALTH_FORM'].apply(lambda x: x.strip().upper())
    attendance_df['TROOP DUES'] = final_troop_df.apply(finalize_troop_dues, axis=1)

    # Check for NaN values in attendance_df
    if attendance_df['TROOP DUES'].isnull().values.any():
        attendance_df = attendance_df.fillna('Missing Data')

    update_google_sheet("1Mm2kYC8j6YLc6nISQFdvgIxXDiZjYaphxZQd9M6DWic", "Input Data!A:G", attendance_df.values.tolist())

    return None

if __name__ == "__main__":
    main()
