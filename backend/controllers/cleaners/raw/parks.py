import json

# for fire

fireData = []

# with open("parks_locations.json", "r") as fire:
#     data = json.load(fire)
#     for each in data:
#         if "cemetery" not in each['name'].lower():
#             fireData.append({
#                 "name": each['name'],
#                 "id": each['id'],
#                 "location": each['location']
#             })

with open("parks_locations1.json", "r") as fire:
    data = json.load(fire)
    for each in data:
        flipped = [[coord[1], coord[0]] for coord in each['location']]
        fireData.append({
            "name": each['name'],
            "id": each['id'],
            "location": flipped
            })

with open('parks_locations1.json', 'w') as fire:
    json.dump(fireData, fire, indent=4)
