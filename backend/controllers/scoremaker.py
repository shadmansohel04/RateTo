
def getTransportationScore(closestTTC, TrafficData, bikeData):
    try:
        if(len(bikeData) > 0):
            totalLength = 0
            for each in bikeData:
                totalLength += each["fromCoord"]
            if(totalLength > 800):
                totalLength = 0.9
            elif totalLength > 600:
                totalLength = 0.8
            elif totalLength > 500:
                totalLength = 0.7
            elif totalLength > 400:
                totalLength = 0.6
            elif totalLength > 300:
                totalLength = 0.5
            elif totalLength > 200:
                totalLength = 0.4
            else:
                totalLength = 0.3

        if closestTTC:
            distance = closestTTC["distance"]    
            if distance < 1:
                distance = 0.9
            elif distance < 1.5:
                distance = 0.8
            elif distance <= 2:
                distance = 0.7
            else:
                distance = 0.6
        
        if(len(TrafficData) > 0):
            traffic = 0
            for each in TrafficData:
                traffic += (each["count"]/ (each["distance"] * 1000))
            traffic = traffic/len(TrafficData)
            if (traffic <= 2):
                traffic = 0.9
            elif(traffic <= 4):
                traffic = 0.8
            elif (traffic <= 6):
                traffic = 0.75
            elif (traffic <= 7):
                traffic = 0.65
            elif (traffic <= 9):
                traffic = 0.55
            elif (traffic <= 10):
                traffic = 0.45
            else:
                traffic = 0.25
        

        if closestTTC and len(TrafficData) > 0 and len(bikeData) > 0:
            score = (traffic*2 + (distance*3) + totalLength)/6

        elif len(TrafficData) > 0 and len(bikeData) > 0:
            score = (traffic*2 + 0.7 + totalLength)/4

        elif closestTTC and len(TrafficData) > 0 and len(bikeData) == 0:
            score = (traffic*2 + distance)/3

        elif closestTTC and len(TrafficData) == 0 and len(bikeData) > 0:
            score = (distance + totalLength)/2

        elif closestTTC:
            score = (distance + 0.75)/2

        elif len(TrafficData) > 0:
            score = (traffic*2 + 0.7)/3

        elif len(bikeData) > 0:
            score = (totalLength + 0.77)/2

        else:
            score = -1
        
        return round(score*100, 2)
    
    except Exception as e:
    
        print(f"{str(e)}")
        return -1

def getArea (closestscore):
    if closestscore > 1000000:
        closestscore = 1
    elif closestscore > 100000:
        closestscore = 0.8
    elif closestscore > 10000:
        closestscore = 0.75
    elif closestscore > 1000:
        closestscore = 0.7
    elif closestscore > 50:
        closestscore = 0.6
    else:
        closestscore = 0.4
    return closestscore

def getParkScore(allPark, closestPark, water):
    try:

        closestscore = closestPark["area"]/((closestPark["distance"]) *1000)

        closestscore = getArea(closestscore)

        maxscore = 0
        for each in allPark:
            parkscoreInd = each["area"]/each["distance"]
            parkscoreInd = getArea(parkscoreInd)
            if(each["distance"] > 1.5):
                parkscoreInd -= 0.2
            elif(each["distance"] > 1):
                parkscoreInd -= 0.05
            if(parkscoreInd > maxscore):
                maxscore = parkscoreInd

        if water > 0:
            if water < 1.5:
                water = 1
            elif water < 3:
                water = 0.85
            elif water < 5:
                water = 0.8
            elif water < 10:
                water = 0.75
            else:
                water = None
        else:
            water = None
        

        if water:
            score = (((0.25 *closestscore) + maxscore + water)/2.25)*100

        else:
            score = (((0.25*closestscore) + maxscore + 0.7)/2.25)*100

        return round(score, 2)
    except Exception as e:
        return -1

def getSafetyScore(hospitalData, policeData, crimeArea, closestFire):
    try:
        closestHospital = hospitalData["closestHospital"]["closest"]

        if(closestHospital <= 2):
            closestHospital = 0.9
        elif(closestHospital <= 3):
            closestHospital = 0.8
        elif(closestHospital <= 4):
            closestHospital = 0.75
        else:
            closestHospital = 0.7

        crimeScore = crimeArea["crimeScore"]
        distance = policeData["closestDepartment"]["distance"]

        if (distance <= 1):
            distance = 0.9
        elif (distance <= 2):
            distance = 0.85
        elif (distance <= 4):
            distance = 0.75
        elif distance <= 5:
            distance = 0.7
        else:
            distance = 0.6

        distance *= 0.5

        if(crimeScore <= 5):
            crimeScore = 0.95
        elif(crimeScore <= 10):
            crimeScore = 0.85 
        elif(crimeScore <= 20):
            crimeScore = 0.8
        elif(crimeScore <= 30):
            crimeScore = 0.7
        elif(crimeScore <= 50):
            crimeScore = 0.6
        elif(crimeScore <= 60):
            crimeScore = 0.5
        elif(crimeScore <= 70):
            crimeScore = 0.4
        elif(crimeScore > 70):
            crimeScore = 0.1      

        firedist = closestFire["closest"]
 
        if (firedist <= 1):
            firedist = 0.9
        elif (firedist <= 2):
            firedist = 0.85
        elif (firedist <= 4):
            firedist = 0.75
        elif firedist <= 5:
            firedist = 0.7
        else:
            firedist = 0.6

        firedist *= 0.5
        
        if closestHospital is not None and distance is not None and firedist is not None:
            finalScore = round(((crimeScore + distance + firedist + closestHospital) / 3 * 100), 2)
        elif crimeScore is None and distance is not None and firedist is not None and closestHospital is not None:
            finalScore = round(((distance + firedist + closestHospital) / 2 * 100), 2)
        elif crimeScore is not None and distance is None and firedist is not None and closestHospital is not None:
            finalScore = round(((crimeScore + firedist + closestHospital) / 3 * 100), 2)
        elif crimeScore is not None and distance is not None and firedist is None and closestHospital is not None:
            finalScore = round(((crimeScore + distance + closestHospital) / 3 * 100), 2)
        elif crimeScore is not None and distance is not None and firedist is not None and closestHospital is None:
            finalScore = round(((crimeScore + distance + firedist) / 3 * 100), 2)
        elif crimeScore is None and distance is None and firedist is not None and closestHospital is not None:
            finalScore = round(((firedist + closestHospital) / 1 * 100), 2)
        elif crimeScore is None and distance is not None and firedist is None and closestHospital is not None:
            finalScore = round(((distance + closestHospital) / 2 * 100), 2)
        elif crimeScore is None and distance is not None and firedist is not None and closestHospital is None:
            finalScore = round(((distance + firedist) / 1 * 100), 2)
        elif crimeScore is not None and distance is None and firedist is None and closestHospital is not None:
            finalScore = round(((crimeScore + closestHospital) / 2 * 100), 2)
        elif crimeScore is not None and distance is None and firedist is not None and closestHospital is None:
            finalScore = round(((crimeScore + firedist) / 2 * 100), 2)
        elif crimeScore is not None and distance is not None and firedist is None and closestHospital is None:
            finalScore = round(((crimeScore + distance) / 2 * 100), 2)
        elif crimeScore is not None and distance is None and firedist is None and closestHospital is None:
            finalScore = round((crimeScore * 100), 2)
        elif crimeScore is None and distance is not None and firedist is None and closestHospital is None:
            finalScore = round((distance * 100), 2)
        elif crimeScore is None and distance is None and firedist is not None and closestHospital is None:
            finalScore = round((firedist * 100), 2)
        elif crimeScore is None and distance is None and firedist is None and closestHospital is not None:
            finalScore = round((closestHospital * 100), 2)    
        return finalScore
    except:
        return -1