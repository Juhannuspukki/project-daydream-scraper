from slugify import slugify # this package is actually called python-slugify
import json

fileList = ["kaiku-14-15-new", "kaiku-15-16-new", "kaiku-16-17-new", "kaiku-17-18-new", "kaiku-18-19-new", "kaiku-19-20-new"]

newSon = []

for fileName in fileList:
    with open((fileName + '.json'), 'rb') as file:
        courses = json.load(file)
    for course in courses:
        ide = slugify(course["name"] + "-" + course["period"])
        instance = {
                        "code": course["code"],
                        "year": fileName[6:11],
                        "grade": course["grade"],
                        "work": course["work"],
                        "sampleSize": course["sampleSize"]
                    }
        if "letter" in course.keys():
            instance["letter"] = course["letter"]
        if not any(d["id"] == ide for d in newSon):
            newCourse = {
                "name": course["name"],
                "id": ide,
                "period": course["period"],
                "instances": [
                    instance
                ]
            }
            newSon.append(newCourse)
        else:
            for newCourse in newSon:
                if newCourse["name"] == course["name"] and newCourse["period"] == course["period"]:
                    newCourse["instances"].append(instance)


# POP is no longer in use

# with open('pop-master.json', 'rb') as file:
#     courses = json.load(file)
#
# for course in courses:
#     for item in newSon:
#         if item["name"] == course["name"]:
#             item["link"] = course["link"]
#
# for course in courses:
#     years = []
#     for instance in course["instances"]:
#         if instance["year"] in years:
#             print(course["id"])
#         years.append(instance["year"])


with open('kaiku-compiled.json', 'w', encoding="utf-8") as outfile:
    json.dump(newSon, outfile, indent=2, ensure_ascii=False)
