from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.options import Options

from uzdevumi_answers import UzdAnswers

# wait.until(EC.presence_of_element_located((By.ID, "id-search-field"))) # wait until elements is loaded


def wait_and_click(xpath):
    el = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    el.click()


def check_if_completed(el):
    max_p = el.find_elements_by_class_name("max")
    if not len(max_p):
        return False
    earned_p = el.find_elements_by_class_name("earned")

    return int(max_p[0].text) == int(earned_p[0].text)


def check_if_finish():
    global driver
    points = driver.find_elements_by_xpath(
        "//div[contains(@class, 'exerc-points')]//span"
    )
    if not len(points) == 2:
        raise Exception("Was not able to locate task points")

    return int(points[0].text) == int(points[1].text[2:])


def solve_task():
    cur_answers = UzdAnswers()
    while not check_if_finish():
        cur_answers.add_answers()
        retry_href = driver.find_element_by_xpath(
            "//div[contains(@class, 'task-buttons')]//a"
        ).get_attribute("href")
        driver.get(retry_href)
        input()
        pass


options = webdriver.ChromeOptions()
options.add_argument(
    "user-data-dir=C:/Users/user/AppData/Local/Google/Chrome/User Data/Default"
)  # Path to your chrome profile

driver = webdriver.Chrome("C:/temp/chromedriver.exe", chrome_options=options)


wait = WebDriverWait(driver, 20)

driver.get("https://www.uzdevumi.lv/")
wait_and_click("//div[contains(@class, 'menu-list clearfix')]//div[6]")

subjects = driver.find_elements_by_xpath(
    "//ul[contains(@class, 'list-unstyled thumbnails')]//li"
)

print("Found :", len(subjects), " subjects")
# subj_id = int(input("Choose subject (enter from 0 to {}) : ".format(len(subjects) - 1)))

subj_id = 0

subjects[subj_id].click()

theme_hrefs = [
    el.get_attribute("href")
    for el in driver.find_elements_by_xpath(
        "//ol[contains(@class, 'list-unstyled topic-list')]//a"
    )
]

driver.get(theme_hrefs[0])

task_hrefs = [
    el.find_element_by_tag_name("a").get_attribute("href")
    for el in driver.find_elements_by_xpath(
        "//section[contains(@class, 'block sm-wide sm-easy-header exercise-block')]//tr"
    )
    if not check_if_completed(el)
]

for task in task_hrefs:
    driver.get(task)
    wait_and_click("//button[@id='submitAnswerBtn']")
    solve_task()


input()


driver.close()