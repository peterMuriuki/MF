from app.scrapper import get_home_page,parse_table_rows,time_splitter, \
    get_all_other_tips, get_picks_from_tipsters_with_the_best_efficiency, all_other_tips_compiler
from app import create_app, db
from app.models import Predictions, Users