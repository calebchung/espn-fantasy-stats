import re

def create_url(team_id: int = 1, week: int = 1):
    url = ("https://fantasy.espn.com/football/team?leagueId=883531153&"
           "teamId=" + str(team_id) +
           "&seasonId=2024&"
           "scoringPeriodId=" + str(week) + "&statSplit=singleScoringPeriod")
    return url

# TODO: make it so this doesn't break for Sam LaPorta, Trey McBride, et al
# why do all these tight ends have capital letters!!!
def clean_player_name(raw: str) -> str:
    if "/" in raw:
        return re.sub( r"([A-Z])", r" \1", raw).split()[0] + " D/ST"
    first_name = raw.split(" ")[0]
    last_name = re.sub( r"([A-Z])", r" \1", raw.split(" ")[1]).split()
    return first_name + " " + last_name[0]