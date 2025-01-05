import pandas as pd
from libs.utils import clean_player_name 

def total_underperforming(df_dict: dict[int, dict[int, pd.DataFrame]]):
    for team_idx in df_dict.keys():
        team_diff = 0
        for week_idx in df_dict[team_idx].keys():
            week_df = df_dict[team_idx][week_idx]
            proj = week_df.iloc[9, 2]
            actual = week_df.iloc[9, 3]
            diff = round(float(actual) - float(proj), 2)
            team_diff += round(float(actual) - float(proj), 2)
            print("Team {} week {} actual vs projected: {}".format(team_idx, week_idx, diff))

        print("Total team diff: {}".format(round(team_diff, 2)))

# TODO: might be avoidably skipping some names too lazy to figure out rn 
def total_draft_value(df_dict: dict[int, dict[int, pd.DataFrame]], draft_dict: dict[tuple[str, int]]):
    player_rankings = get_player_rankings(df_dict)
    for team_idx in draft_dict.keys():
        # get draft position sum
        team_draft = draft_dict[team_idx]
        team_draft_value = 0
        highest_value = -1
        highest_value_pick = ""

        for player, pos in team_draft:
            ranking = player_rankings.get(clean_player_name(player))
            if not ranking:
                continue
            value = pos - float(ranking)
            if value > highest_value:
                highest_value = value
                highest_value_pick = player
            team_draft_value += value
            print(player + "'s draft value: " + str(value))

        print("Team " + str(team_idx) + "'s total draft value: " + str(team_draft_value))
        print("Best Overall Pick: " + highest_value_pick)
        print("")

def get_player_rankings(df_dict: dict[int, dict[int, pd.DataFrame]]):
    player_rankings = {}
    for team_idx in df_dict.keys():
        week_df = df_dict[team_idx][1]
        player_rows = list(range(0,7)) + [8] + list(range(10,17))
        for player_idx in player_rows:
            raw_name = week_df.iloc[player_idx,1]
            if raw_name == 'Empty':
                continue
            name = raw_name
            rank = week_df.iloc[player_idx,8]
            player_rankings[name] = rank
    return player_rankings