import requests
import pyproj    
from functools import partial
from shapely.geometry import Polygon
from shapely.ops import transform
import urllib.request
import json
import requests
from bs4 import BeautifulSoup

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

        address = data[0]["display_name"]
        toreturn = {
            "point": (float(lat), float(lon)),
            "address": address
        }

        return (toreturn) 
    except:
        print("address to coord no work")


def calculate_area(coords):
    polygon = []
    for each in coords:
        polygon.append((float(each[1]), float(each[0])))

    polygon = Polygon(polygon)
    
    aea_proj = partial(
        pyproj.Transformer.from_crs,
        pyproj.CRS('EPSG:4326'),
        pyproj.CRS(proj='aea', lat_1=polygon.bounds[1], lat_2=polygon.bounds[3]) 
    )
    
    transformed_polygon = transform(aea_proj().transform, polygon)
    
    area = transformed_polygon.area

    return area

def googleReview(park):
    park = park.split(" ")
    newpark = []
    for i, each in enumerate(park):
        if i != (len(park)-1):
            newpark.append(each + "+")
        else:
            newpark.append(each)

    newpark = "".join(newpark)

    response = requests.get("https://www.google.com/search", params={
                "q": newpark
            })

    soup = BeautifulSoup(response.text, "html.parser")

    rating_element = soup.find('div', class_='Hk2yDb KsR1A')
    if rating_element and rating_element.has_attr('aria-label'):
        rating_string = rating_element['aria-label']
        numberRating = rating_string.split(" ")[1]
        print("num")
        return (numberRating)
    else:
        return("Rating not found")