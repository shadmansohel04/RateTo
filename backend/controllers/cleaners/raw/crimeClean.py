import json

# for fire

fireData = []

with open("neighbourhood-crime-rates.geojson", "r") as fire:
    data = json.load(fire)
    for each in data['features']:
        flipped = [[coord[1], coord[0]] for coord in each["geometry"]["coordinates"][0][0]]
        crimes = {
            "ASSAULT_RATE": 0,
            "AUTOTHEFT_RATE": 0,
            "BIKETHEFT_RATE": 0,
            "BREAKENTER_RATE": 0,
            "HOMICIDE_RATE": 0,
            "ROBBERY_RATE": 0,
            "SHOOTING_RATE": 0,
            "THEFTOVER_RATE": 0
        }
        for key in crimes.keys():
            for singleCrime in each["properties"].keys():
                if key in singleCrime:
                    crimes[key] += float(each["properties"][singleCrime])

        fireData.append({
           "areaName": each["properties"]["AREA_NAME"],
           "id": each["properties"]["_id"],
           "population": each["properties"]['POPULATION_2023'],
        #    "autoTheftRate2023": each["properties"]["AUTOTHEFT_RATE_2023"],
        #    "bikeTheftRate2023": each["properties"]["BIKETHEFT_RATE_2023"],
        #    "bneRate2023": each["properties"]["BREAKENTER_RATE_2023"],
        #    "homicideRate2023": each["properties"]["HOMICIDE_RATE_2023"],
        #    "robberyRate2023": each["properties"]["ROBBERY_RATE_2023"],
        #    "shootingRate2023": each["properties"]["SHOOTING_RATE_2023"],
        #    "carTheftRate2023": each["properties"]["THEFTOVER_RATE_2023"],
            "crimes": crimes,
            "poly": flipped
        })

alldata = {
    "crimeData": fireData
}

with open('crimeData.json', 'w') as fire:
    json.dump(fireData, fire, indent=2)
