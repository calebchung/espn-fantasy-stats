from libs.process import total_underperforming
from libs.scrape import scrape
from libs.clean import clean

df_dict = scrape()
total_underperforming(clean(df_dict))
