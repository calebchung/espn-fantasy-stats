from libs.scrape import boil_soups, scrape
from libs.clean import clean, players_only, bench_only
from libs.utils import clean_player_name

def total_underperforming():
    team_soups = boil_soups()
    for week_list in team_soups.values():
        for week_soup in week_list.values():
            total_diff_for_week = 0
            for row in week_soup.find_all("tr", class_="Table__TR Table__TR--lg Table__odd")[:-9]: # exclude bench
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

# total_underperforming()
df_dict = scrape()
print(bench_only(clean(df_dict)[1][1]))