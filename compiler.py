from courseparser import analyze
from slugify import slugify
import json

analyze()

fileList = ["kaiku-14-15", "kaiku-15-16", "kaiku-16-17", "kaiku-17-18", "kaiku-18-19"]

newSon = []

for fileName in fileList:
    with open((fileName + '.json'), 'rb') as file:
        courses = json.load(file)
    for course in courses:
        instance = {
                        "code": course["code"],
                        "year": fileName[6:11],
                        "grade": course["grade"],
                        "work": course["work"],
                        "sampleSize": course["sampleSize"]
                    }
        if "letter" in course.keys():
            instance["letter"] = course["letter"]
        if not any(d["name"] == course["name"] for d in newSon):
            newCourse = {
                "name": course["name"],
                "id": slugify(course["name"]),
                "instances": [
                    instance
                ]
            }
            newSon.append(newCourse)
        else:
            for newCourse in newSon:
                if newCourse["name"] == course["name"]:
                    newCourse["instances"].append(instance)


with open('pop-master.json', 'rb') as file:
    courses = json.load(file)

for course in courses:
    for item in newSon:
        if item["name"] == course["name"]:
            item["link"] = course["link"]


with open(('kaiku.json'), 'w', encoding="utf-8") as outfile:
    json.dump(newSon, outfile, indent=2, ensure_ascii=False)
