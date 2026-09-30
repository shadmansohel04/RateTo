import requests
import json

def addressToCoord(address):
    try:
        response = requests.get("https://geocode.maps.co/search", params={
            "q": address,
            "api_key": "6684a1ab4fb51292837730miv1cefd7"
        })
        
        data = response.json()

        location = data[0]
        lat = location["lat"]
        lon = location["lon"]
        return (float(lat), float(lon)) 
    except Exception as e:
        print(f"{str(e)}")


with open("hospitalData.json", "r") as file:
    hospitals = json.load(file)

hos = []

for i in range(4):
    for each in hospitals:
        if(each["coordinates"] != None):
            coordinates = addressToCoord(each["address"])
            hos.append({**each, "coordinates": coordinates})

with open("hospitalData.json", "w") as file:
    json.dump(hos, file, indent = 2)