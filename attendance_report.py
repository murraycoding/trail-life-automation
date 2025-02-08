"""
File to be run to generate the attendance report
"""
import json
import pandas as pd
from datetime import datetime, timedelta

from src.utils.file_functions import read_in_attendance_file
from src.utils.dataframe_functions import find_trailman_latest_meeting
from src.utils.google_functions import update_google_sheet, clear_range

def attendance_report(env):
    # data setup
    with open("google_sheets_id_data.json") as file:
        google_id_data = json.load(file)
    
    attendance_sheets_id = google_id_data[env]["attendance_report_sheets_id"]

    attendance_df = read_in_attendance_file()
    print(attendance_df)
    troop_meeting_df = attendance_df[attendance_df['Event Type'] == "Troop Meeting"]
    two_years_ago = datetime.now() - timedelta(days=2*365)
    troop_meeting_df = troop_meeting_df[pd.to_datetime(troop_meeting_df['Activity Date']) >= two_years_ago]
    unique_trailmen_series = troop_meeting_df['Trailman Name'].drop_duplicates().reset_index(drop=True)
    attendance_report_df = pd.DataFrame(columns=['Trailman Name', 'Patrol', 'Latest Meeting'])

    for name in unique_trailmen_series:
        print(f"Name = {name}")
        trailman_df = troop_meeting_df[troop_meeting_df['Trailman Name'] == name]
        latest_meeting, patrol = find_trailman_latest_meeting(name, troop_meeting_df)
        
        print(f"Latest Meeting = {latest_meeting}")
        print(f"Patrol = {patrol}")
        print("\n")
        print(" - - - - - - ")
        
        if latest_meeting is not None:
            latest_meeting = latest_meeting.strftime("%m/%d/%Y")
        else:
            latest_meeting = "N/A"
        
        if patrol is None:
            patrol = "N/A"
        
        new_row = pd.DataFrame([{
            'Trailman Name': name,
            'Patrol': patrol,
            'Latest Meeting': latest_meeting
        }])
        attendance_report_df = pd.concat([attendance_report_df, new_row], ignore_index=True)
    
    # update the google sheet
    attendance_sheet_range = "Input Data!A:C"
    clear_range(attendance_sheets_id, attendance_sheet_range)
    update_google_sheet(attendance_sheets_id, attendance_sheet_range, attendance_report_df.values.tolist())

    


    # open the latest attendance report
    

    # covert data in the spreadsheet into a dataframe

    # complete the following tasks as a part of the report
    # 1. Get a list of the last date each trailman attended a meeting
    # 2. Get a list of the number of meetings each trailman has attended separated by the current year and last

if __name__ == "__main__":
    attendance_report("PROD")