import json
import requests
from bs4 import BeautifulSoup
import datetime
from multiprocessing import Pool


def getAllPages(fileName):
    with open(('scrapeEverything/' + fileName + '.json'), 'rb') as file:
        courses = json.load(file)

    length = len(courses)
    x = 0

    list = []

    for course in courses:
        x += 1
        print("Processing " + str(x) + "/" + str(length) + " of " + fileName)

        url = "https://www.tut.fi/kaiku/examineFeedbackPage/feedback?action=resultsForCourseQueries&courseCode=" + course
        cookies = {"JSESSION_KAIKU_ID": "öö",
                   "GUEST_LANGUAGE_ID": "fi_FI",
                   "lb_selection": "öö",
                   "_shibsession_öööö": "öö"}

        r = requests.get(url, cookies=cookies)
        html = " ".join(r.text.split())

        print(datetime.datetime.now())
        parsedHTML = BeautifulSoup(html, 'html.parser').prettify()

        f = open('list-html/' + fileName[-5:] + '-' + course[:200] + '.html', 'w')
        f.write(parsedHTML)
        f.close()

        soup = BeautifulSoup(html, features="lxml")
        soup = soup.find("table", {"class": "common"})
        soup = soup.find_all("tr", ["even", "odd"])
        del soup[-1]

        for elements in soup:
            try:
                single = elements.find_all("td")
                link = single[0].a['href']
                list.append(link)

            except (AttributeError, ValueError, IndexError, TypeError) as e:
                pass

    with open(('linkList' + fileName + '.json'), 'w', encoding="utf-8") as outfile:
        json.dump(list, outfile, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    with Pool(6) as p:
        p.map(getAllPages,
              [
                  "courseList-kaiku-14-15",
                  "courseList-kaiku-15-16",
                  "courseList-kaiku-16-17",
                  "courseList-kaiku-17-18",
                  "courseList-kaiku-18-19",
                  "courseList-kaiku-19-20"
              ]
              )
