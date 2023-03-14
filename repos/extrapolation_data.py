from ..extensions import db
from ..model.models import ExtrapolationData


def createData(data: ExtrapolationData):
    db.session.add(data)
    db.session.commit()


def get_status_ex_data(store_id, day_of_week, window):
    poll: ExtrapolationData = ExtrapolationData.query.filter_by(store_id=store_id,
                                                                day_of_week=day_of_week,
                                                                window=window).first()
    if poll is not None:
        return (poll.value, poll.polls)
    else:
        return (0, 0)


def update_ex_data(store_id, day_of_week, window, value, polls):
    data = ExtrapolationData.query.filter_by(
        store_id=store_id, day_of_week=day_of_week, window=window).first()
    data.value = value
    data.polls = polls
    print(f'data for {day_of_week}_{window}', data)
    db.session.flush()
    db.session.commit()
