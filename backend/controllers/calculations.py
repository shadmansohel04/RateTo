import json
from haversine import haversine, Unit
import os
from controllers.cleaners.otherFunc import addressToCoord, calculate_area
from controllers.scoremaker import getParkScore, getSafetyScore, getTransportationScore
from shapely.geometry import Polygon, Point
import time
import random
import numpy as np
from math import radians, sin, cos, sqrt, atan2

print("cold start")
currentDir = os.path.dirname(__file__)
path = os.path.join(currentDir, "./cleaners/data/water.json")
with open(path, "r") as file:
    data = json.load(file)

coords_array = np.array(data["watercoords"], dtype=np.float64)

def haversine_np(coord, coords_array):
    R = 6371.0
    lat1, lon1 = map(radians, coord)
    lat2 = np.radians(coords_array[:, 0])
    lon2 = np.radians(coords_array[:, 1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    return R * c

def genCode():
    chars = '123456789ABCD'
    random_string = ''.join(random.choices(chars, k=10))
    return random_string

def getWater(coord):
    try:
        distances = haversine_np(coord, coords_array)
        
        min_distance = np.min(distances)
        if min_distance < 100:
            return min_distance
        else:
            return -1
    except Exception as e:
        print("Water failed: " + str(e))
        return -1

def getBike(coord):
    try:
        path = os.path.join(currentDir, "./cleaners/data/bike.json")
        with open (path, "r") as file:
            data = json.load(file)

        network = []
        for each in data:
            for placeholder in each["coord"]:
                converted = (float(placeholder[0]), float(placeholder[1]))
                tempDistance = haversine(coord,converted, unit=Unit.KILOMETERS)
            if tempDistance <= 5:
                each = {
                    **each,
                    "fromCoord": tempDistance
                }
                network.append(each)

        return network
    except Exception as e:
        print(f"{str(e)}")

def getTraffic(coord):
    try:
        path = os.path.join(currentDir, "./cleaners/data/trafficData.json")
        with open(path, "r") as file:
            data = json.load(file)

        coords_array = np.array([each["coord"] for each in data], dtype=np.float64)
        distances = haversine_np(coord, coords_array)

        close = []
        for i, distance in enumerate(distances):
            if distance < 5:
                close.append({
                    **data[i],
                    "distance": round(distance, 2)
                })

        return close
    except Exception as e:
        print("getTraffic failed:", str(e))

def getTTC(coord):
    try:
        path = os.path.join(currentDir, "./cleaners/data/ttcLocations1.json")
        with open(path, "r") as file:
            ttc = json.load(file)

        stations = ttc["stations"]
        coords_array = np.array([each["coord"] for each in stations])

        distances = haversine_np(coord, coords_array)

        within_2km_indices = np.where(distances <= 2)[0]
        close = [
            {
                "name": stations[i]["name"],
                "address": stations[i]["address"],
                "coord": stations[i]["coord"],
                "distance": round(distances[i], 2)
            }
            for i in within_2km_indices
        ]

        closest_index = np.argmin(distances)
        closest = {
            "name": stations[closest_index]["name"],
            "address": stations[closest_index]["address"],
            "coord": stations[closest_index]["coord"],
            "distance": round(distances[closest_index], 2)
        }

        return {
            "ttcStations": close,
            "closestTTCStation": closest
        }

    except Exception as e:
        print("ttc no work")
        print(f"except: {str(e)}")

def getHospitals(coord):
    try:
        path = os.path.join(currentDir, "./cleaners/data/hospitalData.json")
        with open(path) as file:
            hospitals = json.load(file)

        coords_array = np.array([each["coordinates"] for each in hospitals])
        distances = haversine_np(coord, coords_array)

        within_5km_indices = np.where(distances <= 5)[0]
        close = [
            {
                "name": hospitals[i]["name"],
                "address": hospitals[i]["address"],
                "coord": hospitals[i]["coordinates"],
                "distance": round(distances[i], 2)
            }
            for i in within_5km_indices
        ]

        closest_index = np.argmin(distances)
        closest = {
            "name": hospitals[closest_index]["name"],
            "address": hospitals[closest_index]["address"],
            "coord": hospitals[closest_index]["coordinates"],
            "distance": round(distances[closest_index], 2)
        }
        return {
            "allHospitalData": close,
            "closestHospital": closest
        }

    except Exception as e:
        print(f"gethospitalfailed: {e}")
        return None

def getCrime(coord):
    try:
        coord = Point(coord)
        print(f"coord {coord}")
        path = os.path.join(currentDir, "./cleaners/data/crimeData1.json")
        print(f"Path {[path]}")
        with open(path) as file:
            crime = json.load(file)

        inside = {}
        for each in crime["crimeData"]:
            poly = Polygon(each["poly"])
            if poly.contains(coord):
                inside = {
                    "areaName": each["areaName"],
                    "id": each["id"],
                    "population": each["population"],
                    "poly": each["poly"],
                    "crimeScore": each["crimeScore"]
                }
                break

        return inside

    except Exception as e:
        print("getcrime failed")
        print(str(e))

def getFire(coord):
    try:
        path = os.path.join(currentDir, "./cleaners/data/fire_locations.json")
        with open(path) as file:
            fire = json.load(file)
        close = []
        closest = {}

        min = 5

        for each in fire:
            station = (float(each['location'][1]), float(each['location'][0]))
            distance_km = haversine(station, coord, unit=Unit.KILOMETERS)
            if distance_km <= 5:
                close.append({
                    "station": station,
                    "distance": distance_km,
                    "address": each["address"]
                })
                if distance_km <= min:
                    closest = {
                        "station": station,
                        "closest": distance_km,
                        "address": each["address"]
                    }
                    min = distance_km

        return {
            "allFireStations": close,
            "closestStation": closest
        }

    except Exception as e:
        print(f"getFire failed: {e}")
        return None

def getPolice(coord):
    try:
        path = os.path.join(currentDir, "./cleaners/data/police_locations.json")
        with open (path, "r") as file:
            police = json.load(file)

        close = []
        closest = {}
        min = 5
        for each in police:
            department = (float(each["location"][1]), float(each["location"][0]))
            distance = haversine(department, coord, Unit.KILOMETERS)
            if distance <= 5:
                close.append({
                    "address": each["address"],
                    "facility": each["facility"],
                    "location": each["location"],
                    "id": each["id"],
                    "distance": distance
                })

                if distance <= min:
                    closest = {
                        "address": each["address"],
                        "facility": each["facility"],
                        "location": each["location"],
                        "id": each["id"],
                        "distance": distance
                    }
                    min = distance
        
        return ({
            "allDepartments": close,
            "closestDepartment": closest
        })
                
    except Exception as e:
        print("you bum")
        print(str(e))

def getParks(coord):
    try:
        path = os.path.join(currentDir, "./cleaners/data/parks_locations1.json")
        with open (path, "r") as file:
            parks = json.load(file)

        close = []
        closest = {}
        min = 2
        for each in parks:
            department = (float(each["location"][0][0]), float(each["location"][0][1]))
            distance = haversine(department, coord, Unit.KILOMETERS)
            if distance <= 2:
                for parkcoord in each["location"]:
                    closestDistance = haversine(coord, (float(parkcoord[0]), float(parkcoord[1])), Unit.KILOMETERS)
                    if (closestDistance < distance):
                        distance = closestDistance

                area = calculate_area(each['location'])
                close.append({
                    "name": each["name"],
                    "poly": each["location"],
                    "id": each["id"],
                    "distance": distance,
                    "area": area,
                })
                if distance <= min:
                    closest = {
                        "name": each["name"],
                        "poly": each["location"],
                        "id": each["id"],
                        "distance": distance,
                        "area": area
                    }
                    min = distance

        return ({
            "allPark": close,
            "closestPark": closest
        })
                
    except Exception as e:
        print("park bummy")
        print(str(e))

def getSchools(coord, schoolChoice):
    currentDir = os.path.dirname(__file__)
    path = os.path.join(currentDir, "./cleaners/data/school_locations.json")

    with open(path, "r") as file:
        schools = json.load(file)

    data = {}

    public = []
    private = []
    french = []
    catholic = []

    publicClosest = None
    privateClosest = None
    frenchClosest = None
    catholicClosest = None

    if schoolChoice == "public":
        publicMin = 1.5
        for each in schools["EP"]:
            location = (float(each["location"][0][1]), float(each["location"][0][0]))
            distance = haversine(location, coord, Unit.KILOMETERS)
            if distance <= 1.5:
                public.append({
                    "name": each["name"],
                    "address": each["address"],
                    "id": each["id"],
                    "distance": distance,
                    "coord": each["location"][0]
                })
                if distance <= publicMin:
                    publicClosest = {
                        "name": each["name"],
                        "address": each["address"],
                        "id": each["id"],
                        "distance": distance,
                        "coord": each["location"][0]
                    }
                    publicMin = distance
        data = {
            "schools": public,
            "closest": publicClosest
        }

    elif schoolChoice == "private":
        privateMin = 1.5
        for each in schools["PR"]:
            location = (float(each["location"][0][1]), float(each["location"][0][0]))
            distance = haversine(location, coord, Unit.KILOMETERS)
            if distance <= 1.5:
                private.append({
                    "name": each["name"],
                    "address": each["address"],
                    "id": each["id"],
                    "distance": distance,
                    "coord": each["location"][0]
                })
                if distance <= privateMin:
                    privateClosest = {
                        "name": each["name"],
                        "address": each["address"],
                        "id": each["id"],
                        "distance": distance,
                        "coord": each["location"][0]
                    }
                    privateMin = distance
        data = {
            "schools": private,
            "closest": privateClosest
        }

    elif schoolChoice == "french":
        frenchMin = 1.5
        for each in schools["FP"]:
            location = (float(each["location"][0][1]), float(each["location"][0][0]))
            distance = haversine(location, coord, Unit.KILOMETERS)
            if distance <= 1.5:
                french.append({
                    "name": each["name"],
                    "address": each["address"],
                    "id": each["id"],
                    "distance": distance,
                    "coord": each["location"][0]
                })
                if distance <= frenchMin:
                    frenchClosest = {
                        "name": each["name"],
                        "address": each["address"],
                        "id": each["id"],
                        "distance": distance,
                        "coord": each["location"][0]
                    }
                    frenchMin = distance
        data = {
            "schools": french,
            "closest": frenchClosest
        }
        
    elif schoolChoice == "catholic":
        catholicMin = 1.5
        for each in schools["ES"]:
            location = (float(each["location"][0][1]), float(each["location"][0][0]))
            distance = haversine(location, coord, Unit.KILOMETERS)
            if distance <= 1.5:
                catholic.append({
                    "name": each["name"],
                    "address": each["address"],
                    "id": each["id"],
                    "distance": distance,
                    "coord": each["location"][0]
                })
                if distance <= catholicMin:
                    catholicClosest = {
                        "name": each["name"],
                        "address": each["address"],
                        "id": each["id"],
                        "distance": distance,
                        "coord": each["location"][0]
                    }
                    catholicMin = distance
        data = {
            "schools": catholic,
            "closest": catholicClosest
        }
    

    return {
        "data": data
    }

def getList(address, schoolChoice):
    try:
        startTime = time.time()
        thebestdata = addressToCoord(address)
        
        coordinates = thebestdata["point"]

        newaddress = address.split(" ")
        
        for each in newaddress:
            try:
                float(each)
                booleanFor = True
            except:
                booleanFor = False

        if booleanFor == True:
            showaddress = thebestdata["address"].split(",")[0] + thebestdata["address"].split(",")[1] + thebestdata["address"].split(",")[2]

        else:
            showaddress = address

        fireData = getFire(coordinates)
        policeData = getPolice(coordinates)
        schoolData = getSchools(coordinates, schoolChoice)
        parkData = getParks(coordinates)
        crimeData = getCrime(coordinates)
        hospitalData = getHospitals(coordinates)    
        ttcData = getTTC(coordinates)    
        trafficData = getTraffic(coordinates)
        bikeData = getBike(coordinates)
        waterdata = getWater(coordinates)

        parkscore = getParkScore(allPark=parkData["allPark"], closestPark=parkData["closestPark"], water=waterdata)
        safetyScore = getSafetyScore(hospitalData=hospitalData, policeData=policeData, crimeArea=crimeData, closestFire=fireData["closestStation"])
        transportationScore = getTransportationScore(ttcData["closestTTCStation"], trafficData, bikeData)

        endtime = time.time()
        print(f"this is total time: {endtime-startTime}")

        return ({
            "fireData": fireData,
            "policeData": policeData,
            "schoolData": schoolData,
            "parkData": parkData,
            "home": coordinates,
            "crimeData": crimeData,
            "hospitalData": hospitalData,
            "homeAddress" : showaddress,
            "ttcData": ttcData,
            "bikeData": bikeData,
            "scores":{
                "parkScore": parkscore,
                "safetyScore": safetyScore,
                "transportationScore": transportationScore
            }

        })
    
    except Exception as e:
        print(str)
