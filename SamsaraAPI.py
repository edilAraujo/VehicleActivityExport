import requests


def getSafetyEvents(api_token, startTime, endTime):
    url = f"https://api.samsara.com/fleet/safety-events?startTime={startTime}&endTime={endTime}"

    headers = {"Authorization": "Bearer " + api_token}
    response = requests.get(url, headers=headers)

    safetyEvents = response.json()["data"]
    hasnext = response.json()["pagination"]["hasNextPage"]

    while hasnext:
        pagination_url = url + "&after=" + response.json()["pagination"]["endCursor"]
        response = requests.get(pagination_url, headers=headers)
        safetyEvents += response.json()["data"]
        hasnext = response.json()["pagination"]["hasNextPage"]

    return safetyEvents


def getTags(api_token):
    url = "https://api.samsara.com/tags"

    headers = {"Authorization": "Bearer " + api_token}
    response = requests.get(url, headers=headers)

    tags = response.json()["data"]
    hasnext = response.json()["pagination"]["hasNextPage"]

    while hasnext:
        pagination_url = url + "&after=" + response.json()["pagination"]["endCursor"]
        response = requests.get(pagination_url, headers=headers)
        tags += response.json()["data"]
        hasnext = response.json()["pagination"]["hasNextPage"]

    return tags


def getVehicleLocations(api_token, startTime, endTime):
    url = f"https://api.samsara.com/fleet/vehicles/locations/history?startTime={startTime}&endTime={endTime}"

    headers = {"Authorization": "Bearer " + api_token}
    response = requests.get(url, headers=headers)

    locations = response.json()["data"]
    hasnext = response.json()["pagination"]["hasNextPage"]

    while hasnext:
        pagination_url = url + "&after=" + response.json()["pagination"]["endCursor"]
        response = requests.get(pagination_url, headers=headers)
        locations += response.json()["data"]
        hasnext = response.json()["pagination"]["hasNextPage"]

    return locations


def getVehicleHistoricStats(access_token, startTime, endTime, vehicleId="", statTypes=""):
    url = 'https://api.samsara.com/fleet/vehicles/stats/history?startTime=' + startTime + "&endTime=" + endTime + '&vehicleIds=' + vehicleId + '&types=' + statTypes
    payload = {}
    headers = {'Authorization': 'Bearer ' + access_token}
    response = requests.request("GET", url, headers=headers, data=payload)
    vehicleStats = response.json()['data']
    hasnext = response.json()['pagination']['hasNextPage']
    while hasnext:
        pagination_url = url + "&after=" + response.json()['pagination']['endCursor']
        response = requests.request("GET", pagination_url, headers=headers, data=payload)
        vehicleStats = vehicleStats + response.json()['data']
        hasnext = response.json()['pagination']['hasNextPage']
    return vehicleStats


def getVehicles(api_token, tag_ids=''):
    url = f"https://api.samsara.com/fleet/vehicles?limit=512&tagIds={tag_ids}"

    headers = {"Authorization": "Bearer " + api_token}
    response = requests.get(url, headers=headers)

    vehicles = response.json()["data"]
    hasnext = response.json()["pagination"]["hasNextPage"]

    while hasnext:
        pagination_url = url + "&after=" + response.json()["pagination"]["endCursor"]
        response = requests.get(pagination_url, headers=headers)
        vehicles += response.json()["data"]
        hasnext = response.json()["pagination"]["hasNextPage"]

    return vehicles
