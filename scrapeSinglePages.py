import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import uuid

# if driver not found: brew cask install chromedriver

# login
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.tut.fi/kaiku/examineFeedbackPage/feedback")

assert "TUNI Web Login" in driver.title
usernameElement = driver.find_element_by_id("username")
usernameElement.clear()
usernameElement.send_keys("name")

passwordElement = driver.find_element_by_id("password")
passwordElement.clear()
passwordElement.send_keys("pw")

passwordElement.send_keys(Keys.RETURN)


# wait for login to complete
try:
    WebDriverWait(driver, 10).until(
        EC.title_is("Kaiku")
    )

except TimeoutException:
    print("Login timed out.")
    driver.quit()

with open('scrapeEverything/courseList-kaiku-19-20.json', 'rb') as file:
    courses = json.load(file)

length = str(len(courses))
x = 0

for courseUrl in courses:
    x += 1
    processedLinkIndex = 0

    print(courseUrl)
    print("Processing " + str(x) + "/" + length)

    courseCode = courseUrl.split("&")[0]

    try:
        while True:
            driver.get('https://www.tut.fi/kaiku/examineFeedbackPage/feedback?action=resultsForCourseQueries&courseCode=' + courseUrl)

            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "common"))
            )

            form = driver.find_element_by_class_name("common")
            formLinks = form.find_elements_by_tag_name("a")

            maxLinkIndex = len(formLinks)

            if maxLinkIndex == 0:
                break

            formLinks[processedLinkIndex].click()

            parsedHTML = BeautifulSoup(driver.page_source, 'html.parser').prettify()

            f = open('single-html/' + "19-20" + '-' + courseCode + "-" + str(uuid.uuid4()) + '.html', 'w')
            f.write(parsedHTML)
            f.close()

            time.sleep(0.5)

            processedLinkIndex += 1

            if processedLinkIndex >= maxLinkIndex:
                break


    except TimeoutException as e:
        print("Search timed out at " + str(x))


print("Done.")

driver.close()