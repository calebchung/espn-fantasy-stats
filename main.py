from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

from utils import clean_player_name

base_url = "https://fantasy.espn.com/football/team?leagueId=883531153&teamId=1&seasonId=2024&scoringPeriodId=1&statSplit=singleScoringPeriod"
options = webdriver.ChromeOptions()
options.add_argument(argument="--headless")
driver = webdriver.Chrome(options=options)
driver.get(base_url)

def total_underperforming(driver):
    WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, "Table__Scroller")))
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    for row in soup.find_all("tr", class_="Table__TR Table__TR--lg Table__odd")[:-2]:
        try:
            cols = row.find_all("td")
            raw_name = cols[1].get_text()
            if raw_name != "":
                print(clean_player_name(raw_name))
        except AttributeError:
            continue




total_underperforming(driver)