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
weeks = range(1, 5)

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
        # if team != 6:
        #     continue 
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

# generate bs4 for draft recap
def boil_draft_soup():
    driver = start_driver()
    url = "https://fantasy.espn.com/football/league/draftrecap?leagueId=883531153"

    driver.get(url)
    WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, "InnerLayout")))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup
    
def scrape_draft_recap():
    soup = boil_draft_soup()
    team_drafts = {key: [] for key in teams}

    draft_round_tables = soup.find_all('table')
    snake_order = False
    draft_round = 1

    for round in draft_round_tables:
        snake_order = not snake_order
        round_df = pd.read_html(StringIO(str(round)))[0]

        team_indexes = teams if snake_order else range(6,0,-1)

        for team_idx in team_indexes:
            team_idx_in_dict = 7 - team_idx if snake_order else team_idx
            row_idx = team_idx - 1
            player_name = round_df.iloc[row_idx, 1]
            if "D/ST" in player_name:
                continue
            team_drafts[team_idx_in_dict].append((player_name, draft_round))
        draft_round += 1
        
    return team_drafts


