import requests
from bs4 import BeautifulSoup

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
        return(rating_string)
    else:
        return("Rating not found")

print(googleReview("INGLEWOOD PARKETTE"))