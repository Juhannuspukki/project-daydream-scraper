import json

from courseParser import analyze
from courseParser import gradeCourses
from getPeriodData import getPeriodData

# RUN THIS FIRST and uncomment "analyze" before you do
analyze()


fileList = ["kaiku-17-18"]

for fileName in fileList:
    print("\n\n\n" + fileName + "\n\n\n")
    courseList = getPeriodData(fileName)
    with open((fileName + '-new.json'), 'w', encoding="utf-8") as outfile:
        json.dump(gradeCourses(courseList), outfile, indent=2, ensure_ascii=False)

# After this, run crawlKaiku
# After that, run compiler
