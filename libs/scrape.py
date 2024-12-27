from io import StringIO

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from libs.utils import create_url

import pandas as pd

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
    per_team = {}
    for team in teams:
        week_soups = {}
        for week in weeks:
            url = create_url(team, week)
            driver.get(url)
            WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, "Table__Scroller")))
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            week_soups[week] = soup
        per_team[team] = week_soups

    return per_team

def scrape():
    team_soups = boil_soups()
    team_dfs = {}
    for week_idx in team_soups.keys():
        week_dfs = {}
        for week_soup_idx in team_soups[week_idx]:
            week_table = team_soups[week_idx][week_soup_idx].find_all('table')
            week_df = pd.read_html(StringIO(str(week_table)))[0]
            week_dfs[week_soup_idx] = week_df

        team_dfs[week_idx] = week_dfs
    return team_dfs
