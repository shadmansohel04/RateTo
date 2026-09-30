import json

with open("crimeData1.json", "r") as crime:
    data = json.load(crime)
    

for each in data["crimeData"]:
    score = 0
    for key in data["maxData"].keys():
        finalKey = key.lower()
        if("shooting" in finalKey or "homicide" in finalKey):
            weight = 10
        elif("assault" in finalKey):
            weight = 8
        elif("robbery" in finalKey):
            weight = 5
        elif("bne" in finalKey):
            weight = 4
        elif("autoTheft" in finalKey):
            weight = 3
        elif("cartheft" in finalKey):
            weight = 2
        elif("bike" in finalKey):
            weight = 1
        else:
            weight = 0

        score += each["crimes"][key]/data["maxData"][key]*weight
    each["crimeScore"] = score/30 * 100
    


with open("crimedata1.json", "w") as newfile:
    json.dump(data, newfile, indent=2)
            