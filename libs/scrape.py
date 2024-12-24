from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from libs.utils import create_url

# teams and weeks are 1-indexed
teams = range(1, 7)
weeks = range(1, 2)

def start_driver():
    options = webdriver.ChromeOptions()
    options.add_argument(argument="--headless")
    driver = webdriver.Chrome(options=options)
    return driver

# generate bs4 for each team, for each week
# get it bc boil B)
def boil_soups():
    driver = start_driver()
    team_week_soups = {}
    for team in teams:
        for week in weeks:
            url = create_url(team, week)
            driver.get(url)
            WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, "Table__Scroller")))
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            team_week_soups[(team, week)] = soup

    return team_week_soups