from bs4 import BeautifulSoup
import json


def parseCourses(fileName):
    print("Processing " + fileName)

    with open((fileName + '.html'), 'rb') as file:
        soup = BeautifulSoup(file, features="lxml")
    soup = soup.find("table", {"class": "dataTable"})
    soup = soup.find_all("tr", {"role": "row"})  # find correct elements
    courseList = []

    for elements in soup:
        single = elements.find_all("td")
        try:
            single = single[1]
            name = single.a.string.strip()
            link = single.a['href'][75:]
            print(name, link)
            courseList.append({"name": name, "link": link})
        except IndexError:
            pass

    return courseList


courseLinks = []
for i in range(10):
    courseList = parseCourses("pop-19-20-" + str(i))
    courseLinks += courseList


with open('pop-master.json', 'w', encoding="utf-8") as outfile:
    json.dump(courseLinks, outfile, indent=2, ensure_ascii=False)
