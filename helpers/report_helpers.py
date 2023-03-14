from ..helpers.date_time_helpers import *
from ..helpers.report_helpers import *
from ..helpers.extrapolation_helpers import *
from ..repos.extrapolation_data import *
from ..repos.polls import *
from ..repos.menu_hours import *
from ..repos.report import *

def generate_report_id(store_id, week, day, window):
    return f'{store_id}_{week}_{day}_{window}'

