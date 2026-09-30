import json

# for fire

police = []

with open("./data/policeLocations.json", "r") as fire:
    data = json.load(fire)
    for each in data['features']:
        police.append({
            "address": each['properties']['ADDRESS'],
            "facility": each['properties']['FACILITY'],
            "id": each['properties']['_id'],
            "location": each['geometry']['coordinates'][0]
        })

with open('./data/police_locations.json', 'w') as fire:
    json.dump(police, fire, indent=4)
