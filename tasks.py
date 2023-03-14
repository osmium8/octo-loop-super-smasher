from datetime import timedelta
from .model.models import Report
from .helpers.date_time_helpers import *
from .helpers.report_helpers import *
from .helpers.extrapolation_helpers import *
from .repos.extrapolation_data import *
from .repos.polls import *
from .repos.menu_hours import *

def get_last_hour(store_id, timestamp):
    window = get_window(timestamp)
    week = get_week_of_year(timestamp)
    day = get_day(timestamp)

    if (window == 0):
        window = 23
        day = decrement_day(day)
        if (day == 6):
            week = get_week_of_year(timestamp - timedelta(days=1))
    else:
        window = window - 1

    status = get_status(store_id, week, day, window)

    uptime_minutes = 0

    if (status is not None):
        if (status):
            uptime_minutes = 60
        else:
            uptime_minutes = 60
    else:
        uptime_minutes = get_extrapolated_minutes(
            get_status_ex_data(store_id, day, window))

    downtime_minutes = 60 - uptime_minutes

    return (uptime_minutes, downtime_minutes)


def get_last_day(store_id, timestamp):
    day = get_day(timestamp)
    week = get_week_of_year(timestamp)

    if (day == 0):
        day = 6
        week = get_week_of_year(timestamp - timedelta(days=1))
    else:
        day = day - 1

    last_day = day

    db = get_reports_by_day(store_id, week, last_day)
    minutes = 0

    window_tuple = get_valid_windows(store_id, day)
    # print('last day', get_valid_windows(store_id, day))
    for window in range(window_tuple[0], window_tuple[1]):
        if (window in db):
            if (db[window]):
                minutes += 60.0
            else:
                minutes += 0.0
        else:
            minutes += get_extrapolated_minutes(
                get_status_ex_data(store_id, day, window))

    max_avaialble_hours = (window_tuple[1] - window_tuple[0])
    uptime_hours = minutes / 60
    downtime_hours = max_avaialble_hours - uptime_hours
    return (uptime_hours, downtime_hours)


def get_last_week(store_id, timestamp):
    week = get_week_of_year(timestamp)

    if (week == 0):
        week = get_week_of_year(timestamp - timedelta(days=1))
    else:
        week = week - 1

    last_week = week
    db = get_reports_by_week(store_id, last_week)
    print('db', db)

    minutes = 0
    max_avialable_hours = 0

    for day in [0, 1, 2, 3, 4, 5, 6]:
        window_tuple = get_valid_windows(store_id, day)
        max_avialable_hours += (window_tuple[1] - window_tuple[0])
        if (day in db):
            # print('window_tuple', window_tuple)
            for window in range(window_tuple[0], window_tuple[1]):
                if (window in db[day]):
                    print('debug', db[day][window])
                    if (db[day][window]):
                        minutes += 60.0
                    else:
                        minutes += 0.0
                else:
                    minutes += get_extrapolated_minutes(
                        get_status_ex_data(store_id, day, window))
        else:
            for window in range(window_tuple[0], window_tuple[1]):
                minutes += get_extrapolated_minutes(
                    get_status_ex_data(store_id, day, window))

    uptime_hours = minutes/60
    downtime_hours = max_avialable_hours - uptime_hours
    return (uptime_hours, downtime_hours)


def generate_report(report_id, store_id, current_time):
    '''
    this function(job) will be queued and RQ (Redis Queue) will be processing this
    in the background with workers
    '''
    a = get_last_hour(store_id, current_time)
    b = get_last_day(store_id, current_time)
    c = get_last_week(store_id, current_time)
    db.session.add(Report(report_id=report_id, uptime_last_hour=a[0],
                   uptime_last_day=b[0], uptime_last_week=c[0],
                   downtime_last_hour=a[1], downtime_last_day=b[1], downtime_last_week=c[1]))
    db.session.commit()
