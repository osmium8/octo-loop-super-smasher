from ..extensions import db
from ..model.models import Poll

def create(poll: Poll):
    db.session.add(poll)
    db.session.commit()


def delete(report: Poll):
    db.session.delete(report)
    db.session.commit()


def get_status(store_id, week_of_year, day_of_week, window):
    poll = Poll.query.filter_by(store_id=store_id,
                                week_of_year=week_of_year,
                                day_of_week=day_of_week,
                                window=window).first()
    if poll is not None:
        return poll.status
    else:
        return None


def get_reports_by_day(store_id, week_of_year, day_of_week):
    polls = Poll.query.filter_by(store_id=store_id,
                                 week_of_year=week_of_year,
                                 day_of_week=day_of_week).all()
    window_to_status = dict()
    for poll in polls:
        window_to_status[poll.window] = poll.status
    return window_to_status


def get_reports_by_week(store_id, week_of_year):
    polls: list[Poll] = Poll.query.filter_by(store_id=store_id,
                                 week_of_year=week_of_year).all()
    print('polls', polls)
    day_to_window_to_status = dict()
    for poll in polls:

        if (poll.day_of_week in day_to_window_to_status):
            temp = day_to_window_to_status[poll.day_of_week]
        else:
            temp = dict()

        temp[poll.window] = poll.status
        day_to_window_to_status[poll.day_of_week] = temp
        
    return day_to_window_to_status

