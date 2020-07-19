import json
with open(('kaiku.json'), 'rb') as file:
    courses = json.load(file)

ids = []
# perform diagnostics
for course in courses:
    years = []
    if course["id"] in ids:
        print("Duplicate id: " + course["id"])
    years.append(course["id"])
    for instance in course["instances"]:
        if instance["year"] in years:
            print(course["id"])
        years.append(instance["year"])
