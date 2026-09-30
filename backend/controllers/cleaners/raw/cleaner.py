import json

with open ("trafficData.json", "r") as file:
    traffic = json.load(file)

data = {}

for each in traffic["records"]:
    location = each["location"]
    if (location not in data):
        cars = 0
        for key in each.keys():
            if("cars" in key):
                cars += each[key]
    data[each["location"]] = cars

print(data)