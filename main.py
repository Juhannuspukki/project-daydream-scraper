from bs4 import BeautifulSoup
from operator import itemgetter
import json
import math

fileList = ["kaiku-14-15", "kaiku-15-16", "kaiku-16-17", "kaiku-17-18", "kaiku-18-19"]

previous = []

for fileName in fileList:
    with open((fileName + '.html'), 'rb') as file:
        soup = BeautifulSoup(file, features="lxml")
    soup = soup.find("table", {"class": "common"})
    soup = soup.find_all("tr", ["even", "odd"])  # find correct elements
    courseList = []

    for elements in soup:
        single = elements.find_all("td")
        courseData = {}

        try:
            name = single[0].a.string.strip().split()  # split course name to code and name
            courseData["code"] = name[0]
            courseData["name"] = " ".join(name[1:])  # save them separately

            totalGrade = 0
            grades = single[1].string.strip().split(" / ")
            for i in range(6):
                totalGrade += i * int(grades[i])
            courseData["grade"] = totalGrade / 100  # calculate avg for grades and scale it to 0-5

            totalWork = 0
            works = single[3].string.strip().split(" / ")

            for i in range(3):
                totalWork += i * int(works[i])
            courseData["work"] = (totalWork - 100)
            courseData["sampleSize"] = int(single[4].string.strip())-int(single[5].string.strip())  # ignore people who dont give feedback

        except (AttributeError, ValueError, IndexError) as e:
            pass

        if len(courseData) > 2 and courseData["sampleSize"] >= 5:
            courseList.append(courseData)

    # filter out KIE courses :D

    courseList[:] = [d for d in courseList if "KIE-" not in d.get('code')]

    # filter out PLA courses (Pori)

    courseList[:] = [d for d in courseList if "PLA-" not in d.get('code')]

    # filter out courses with english variants

    duplicateList = []

    for course in courseList:
        if course['code'].endswith("6"):
            template = course['code'][:-1] + "0"
            if any(template in d['code'] for d in courseList):
                duplicateList.append(course['code'])

    for item in duplicateList:
        courseList[:] = [d for d in courseList if d.get('code') != item]

    courseList = sorted(courseList, key=itemgetter('grade'), reverse=True)  # sort list for grading

    totalItems = len(courseList)

    gradeableItems = 0
    for item in courseList:
        if item["sampleSize"] >= 21:
            gradeableItems += 1

    letterWeights = [math.ceil(gradeableItems*0.05),
                      math.ceil(gradeableItems*0.15),
                      math.ceil(gradeableItems*0.20),
                      math.floor(gradeableItems * 0.24),
                      math.floor(gradeableItems * 0.20),
                      math.floor(gradeableItems * 0.11)]

    letterWeights.append(gradeableItems - sum(letterWeights))

    letters = ["L", "E", "M", "C", "B", "A", "I"]

    weightCounter = 0
    letterCounter = 0
    totalCounter = 0
    print(letterWeights)

    for i in range(totalItems):
        if courseList[i]["sampleSize"] >= 21:
            try:
                if totalCounter < letterWeights[weightCounter]:
                    courseList[i]["letter"] = letters[letterCounter]
                    totalCounter += 1
                if totalCounter == letterWeights[weightCounter]:
                    weightCounter += 1
                    letterCounter += 1
                    totalCounter = 0
            except IndexError:
                break

    gradeSum = 0
    for stuff in courseList:
        gradeSum += stuff["grade"]

    print("List length", len(courseList))
    print("Average", gradeSum/len(courseList))

    if previous:
        for course in courseList:
            for previousCourse in previous:
                if previousCourse["code"] == course["code"]:
                    delta = course["grade"] - previousCourse["grade"]
                    course["gradeDelta"] = round(delta, 3)
                    delta = course["work"] - previousCourse["work"]
                    course["workDelta"] = round(delta, 3)

    previous = courseList

    with open((fileName + '.json'), 'w', encoding="utf-8") as outfile:
        json.dump(courseList, outfile, indent=2, ensure_ascii=False)
