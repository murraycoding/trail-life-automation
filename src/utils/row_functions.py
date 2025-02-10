""" File to contain all of the functions on rows for any trail life coding work"""

### IMPORTS ###
import pandas as pd
from datetime import datetime, date

from src.utils.date_functions import format_date

# passing unit tests
def determine_patrol_name(row):
    """
    Returns just the patrol name 
    """
    try:
        split_values = row['PATROL'].split(' - ')
    except AttributeError:
        return "None"
    
    return split_values[0]

# passing unit tests
def determine_patrol_from_birthday(row):
    """
    Determines what patrol the trailman should be in based on birthday
    """
    now = datetime.now()
    if now.month < 8:
        reference_year = now.year-1
    else:
        reference_year = now.year
    
    fox_year1_date = format_date(10,1,reference_year-5)
    fox_year2_date = format_date(10,1,reference_year-6)
    hawk_year1_date = format_date(10,1,reference_year-7)
    hawk_year2_date = format_date(10,1,reference_year-8)
    mountainlion_year1_date = format_date(10,1,reference_year-9)
    mountainlion_year2_date = format_date(10,1,reference_year-10)
    navigator_date = format_date(10,1,reference_year-11)
    adventurer_date = format_date(10,1,reference_year-14)

    if pd.notna(row['BIRTHDATE']):
        birthday_list = row['BIRTHDATE'].split("/")
        birthday_obj = format_date(birthday_list[0],birthday_list[1],birthday_list[2])
    
    if birthday_obj < adventurer_date:
        return "Adventurer"
    elif birthday_obj < navigator_date:
        return "Navigator"
    elif birthday_obj < mountainlion_year2_date:
        return "Mountain Lion - Year 2"
    elif birthday_obj < mountainlion_year1_date:
        return "Mountain Lion - Year 1"
    elif birthday_obj < hawk_year2_date:
        return "Hawk - Year 2"
    elif birthday_obj < hawk_year1_date:
        return "Hawk - Year 1"
    elif birthday_obj < fox_year2_date:
        return "Fox - Year 2"
    elif birthday_obj < fox_year1_date:
        return "Fox - Year 1"
    else:
        return "Child not old enough"

# passing unit tests
def create_display_name(row):
    """
    Takes in the row for each trailman and creates a display name for them
    """
    if pd.notna(row['NICKNAME']) and row['NICKNAME'] != '':
        nickname = row['NICKNAME'].split(" ")[0]
        return f"{nickname} {row['LAST NAME']}"
    else:
        return f"{row['FIRST NAME']} {row['LAST NAME']}"

# passing unit tests
def days_until_expiration(row):
    """
    Returns the days until a trailman's membership expires
    """
    date_str = row['MEMBERSHIP EXPIRATION']
    if "/" not in date_str:
        return "No date found"
    
    date_list = date_str.split("/")

    month = date_list[0]
    day = date_list[1]
    year = date_list[2]

    date_obj = format_date(month, day, year)
    now = datetime.now()
    now_obj = date(now.year, now.month, now.day)

    if now_obj >= date_obj:
        return "Membership Expired"
    else:
        days_until_expiration = int(str(date_obj - now_obj).split(" ")[0])
        if days_until_expiration < 30:
            return f"Expires in {days_until_expiration} days"
        else:
            return "Current"

# passing unit tests
def health_form_data(row):
    """
    Creates a report of who has turned in their health forms
    """
    if pd.notna(row['HEALTH FORM']):
        return "Complete"
    else:
        return "MISSING"

# not tested
def finalize_troop_dues(row):
    """
    Returns the final troop informtion for dues and fills in N for missing values
    """
    # cleans value
    if pd.isna(row['DUES PAID']):
        return 'Missing Data'
    elif row['DUES PAID'].strip().upper() == 'Y':
        return 'Paid'
    elif row['DUES PAID'].strip().upper() == 'N':
        return 'Not Paid'
    else:
        return 'Missing Data'