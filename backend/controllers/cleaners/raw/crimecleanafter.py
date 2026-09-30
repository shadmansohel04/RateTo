import json

# for fire
fireData = []

with open("crimeData.json", "r") as fire:
    data = json.load(fire)
    maxData = {
        "ASSAULT_RATE": 0,
        "AUTOTHEFT_RATE": 0,
        "BIKETHEFT_RATE": 0,
        "BREAKENTER_RATE": 0,
        "HOMICIDE_RATE": 0,
        "ROBBERY_RATE": 0,
        "SHOOTING_RATE": 0,
        "THEFTOVER_RATE": 0
    }

    for each in data:
        for single in each["crimes"].keys():
            if (each["crimes"][single] > maxData[single]):
                maxData[single] = each["crimes"][single]

with open("crimeData1.json", "w") as crime:
    newData = {
        "crimeData": data,
        "maxData": maxData
    }
    json.dump(newData, crime, indent=2)