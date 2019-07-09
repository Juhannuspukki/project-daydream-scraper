from bs4 import BeautifulSoup
from operator import itemgetter
import json
import math


def parseCourses(fileName):
    print("Processing " + fileName)

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

    return sorted(courseList, key=itemgetter('grade'), reverse=True)  # sort list for grading


def gradeCourses(courseList):
    # only contains the items that will be graded
    gradeableItems = []

    for item in courseList:
        if item["sampleSize"] >= 21:
            gradeableItems.append(item)

    gradeableCount = len(gradeableItems)

    letterWeights = [
        math.ceil(gradeableCount*0.05),
        math.ceil(gradeableCount*0.15),
        math.ceil(gradeableCount*0.20),
        math.floor(gradeableCount * 0.24),
        math.floor(gradeableCount * 0.20),
        math.floor(gradeableCount * 0.11)
    ]

    sumOfLetterWeights = sum(letterWeights)

    # assign improbaturs
    letterWeights.append(gradeableCount - sumOfLetterWeights)

    letters = ["L", "E", "M", "C", "B", "A", "I"]

    # tells which letter you are on
    letterCounter = 0

    # count courses that have received a "too good" grade due to rounding
    done = [0, 0]

    # tells how many courses of this letter have been graded
    totalCounter = 1

    print(letterWeights)

    gradeableItems[0]["letter"] = letters[0]

    for i in range(1, len(gradeableItems)):
        if totalCounter >= letterWeights[letterCounter] and gradeableItems[i]["grade"] == gradeableItems[i - 1]["grade"]:
            gradeableItems[i]["letter"] = gradeableItems[i - 1]["letter"]
            done[1] += 1
            totalCounter += 1

        elif totalCounter >= letterWeights[letterCounter]:
            try:
                gradeableItems[i]["letter"] = letters[letterCounter+1]
                letterWeights[letterCounter+1] -= sum(done)
                letterCounter += 1
            except IndexError:
                gradeableItems[i]["letter"] = letters[letterCounter]
            done[0] = done[1]
            done[1] = 0
            totalCounter = 0
        else:
            gradeableItems[i]["letter"] = gradeableItems[i - 1]["letter"]
            totalCounter += 1

    print("List length", len(gradeableItems), len(courseList))

    return courseList


def analyze():
    fileList = ["kaiku-14-15", "kaiku-15-16", "kaiku-16-17", "kaiku-17-18"]

    for fileName in fileList:
        courseList = parseCourses(fileName)
        with open((fileName + '.json'), 'w', encoding="utf-8") as outfile:
            json.dump(gradeCourses(courseList), outfile, indent=2, ensure_ascii=False)

    courses = []

    for i in range(10):
        courseList = parseCourses("kaiku-18-19-" + str(i))
        courses = courses + courseList

    courses = gradeCourses(sorted(courses, key=itemgetter('grade'), reverse=True))
    with open('kaiku-18-19.json', 'w', encoding="utf-8") as outfile:
        json.dump(courses, outfile, indent=2, ensure_ascii=False)
