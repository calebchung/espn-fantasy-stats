from libs.process import total_underperforming
from libs.process import total_draft_value
from libs.scrape import scrape_draft_recap
from libs.scrape import scrape
from libs.clean import clean

df_dict = scrape()
# total_underperforming(clean(df_dict))

draft_dict = scrape_draft_recap()
total_draft_value(clean(df_dict), draft_dict)