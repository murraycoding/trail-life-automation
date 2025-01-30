### IMPORTS ###
import os
from datetime import date
import pandas as pd

from src.utils.date_functions import format_date

# unit tested
def read_in_latest_file():
    """
    Reads in the latest troop report. Trail life report is a pandas dataframe and latest_file is a string.
    :param: None
    :return: trail_life_report, latest_file
    """

    current_directory = os.path.dirname(os.path.abspath(__file__))
    reports_directory = os.path.join(current_directory, 'reports')

    # put in the date of the start of the school year
    latest_date = date(2020,8,1)
    latest_file = None

    # lists files in the directory
    for file_name in os.listdir(reports_directory):
        file_date = pull_date_from_filename(file_name)
        if file_date > latest_date:
            latest_file = file_name
            latest_date = file_date
    
    trail_life_report = pd.read_excel(os.path.join(reports_directory,latest_file), engine='openpyxl')

    return trail_life_report, str(latest_file)

def pull_date_from_filename(file_name):
    """
    Pulls the date from the end of the filename
    """
    # TODO Change this to a regex pattern (2 digits)-(2 digits)-(4 digits)

    # print(f"File name = {file_name}")
    try:
        date_string = file_name[-15:-5]
        date_list = date_string.split("-")
        day = date_list[0]
        month = date_list[1]
        year = date_list[2]
    except IndexError:
        print(f"Index error occured...moving to next file")
        return format_date(1,1,2001)

    return format_date(month, day, year)

def read_in_latest_attendance_file():
    """
    Reads in the latest attendance report.
    :param: None
    return: attendance_report, latest_file
    """
    current_directory = os.path.dirname(os.path.abspath(__file__))
    reports_directory = os.path.join(current_directory, 'attendance_reports')

    latest_file = None
    largest_file_number = 0

    for file_name in os.listdir(reports_directory):
        file_number = int(file_name.split("-")[2].split(".")[0])
        if file_number > largest_file_number:
            largest_file_number = file_number
            latest_file = file_name
    
    attendance_report = pd.read_excel(os.path.join(reports_directory,latest_file), engine='openpyxl')

    return attendance_report, str(latest_file)