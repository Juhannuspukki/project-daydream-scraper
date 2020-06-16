from bs4 import BeautifulSoup
import json

def findLinks(fileName):
    print("Processing " + fileName)

    with open(("kaiku-html/" + fileName + '.html'), 'rb') as file:
        soup = BeautifulSoup(file, features="lxml")
    soup = soup.find("table", {"class": "common"})
    soup = soup.find_all("tr", ["even", "odd"])  # find correct elements
    courseList = []

    for elements in soup:
        single = elements.find_all("td")

        try:
            source = single[0].a['href'][78:]
            courseList.append(source)
            print(source)

        except (AttributeError, ValueError, IndexError, TypeError) as e:
            pass

    return courseList


fileList = ["kaiku-14-15", "kaiku-15-16", "kaiku-16-17", "kaiku-17-18"]

for fileName in fileList:
    courseList = findLinks(fileName)
    with open(('courseList-' + fileName + '.json'), 'w', encoding="utf-8") as outfile:
        json.dump(courseList, outfile, indent=2, ensure_ascii=False)

# Year 18-19 is in several files

courses = []

for i in range(10):
    courseList = findLinks("kaiku-18-19-" + str(i))
    courses = courses + courseList

with open('courseList-kaiku-18-19.json', 'w', encoding="utf-8") as outfile:
    json.dump(courses, outfile, indent=2, ensure_ascii=False)

# Year 19-20 is also in several files

courses = []

for i in range(10):
    courseList = findLinks("kaiku-19-20-" + str(i))
    courses = courses + courseList

with open('courseList-kaiku-19-20.json', 'w', encoding="utf-8") as outfile:
    json.dump(courses, outfile, indent=2, ensure_ascii=False)
