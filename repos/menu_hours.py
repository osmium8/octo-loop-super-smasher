from ..model.models import MenuHours, Timezone
import pytz
import datetime
from ..helpers.date_time_helpers import get_window
from ..extensions import db

def create_menu_hours(store_id, day, start_time, end_time):
    db.session.add(MenuHours(store_id=store_id, day_of_week=day, start_time_local=start_time, end_time_local=end_time))
    db.session.commit()

def get_valid_windows(store_id, day):
    time: MenuHours = MenuHours.query.filter_by(store_id=store_id, day_of_week=day).first()
    timezone: Timezone = Timezone.query.filter_by(store_id=store_id).first()
    utc = pytz.utc
    fmt = '%H:%M'
    timezone_str = pytz.timezone(timezone.timezone)

    dt_start = datetime.datetime.strptime(time.start_time_local, fmt)
    dt_end = datetime.datetime.strptime(time.end_time_local, fmt)

    dt_start_local = timezone_str.localize(dt_start)
    dt_start_end = timezone_str.localize(dt_end)

    dt_start_utc: datetime = dt_start_local.astimezone(utc)
    dt_end_utc: datetime = dt_start_end.astimezone(utc)

    return (get_window(dt_start_utc), get_window(dt_end_utc))