"""
File to be run to generate the attendance report
"""
import json

def attendance_report(env):
    # data setup
    with open("google_sheets_id_data.json") as file:
        google_id_data = json.load(file)
    
    attendance_sheets_id = google_id_data[env]["attendance_report_sheets_id"]

    # open the latest attendance report
    

    # covert data in the spreadsheet into a dataframe

    # complete the following tasks as a part of the report
    # 1. Get a list of the last date each trailman attended a meeting
    # 2. Get a list of the number of meetings each trailman has attended separated by the current year and last
    pass

if __name__ == "__main__":
    attendance_report("DEV")