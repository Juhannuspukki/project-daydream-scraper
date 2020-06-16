from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json


# if driver not found: brew cask install chromedriver
# login
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.tut.fi/kaiku/examineFeedbackPage/feedback")

assert "TUNI Web Login" in driver.title
usernameElement = driver.find_element_by_id("username")
usernameElement.clear()
usernameElement.send_keys("username")

passwordElement = driver.find_element_by_id("password")
passwordElement.clear()
passwordElement.send_keys("password")

passwordElement.send_keys(Keys.RETURN)


# wait for login to complete
try:
    WebDriverWait(driver, 10).until(
        EC.title_is("Kaiku")
    )

except TimeoutException:
    print("Login timed out.")
    driver.quit()

# search

searchFieldElement = driver.find_element_by_id("searchForm.courseId")
searchFieldElement.clear()
searchFieldElement.send_keys("22100")
time.sleep(1)
searchFieldElement.send_keys(Keys.RETURN)

with open('faculties.json', 'rb') as file:
    courses = json.load(file)

codes = []

for item in courses:
    codes.append(item["name"])

print(codes)

for character in codes:

    driver.get("https://www.tut.fi/kaiku/examineFeedbackPage/feedback")

    time.sleep(1)

    searchFieldElement = driver.find_element_by_id("searchForm.courseId")
    searchFieldElement.clear()
    searchFieldElement.send_keys(character + "-")
    time.sleep(1)
    searchFieldElement.send_keys(Keys.RETURN)

    time.sleep(1)

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "common"))
        )
        f = open('kaiku-18-19-' + character + '.html', 'w')
        f.write(driver.page_source)
        f.close()

        time.sleep(1)

    except TimeoutException:
        print("Search timed out.")

print("Done.")

driver.close()

# find data
