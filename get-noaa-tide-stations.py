import json
import requests

geoGroupsUrl = "https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/geogroups.json?type=ETIDES&lvl=4"
stationsUrl = "https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/geogroups/{}/children.json"
filename = "tide-stations.json"
tideStationsByGroup = []

print("Grabbing geo groups...")
result = requests.get(geoGroupsUrl).json()

geoGroupList = result["geoGroupList"]
for group in geoGroupList:
    print("Grabbing stations in group id {}...".format(group["geoGroupId"]))
    stationsInGroup = requests.get(stationsUrl.format(group["geoGroupId"])).json()
    stationsByGroup = {}
    stationsByGroup["geoGroupName"] = group["geoGroupName"]
    stationsByGroup["geoGroupId"] = group["geoGroupId"]
    stationList = stationsInGroup["stationList"]
    stations = []
    for station in stationList:
        if station["stationId"] is None:
            continue
        stationEntry = {}
        stationEntry["stationId"] = station["stationId"]
        stationEntry["lat"] = station["lat"]
        stationEntry["lon"] = station["lon"]
        stationEntry["name"] = station["geoGroupName"]
        stations.append(stationEntry)
    stationsByGroup["stations"] = stations
    tideStationsByGroup.append(stationsByGroup)

print("success, writing to {}".format(filename))
with open(filename, "w") as output:
    json.dump(tideStationsByGroup, output)