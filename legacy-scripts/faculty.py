import json

yearList = ["14-15", "15-16", "16-17", "17-18", "18-19"]

totals = []

with open('kaiku.json', 'rb') as file:
    courses = json.load(file)

for course in courses:
    for instance in course["instances"]:
        if instance["sampleSize"] > 20:
            # search by code
            facultyIndex = next((index for (index, d) in enumerate(totals) if d["name"] == instance["code"][:3]), None)
            if facultyIndex is None:
                totals.append({"name": instance["code"][:3],
                               "data": [{
                                   "year": instance["year"],
                                   "grade": instance["grade"],
                                   "sampleSize": instance["sampleSize"],
                                   "work": instance["work"],
                                   "courseCount": 1,
                               }]
                               })
            else:
                facultyDataList = totals[facultyIndex]["data"]
                # search by year
                courseIndex = next((index for (index, d) in enumerate(facultyDataList) if d["year"] == instance["year"]), None)
                if courseIndex is None:
                    facultyDataList.append({
                                        "year": instance["year"],
                                        "grade": instance["grade"],
                                        "sampleSize": instance["sampleSize"],
                                        "work": instance["work"],
                                        "courseCount": 1,
                                   })
                else:
                    facultyDataList[courseIndex]["grade"] += instance["grade"]
                    facultyDataList[courseIndex]["sampleSize"] += instance["sampleSize"]
                    facultyDataList[courseIndex]["work"] += instance["work"]
                    facultyDataList[courseIndex]["courseCount"] += 1


for total in totals:
    for year in total["data"]:
        try:
            year["grade"] = round((year["grade"] / year["courseCount"]), 2)
            year["work"] = round((year["work"] / year["courseCount"]), 2)
        except KeyError:
            pass
    try:
        total["data"][:] = [d for d in total["data"] if d.get('courseCount') > 4]
    except TypeError:
        pass

totals[:] = [d for d in totals if len(d.get('data')) != 0]
totals[:] = [d for d in totals if d.get('name') != "YHT"]

for total in totals:
    for year in yearList:
        if not [d for d in total["data"] if d.get('year') == year]:
            total["data"].append({"year": year})

    total["data"] = sorted(total["data"], key=lambda i: i['year'])

totals = sorted(totals, key=lambda i: i['name'])

with open(('faculties.json'), 'w', encoding="utf-8") as outfile:
    json.dump(totals, outfile, indent=2, ensure_ascii=False)
