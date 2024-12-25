from libs.utils import clean_player_name

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
            week_df.replace({'--': 0}, regex=True, inplace=True)
            week_df['Player'] = week_df['Player'].apply(lambda raw_name: clean_if_name(raw_name))
    return df_dict

def clean_if_name(name_or_int):
    if isinstance(name_or_int, str) and " " in name_or_int:
        return clean_player_name(name_or_int)
    return name_or_int