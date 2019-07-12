import requests
from bs4 import BeautifulSoup
from operator import itemgetter
import json
from courseparser import gradeCourses


def getPeriodData(fileName):
    with open((fileName + '.json'), 'rb') as file:
        courses = json.load(file)

    newCourses = []

    length = len(courses)
    x = 0
    for course in courses:
        url = "https://www.tut.fi/kaiku/examineFeedbackPage/feedback?action=resultsForCourseQueries&courseCode=" + course["source"]
        cookies = {"JSESSION_KAIKU_ID": "ööö",
                   "GUEST_LANGUAGE_ID": "fi_FI",
                   "lb_selection": "öö",
                   "_shibsession_öö": "ööö"}

        r = requests.get(url, cookies=cookies)
        html = " ".join(r.text.split())

        parsedHTML = BeautifulSoup(html, 'html.parser').prettify()

        soup = BeautifulSoup(html, features="lxml")
        soup = soup.find("table", {"class": "common"})
        soup = soup.find_all("tr", ["even", "odd"])
        del soup[-1]

        courseData = []
        x += 1

        for elements in soup:
            single = elements.find_all("td")
            if "colspan" in single[0].attrs.keys():
                period = single[0].string[33:].split()[0]
                courseData.append({"period": period})
            try:
                totalGrade = 0
                grades = single[1].string.strip().split(" / ")
                for i in range(6):
                    totalGrade += i * int(grades[i])
                courseData[-1]["grade"] = totalGrade / 100  # calculate avg for grades and scale it to 0-5

                totalWork = 0
                works = single[3].string.strip().split(" / ")

                courseData[-1]["name"] = course["name"]
                courseData[-1]["code"] = course["code"]

                for i in range(3):
                    totalWork += i * int(works[i])
                courseData[-1]["work"] = (totalWork - 100)
                courseData[-1]["sampleSize"] = int(single[4].string.strip()) - int(single[5].string.strip())  # ignore people who dont give feedback
            except (AttributeError, ValueError, IndexError) as e:
                pass

        print(courseData)
        for items in courseData:
            if len(items) > 3 and items["sampleSize"] >= 5:
                newCourses.append(items)

        print("Processing " + str(x) + "/" + str(length) + " of " + fileName)

    return sorted(newCourses, key=itemgetter('grade'), reverse=True)


fileList = ["kaiku-14-15", "kaiku-15-16", "kaiku-16-17", "kaiku-17-18"]

for fileName in fileList:
    print("\n\n\n" + fileName + "\n\n\n")
    courseList = getPeriodData(fileName)
    with open((fileName + '-new.json'), 'w', encoding="utf-8") as outfile:
        json.dump(gradeCourses(courseList), outfile, indent=2, ensure_ascii=False)
