import pytz
import csv
import os
import datetime
from datetime import timedelta

import SamsaraAPI


def convertTimeZone(tz):
    if tz == 'PDT' or tz == 'PST' or tz == 'Pacific Daylight Time' or tz == 'Pacific Standard Time':
        return 'US/Pacific'
    elif tz == 'EDT' or tz == 'EST' or tz == 'Eastern Daylight Time' or tz == 'Eastern Standard Time':
        return 'US/Eastern'
    elif tz == 'CDT' or tz == 'CST' or tz == 'Central Daylight Time' or tz == 'Central Standard Time':
        return 'US/Central'
    elif tz == 'MDT' or tz == 'MST' or tz == 'Mountain Daylight Time' or tz == 'Mountain Standard Time':
        return 'US/Mountain'
    elif tz == 'AKDT' or tz == 'AKST' or tz == 'Alaska Daylight Time' or tz == 'Alaska Standard Time':
        return 'US/Alaska'
    elif tz == 'HADT' or tz == 'HST' or tz == 'Hawaii Daylight Time' or tz == 'Hawaii Standard Time':
        return 'US/Hawaii'
    else:
        return 'UTC'


# create array or array. array = [[Name,Start Time,Start Location,End Time,End Location,Delta], [Name,Start Time,Start Location,End Time,End Location,Delta]]. Use append to add more.
def write_CSV(dataArray, filename, columnHeaders ,folderName):
    # Define the folder name
    folder_name = folderName

    # Create the "Reports" folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    # Construct the full path for the CSV file
    file_path = os.path.join(folder_name, filename + '.csv')

    with open(file_path, 'w', newline='', encoding="utf-8") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(columnHeaders)
        for row in dataArray:
            filewriter.writerow(row)



def convert_to_rfc(date_obj):
    # date_obj = datetime.datetime.strptime(date_str, '%m/%d/%Y')
    local_tz = pytz.timezone(convertTimeZone(str(datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo)))
    local_date_obj = local_tz.localize(date_obj, is_dst=None)
    rfc_date_str = local_date_obj.isoformat()

    return rfc_date_str


def convert_date(date_str, str_format='%b %d, %Y %I:%M:%S %p %Z'):
    date_time = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
    utc_time = pytz.utc.localize(date_time)
    local_timezone = pytz.timezone(convertTimeZone(
        str(datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo)))  # Replace with your local timezone
    local_time = utc_time.astimezone(local_timezone)
    formatted_date_str = datetime.datetime.strftime(local_time, str_format)
    return formatted_date_str


def getUserDates():
    while True:
        startDateString = input("Enter a start date (in the format '05/08/2023'): ").strip()
        endDateString = input("Enter an end date (in the format '05/09/2023'): ").strip()

        # Ensure the date format is 'mm/dd/yyyy'
        if len(startDateString) < 10 or len(endDateString) < 10:
            print("Invalid date format. Please enter dates in the format 'mm/dd/yyyy'")
            continue

        # Convert input strings to datetime objects
        start_date = datetime.datetime.strptime(startDateString, "%m/%d/%Y")
        end_date = datetime.datetime.strptime(endDateString, "%m/%d/%Y")

        # Ensure the start date is earlier than the end date
        if start_date > end_date:
            print("Start date should be earlier than the end date. Please try again.")
            continue

        # Calculate the delta between start and end dates
        date_delta = end_date - start_date

        # Check if the delta is within the allowed range
        if date_delta == timedelta(days=0):
            end_date = end_date + timedelta(days=1)
            rfcEndDate = convert_to_rfc(end_date)
            return [convert_to_rfc(start_date), rfcEndDate]
        elif date_delta <= timedelta(days=31):
            return [convert_to_rfc(start_date), convert_to_rfc(end_date)]
        else:
            print("The date range should not exceeds 31 days. Please enter valid dates.")


def getAPIKey():
    while True:
        APIKEY = input("Enter a Samsara API key (e.g., samsara_api_0123456789): ").strip()

        # Perform input validation
        if is_valid_api_key(APIKEY):
            return APIKEY
        else:
            print("Invalid API key format. Please enter a valid API key.")


def is_valid_api_key(api_key):
    # Perform API key format validation (you can customize this based on Samsara's API key format)
    return api_key.startswith("samsara_api_") and len(api_key) == 42


def get_tag_id(api_key):
    tag_filter = input("Filter by Tag? (yes/no): ").strip().lower()

    if tag_filter == 'yes' or tag_filter == 'y':
        tag_array_api = SamsaraAPI.getTags(api_key)
        tag_array = {}
        displayTags = input("Display all tag ids? (yes/no): ").strip().lower()
        if displayTags == 'yes' or tag_filter == 'y':
            print('')
            for tag in tag_array_api:
                tag_array[tag['id']] = tag
                print(f"{tag['name']}: {tag['id']}")
            print('')
        while True:
            tag_selected = input("Enter Tag ID (e.g., 12345): ").strip()
            if tag_selected.isdigit() and tag_selected in tag_array:
                return tag_array[tag_selected]
            else:
                print("Invalid input. Tag ID should be a number. Please try again.")

    return {'name': "", 'id': ""}  # Return None if no tag filter is applied
