from flask import Blueprint, request
from datetime import datetime
from ..repos.polls import *
from ..repos.extrapolation_data import *
from ..repos.menu_hours import *
from ..model.models import ExtrapolationData
from ..helpers.date_time_helpers import *

poll = Blueprint('poll', __name__)

@poll.route('/create_demo', methods=['POST'])
def create_demo():
    for window in [2, 3]:
        create(Poll(store_id=1, week_of_year=10, day_of_week=6, window=window, status=True))
    return {'status': 'DONE'}

@poll.route('/create_menu_hours', methods=['POST'])
def create_menu_hours_route():
    for day in [0, 1, 2, 3, 4, 5, 6]:
        create_menu_hours(1, day, '10:00', '23:00')
    return {'status': 'DONE'}

@poll.route('/create_demo_ex_data', methods=['POST'])
def create_demo_ex_data():
    for store_id in [1]:
        for day in [0, 1, 2, 3, 4, 5, 6]:
            for window in range(1, 24):
                createData(ExtrapolationData(store_id=store_id, day_of_week=day, window=window, value=3, polls=4))
    return {'status': 'DONE'}

@poll.route('/poll', methods=['POST'])
def poll_route():
    store_id: str = request.args['store_id']
    status: str = request.args['status']
    time_utc_str: str = request.args['time_utc']
    time_utc_object: datetime = datetime.datetime.strptime(time_utc_str, '%m/%d/%y %H:%M:%S')

    day: int = get_day(time_utc_object)
    window: int = get_window(time_utc_object)
    week: int = get_week_of_year(time_utc_object)

    # update polls db table
    try:
        create(Poll(store_id=store_id, week_of_year=week, day_of_week=day, window=window, status=bool(status)))
        
        # update extrapolation data db table
        value_polls_tuple: tuple = get_status_ex_data(store_id,day,window)
        if (bool(status) is True):
            value: int = value_polls_tuple[0] + 1
        else:
            value: int = value_polls_tuple[0] - 1
            value = max(0, value)

        polls: int = value_polls_tuple[1] + 1
        update_ex_data(store_id, day, window, value, polls)
    except:
        return {"status": "already created"}, 409

    return {"status": "created"}, 201