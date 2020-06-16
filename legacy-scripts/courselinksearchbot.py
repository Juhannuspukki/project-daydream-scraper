from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

import time

# if driver not found: brew cask install chromedriver
# login
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://poprock.tut.fi/group/pop/opas/haku/opintojaksot")

assert "TUNI Web Login" in driver.title
usernameElement = driver.find_element_by_id("username")
usernameElement.clear()
usernameElement.send_keys("usr")

passwordElement = driver.find_element_by_id("password")
passwordElement.clear()
passwordElement.send_keys("pw")

passwordElement.send_keys(Keys.RETURN)


# wait for login to complete
try:
    WebDriverWait(driver, 10).until(
        EC.title_is("Opintojaksot - POP")
    )

except TimeoutException:
    print("Login timed out.")
    driver.quit()

# search

searchFieldElement = driver.find_element_by_id("course")
select = Select(driver.find_element_by_id('studyguide-search-year'))
select.select_by_value('288')
searchFieldElement.clear()
time.sleep(1)
searchFieldElement.send_keys("221")
time.sleep(1)
searchFieldElement.send_keys(Keys.RETURN)
time.sleep(3)
print("Initial test complete.")

for i in range(10):

    driver.get("https://poprock.tut.fi/group/pop/opas/haku/opintojaksot")

    searchFieldElement = driver.find_element_by_id("course")
    select = Select(driver.find_element_by_id('studyguide-search-year'))
    select.select_by_value('288')
    searchFieldElement.clear()
    searchFieldElement.send_keys("-" + str(i))
    time.sleep(1)
    searchFieldElement.send_keys(Keys.RETURN)
    time.sleep(1)

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "table-striped"))
        )
        f = open('pop-19-20-' + str(i) + '.html', 'w')
        f.write(driver.page_source)
        f.close()

        print(str(i) + " of 9")

    except TimeoutException:
        print("Search timed out.")

print("Done.")

driver.close()
