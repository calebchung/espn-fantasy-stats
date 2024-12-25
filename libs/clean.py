import pandas as pd
import numpy as np

def clean(df_dict):
    for team_weeks in df_dict.values():
        for week_df in team_weeks.values():
            new_columns = []
            for col in week_df.columns:
                new_columns.append(col[1])
            week_df.columns = new_columns
            week_df.drop('opp', axis=1, inplace=True)
            week_df.drop('STATUS', axis=1, inplace=True)
            week_df.drop('LAST', axis=1, inplace=True)
            week_df.fillna(0, inplace=True)
    return df_dict