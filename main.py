import os
import helper
import SamsaraAPI
import datetime
import logging
import pandas as pd


# Create a timestamp for the log file name
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Configure logging with the timestamp in the log file name
log_filename = f'VehicleActivity_{timestamp}.log'
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Takes gps locations and creates a CSV file with this data using Pandas
def saveActivityFilePandas(vehicle, x, total_vehicles, csv_headers, start_date, end_date, locations):
    vehicleName = vehicle['name']
    logging.info(f"Saving activity file for: {vehicleName}  ({x} out of {total_vehicles}) - Vehicles Index: {x-1}")
    print(f"Saving activity file for: {vehicleName} -- ({x} out of {total_vehicles})")

    data = []

    for location_data in locations[vehicle['id']]:
        # Assuming location_data is a dictionary with keys matching csv_headers
        data.append(location_data)

    if data:
        df = pd.DataFrame(data, columns=csv_headers)
        folder_name = "Samsara Reports"
        os.makedirs(folder_name, exist_ok=True)  # Create the "reports" folder if it doesn't exist
        file_name = os.path.join(folder_name, f"{vehicleName} - {start_date[:10]} to {end_date[:10]}.csv")
        df.to_csv(file_name, index=False, encoding='utf-8')
        logging.info(f"{vehicleName} file saved")
        return 1
    return 0


# Gets user input for API key, and stat/end dates.
# Gets list of vehicles and then proceeds to generate activity files for each vehicle.
def getVehicleActivity():
    # API_KEY = ''
    API_KEY = helper.getAPIKey()
    logging.info(f"API Key: {API_KEY}")

    start_date, end_date = helper.getUserDates()
    logging.info(f"Start Date: {start_date}")
    logging.info(f"End Date: {end_date}")

    tag_selected = helper.get_tag_id(API_KEY)
    logging.info(f"Tag selected: {tag_selected['name']}  -- id: {tag_selected['id']}")

    csv_headers = ['Vehicle Name', 'Time', 'Speed', 'Latitude', 'Longitude', 'Address', 'Odometer']

    logging.info(f"Getting vehicle list from Samsara API")
    print(f"Getting vehicle list from Samsara API")

    vehicles = SamsaraAPI.getVehicles(API_KEY, tag_selected['id'])
    total_vehicles = len(vehicles)
    filesSaved = 0

    logging.info(f"Total number of vehicles: {total_vehicles}")
    print(f"Total number of vehicles: {total_vehicles}")

    for x, vehicle in enumerate(vehicles, start=1):
    # for x, vehicle in enumerate(vehicles[180:], start=181):
    # if the process get's cut short with vehicle 180 being the last one in the log file,
    # this would have to start with the next vehicle. Log file number - 1 and log file number + 1
        # print (f"{x} - {vehicle['name']}")
        locations = getVehicleGPSLocations(API_KEY, start_date, end_date, vehicle['id'],
                                           'gps&decorations=obdOdometerMeters')

        if len(locations) == 0:
            print(f"No location data for {vehicle['name']} -- ({x} out of {total_vehicles})")
            logging.info(f"No location data for {vehicle['name']} -- ({x} out of {total_vehicles}) - Vehicles Index: {x-1}")
        else:
            filesSaved = filesSaved + saveActivityFilePandas(vehicle, x, total_vehicles, csv_headers, start_date, end_date, locations)
    logging.info(f"{filesSaved} files saved")


# Get vehicle GPS locations from the Vehicle Stats API.
# Using the stats API in order for the data to be pre-associated with the odometer values
def getVehicleGPSLocations(API_KEY, startTime, endTime, vehicleId="", statTypes=""):
    activityLogs = {}

    gpsLocations = SamsaraAPI.getVehicleHistoricStats(API_KEY, startTime, endTime, vehicleId, statTypes)

    for vehicle in gpsLocations:
        # print(f"Gathering Activity data for: {vehicle['name']}")
        for loc in vehicle['gps']:
            if ('decorations' in loc and 'obdOdometerMeters' in loc['decorations']):
                odometer = round((loc['decorations']['obdOdometerMeters']['value'] / 1609.34), 2)
            else:
                odometer = ''
            if ('reverseGeo' in loc and 'formattedLocation' in loc['reverseGeo']):
                reverseGeo = (loc['reverseGeo']['formattedLocation'])
            else:
                reverseGeo = ''

            if vehicle['id'] not in activityLogs:
                activityLogs[vehicle['id']] = []

            activityLogs[vehicle['id']].append([
                vehicle['name'],
                loc['time'],
                loc['speedMilesPerHour'],
                loc['latitude'],
                loc['longitude'],
                reverseGeo,
                odometer])

    return activityLogs

if __name__ == '__main__':
    getVehicleActivity()

