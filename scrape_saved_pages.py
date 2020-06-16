from bs4 import BeautifulSoup
from slugify import slugify # this package is actually called python-slugify
from course_grader import grade_courses
from operator import itemgetter
import json
import os

# this file is for scraping the html pages that contain information about a single implementation

years = ["14-15", "15-16", "16-17", "17-18", "18-19", "19-20"]


def scrape_page(year):
    courses = []
    with os.scandir('single-html/' + year) as entries:
        for entry in entries:
            with open('single-html/' + year + "/" + entry.name, 'rb') as file:

                # Open file
                try:
                    soup = BeautifulSoup(file, features="lxml")
                except UnicodeDecodeError:
                    print("File " + year + "/" + entry.name + " Raised an UnicodeDecodeError when parsing HTML.")
                    continue

                # Find code && name of course
                try:
                    course_code = soup.find_all("nobr")[2].contents[0].strip().split("\n")[0]
                    course_name = soup.find_all("nobr")[2].contents[0].strip().split("\n")[2].strip()
                except IndexError:
                    print("File " + year + "/" + entry.name + " Raised an IndexError when finding the course name.")
                    continue

                # Find average grade
                try:
                    target_table = soup.find_all("table", {"class": "common"})[2]
                    average_row = target_table.find_all("tr")[2]
                    average_proto = average_row.find_all("td")[0].contents[0].strip()
                    average = float(average_proto)
                except ValueError:
                    print("Course " + year + "/" + course_code + " Raised a ValueError when converting average to a float.")
                    continue
                except IndexError:
                    print("Course " + year + "/" + course_code + " Raised an IndexError when finding the correct table.")
                    continue

                # Find answer count
                try:
                    target_table = soup.find_all("table", {"class": "common"})[2]
                    rows = target_table.find_all("tr")[5:11]
                    grade_distribution = []
                    for row in rows:
                        grade_distribution.append(int(float(row.find_all("td")[1].contents[0].strip())))
                    answer_count = sum(grade_distribution)
                except IndexError:
                    print("Course " + year + "/" + course_code + " Raised an IndexError when finding answer counts.")
                    continue

                # Find workload
                try:
                    target_table = soup.find_all("table", {"class": "common"})[2]
                    workload_row = target_table.find_all("tr", {"class": "odd"})[10]
                    workload_proto = workload_row.find_all("td")[0].contents[0].strip()
                    workload = int(round((float(workload_proto) - 2) * 100))
                except ValueError:
                    print("Course " + year + "/" + course_code + " Raised a ValueError when converting workload to float.")
                    continue
                except IndexError:
                    print("Course " + year + "/" + course_code + " Raised an IndexError when finding the workload.")
                    continue

                # Find period data
                try:
                    target_table = soup.find_all("table")[0]
                    periods = target_table.find_all("tr")[2].find("td").contents[0].split(",")[1].strip().split(" ")[1]

                except IndexError:
                    print("Course " + year + "/" + course_code + " Raised an IndexError when finding the correct period.")
                    continue

                if answer_count >= 1:

                    new_course = {
                        "code": course_code,
                        "name": course_name,
                        "work": workload,
                        "grade": average,
                        "period": periods,
                        "sampleSize": answer_count,
                        "sampleDistribution": grade_distribution,
                    }

                    courses.append(new_course)

                # print(year + " " + periods + " " + course_code + " " + course_name + " " + str(average) + " " + str(workload))

    return courses


def filter_courses(courses):

    reject_list = []

    for course in courses:

        # filter out KIE courses :D
        if "KIE-" in course['code']:
            reject_list.append(course)

        # filter out PLA courses (Pori)
        if "PLA-" in course['code']:
            reject_list.append(course)

        # filter out seminars
        if "graduate" in course['name'].lower() or "seminar" in course['name'].lower() or "seminaari" in course['name'].lower():
            reject_list.append(course)

        # filter out courses with english variants (end with 6 or 7)
        if course['code'].endswith("6"):
            template = course['code'][:-1] + "0"
            if any(template in d['code'] for d in courses):
                reject_list.append(course)
        if course['code'].endswith("7"):
            template = course['code'][:-1] + "0"
            if any(template in d['code'] for d in courses):
                reject_list.append(course)
            template = course['code'][:-1] + "1"
            if any(template in d['code'] for d in courses):
                reject_list.append(course)

    print(reject_list)

    for item in reject_list:
        courses[:] = [d for d in courses if d.get('code') != item['code']]

    print(courses)
    sorted_duplicates = sorted(reject_list, key=itemgetter('grade'), reverse=True)
    filtered_courses = sorted(courses, key=itemgetter('grade'), reverse=True) # sort list for grading
    return filtered_courses, sorted_duplicates


def compile():

    compiled_courses = []

    for year in years:
        with open((year + '.json'), 'rb') as file:
            courses = json.load(file)

        for course in courses:
            course_id = slugify(course["name"])
            instance = {
                "code": course["code"],
                "year": year,
                "grade": course["grade"],
                "work": course["work"],
                "sampleSize": course["sampleSize"],
                "period": course["period"],
            }
            if "letter" in course.keys():
                instance["letter"] = course["letter"]

            if not any(d["id"] == course_id for d in compiled_courses):
                new_course = {
                    "name": course["name"],
                    "id": course_id,
                    "instances": [
                        instance
                    ]
                }
                compiled_courses.append(new_course)
            else:
                for new_course in compiled_courses:
                    if new_course["name"] == course["name"]:
                        new_course["instances"].append(instance)

    with open('kaiku.json', 'w', encoding="utf-8") as outfile:
        json.dump(compiled_courses, outfile, indent=2, ensure_ascii=False)


for year in years:
    courses = scrape_page(year)
    accepted, rejected = filter_courses(courses)

    result = grade_courses(accepted)

    with open(year + '-rejects.json', 'w', encoding="utf-8") as outfile:
        json.dump(rejected, outfile, indent=2, ensure_ascii=False)

    with open(year + '.json', 'w', encoding="utf-8") as outfile:
        json.dump(result, outfile, indent=2, ensure_ascii=False)

compile()
