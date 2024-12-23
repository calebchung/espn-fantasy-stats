import re

def clean_player_name(raw: str) -> str:
    if "/" in raw:
        return re.sub( r"([A-Z])", r" \1", raw).split()[0] + " D/ST"
    first_name = raw.split(" ")[0]
    last_name = re.sub( r"([A-Z])", r" \1", raw.split(" ")[1]).split()
    return first_name + " " + last_name[0]