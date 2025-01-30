""" File contains all of the function performed given the troop report data"""
import pandas as pd
from src.utils.row_functions import create_display_name, determine_patrol_name,\
    determine_patrol_from_birthday, health_form_data, days_until_expiration
from src.utils.file_functions import read_in_latest_file
from src.utils.dataframe_functions import create_dataframe_with_headers

from src.utils.google_functions import get_google_sheets_data

def find_parent_info(trailmen_df, adult_df):
    """
    Given the dataframe for the kids and adults, make an adults dataframe of only parent display name and parent phone number
    """
    adult_information = []

    for index, trailman_row in trailmen_df.iterrows():
        
        address = trailman_row['ADDRESS LINE 1']
        adult_found = False
        for index, adult_row  in adult_df.iterrows():
            if address == adult_row['ADDRESS LINE 1']:
                adult_display_name = create_display_name(adult_row)
                adult_information.append([adult_display_name, adult_row['MOBILE PHONE']])
                adult_found = True
                break

        # adds a place holder in case no parent is identified
        if adult_found == False:
            adult_information.append(['Unknown Parent', 'n/a'])
    
    parent_df = pd.DataFrame(adult_information, columns=['PARENT NAME', 'PARENT PHONE NUMBER'])

    return parent_df

def make_youth_report(troop_report):
    """
    Takes in the report as a dataframe and writes summary out to a different sheet
    """
    # filter the datafram to only youth ('YOUTH' column name = 'Y')
    trailmen_df = troop_report[troop_report['YOUTH'] == 'Y']
    trailmen_df = trailmen_df.reset_index()
    adult_df = troop_report[troop_report['YOUTH'] == 'N']
    adult_df = adult_df.reset_index()

    # sets up information
    trailmen_report_df = pd.DataFrame()
    trailmen_report_df['DISPLAY NAME'] = trailmen_df.apply(create_display_name, axis=1)
    trailmen_report_df['PATROL'] = trailmen_df.apply(determine_patrol_name, axis=1)

    # adds parent information
    parent_info_df = find_parent_info(trailmen_df, adult_df)
    trailmen_report_df = pd.concat([trailmen_report_df, parent_info_df], axis=1, ignore_index=True)
    trailmen_report_df['MEMBER_NUMBER'] = trailmen_df['MEMBER NUMBER']
    trailmen_report_df['HEALTH_FORM'] = trailmen_df.apply(health_form_data, axis=1)
    trailmen_report_df['MEMBERSHIP EXPIRATION'] = trailmen_df['MEMBERSHIP EXP.']
    trailmen_report_df['SUGGESTED PATROL'] = trailmen_df.apply(determine_patrol_from_birthday, axis=1)
    trailmen_report_df.columns = ['NAME','PATROL','PARENT NAME',
                                  'PARENT PHONE NUMBER','MEMBER_NUMBER','HEALTH_FORM','MEMBERSHIP EXPIRATION','SUGGESTED PATROL']

    return trailmen_report_df

def create_expiring_trailmen_report(troop_report):
    """
    Gives a report of people who's memberships have expired or are about to be expired - returns a dataframe to be written to excel file
    """
    trailmen_df = troop_report[troop_report['YOUTH'] == 'Y']
    expiring_trailmen_df = pd.DataFrame()
    expiring_trailmen_df['DISPLAY NAME'] = trailmen_df.apply(create_display_name, axis=1)
    expiring_trailmen_df['PATROL'] = trailmen_df.apply(determine_patrol_name, axis=1)
    expiring_trailmen_df['MEMBERSHIP EXPIRATION'] = trailmen_df['MEMBERSHIP EXPIRATION']
    expiring_trailmen_df['DAYS UNTIL EXPIRATION'] = trailmen_df.apply(days_until_expiration, axis=1)

    return expiring_trailmen_df

def print_troop_dues_data(troop_dues_data):
    """
    Prints data for testing purposes
    """
    print(" - - - - - - TROOP DUES DATA - - - - - - ")
    print(troop_dues_data.head())
    print(f"Number of Trailmen: {len(troop_dues_data)}")
    print(f"Number of Trailmen with Dues: {len(troop_dues_data[troop_dues_data['DUES PAID'] == 'Y'])}")
    print(f"Number of Trailmen without Dues: {len(troop_dues_data[troop_dues_data['DUES PAID'] == 'N'])}")
    print(f"Troop Dues Column Names = {troop_dues_data.columns}")
    for row in troop_dues_data.iterrows():
        if row[1]['DUES PAID'] != 'N' and row[1]['DUES PAID'] != 'Y':
            print(row[1]['TRAILMAN'])
    print(" - - - - - - END OF TROOP DUES DATA - - - - - - ")
    print()
    return None

def print_youth_report_data(youth_report):
    """
    Prints testing data on the troop report
    """
    print(" - - - - - - TROOP REPORT DATA - - - - - - ")
    print(youth_report.head())
    print(f"Number of Trailmen: {len(youth_report)}")
    print(f"Youth Report Column Names = {youth_report.columns}")
    print(f"Number of Trailmen in Fox: {len(youth_report[youth_report['PATROL'] == 'Fox'])}")
    print(f"Number of Trailmen in Hawk: {len(youth_report[youth_report['PATROL'] == 'Hawk'])}")
    print(f"Number of Trailmen in Mountain Lion: {len(youth_report[youth_report['PATROL'] == 'Mountain Lion'])}")
    print(f"Number of Trailmen in Navigators: {len(youth_report[youth_report['PATROL'] == 'Navigator'])}")
    print(f"Number of Trailmen in Adventurers: {len(youth_report[youth_report['PATROL'] == 'Adventurer'])}")
    print(" - - - - - - END OF TROOP REPORT DATA - - - - - - ")
    print()

    return {
        "Trailmen": len(youth_report),
        "Fox": len(youth_report[youth_report['PATROL'] == 'Fox']),
        "Hawk": len(youth_report[youth_report['PATROL'] == 'Hawk']),
        "Mountain Lion": len(youth_report[youth_report['PATROL'] == 'Mountain Lion']),
        "Navigators": len(youth_report[youth_report['PATROL'] == 'Navigator']),
        "Adventurers": len(youth_report[youth_report['PATROL'] == 'Adventurer'])
    }

def get_troop_meeting_data(troop_attendance_df):
    """
    Takes in the troop attendance data as a dataframe and returns a dataframe of the troop meeting data
    :param: troop attendance data (dataframe)
    """
    # filter the data to only include the troop meetings
    troop_meeting_df = troop_attendance_df[troop_attendance_df['EVENT TYPE'] == 'Troop Meeting']

    formatted_troop_meeting_df = pd.DataFrame()
    formatted_troop_meeting_df['NAME'] = troop_meeting_df['TRAILMAN NAME']
    formatted_troop_meeting_df['PATROL'] = troop_meeting_df['EVENT LEVEL']
    formatted_troop_meeting_df['DATE'] = pd.to_datetime(troop_meeting_df['ACTIVITY DATE'], format='%m/%d/%Y')
    formatted_troop_meeting_df = formatted_troop_meeting_df.reset_index(drop=True)

    return formatted_troop_meeting_df

def get_trailmen_counts():
    """
    Gets general counts for the trailmen in the troop
    """
    # read in latest file
    troop_report, file_name = read_in_latest_file()
    troop_report = create_dataframe_with_headers(troop_report)
    # youth_report = make_youth_report(troop_report)

    # youth_data = print_youth_report_data(youth_report)

    # return youth_data

def return_meeting_data(troop_meeting_df, trailmen_counts, date):
    """
    Returns a summary of the meeting data formatted to be entered into the Google Sheet
    :param: troop meeting dataframe
    :param: trailmen counts (dictionary of the counts in each patrol)
    :param: date (datetime object)

    :return: meeting data (list of data)
    """
    meeting_data = troop_meeting_df[troop_meeting_df['DATE'] == date]
    
    fox_count = 0
    hawk_count = 0
    mountain_lion_count = 0
    navigator_count = 0
    adventurer_count = 0

    for index, row in meeting_data.iterrows():
        if row['PATROL'] == 'Fox':
            fox_count += 1
        elif row['PATROL'] == 'Hawk':
            hawk_count += 1
        elif row['PATROL'] == 'Mountain Lion':
            mountain_lion_count += 1
        elif row['PATROL'] == 'Navigator':
            navigator_count += 1
        elif row['PATROL'] == 'Adventurer':
            adventurer_count += 1
    
    troop_percent = len(meeting_data) / trailmen_counts['Trailmen']
    fox_percent = fox_count / trailmen_counts['Fox']
    hawk_percent = hawk_count / trailmen_counts['Hawk']
    mountain_lion_percent = mountain_lion_count / trailmen_counts['Mountain Lion']
    navigator_percent = navigator_count / trailmen_counts['Navigators']
    adventurer_percent = adventurer_count / trailmen_counts['Adventurers']

    return [date, len(meeting_data), troop_percent, fox_count, fox_percent, hawk_count, hawk_percent, mountain_lion_count, mountain_lion_percent, navigator_count, navigator_percent, adventurer_count, adventurer_percent]


