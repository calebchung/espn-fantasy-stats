from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

from libs.utils import clean_player_name

# teams and weeks are 1-indexed
teams = range(1, 7)
weeks = range(1, 2)

def start_driver():
    options = webdriver.ChromeOptions()
    options.add_argument(argument="--headless")
    driver = webdriver.Chrome(options=options)
    return driver

def create_url(team_id: int = 1, week: int = 1):
    url = ("https://fantasy.espn.com/football/team?leagueId=883531153&"
           "teamId=" + str(team_id) +
           "&seasonId=2024&"
           "scoringPeriodId=" + str(week) + "&statSplit=singleScoringPeriod")
    return url

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

def total_underperforming():
    team_week_soups = boil_soups()
    for soup in team_week_soups.values():
        total_diff_for_week = 0
        for row in soup.find_all("tr", class_="Table__TR Table__TR--lg Table__odd")[:-9]: # exclude bench
            cols = row.find_all("td")
            if cols[1].get_text() == "":
                continue
            name = clean_player_name(cols[1].get_text())
            projected = float(cols[4].get_text())
            if cols[5].get_text() == "--": # did not play
                actual = 0
            else:
                actual = float(cols[5].get_text())
            diff = round(actual - projected, 2)
            print(name + " " + str(diff))
            total_diff_for_week += diff

        print("Week 1 diff vs projection: " + str(round(total_diff_for_week, 2)))

total_underperforming()