import pandas as pd

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
