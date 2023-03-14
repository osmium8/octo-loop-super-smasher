from ..extensions import db

class Report(db.Model):
    report_id = db.Column(db.String(30), primary_key=True)
    uptime_last_hour = db.Column(db.Integer)
    uptime_last_day = db.Column(db.Integer)
    uptime_last_week = db.Column(db.Integer)
    downtime_last_hour = db.Column(db.Integer)
    downtime_last_day = db.Column(db.Integer)
    downtime_last_week = db.Column(db.Integer)

    def __repr__(self):
        return f'<Report {self.store_id} {self.uptime_last_week} {self.uptime_last_day} {self.uptime_last_hour}>'

class Poll(db.Model):
    store_id = db.Column(db.Integer, primary_key=True)
    week_of_year = db.Column(db.Integer, primary_key=True)
    day_of_week = db.Column(db.Integer, primary_key=True)
    window = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean)

    def __repr__(self):
        return f'<Poll {self.store_id} {self.week_of_year} {self.day_of_week} {self.window} {self.status}>'

class ExtrapolationData(db.Model):
    store_id = db.Column(db.Integer, primary_key=True)
    day_of_week = db.Column(db.Integer, primary_key=True)
    window = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)
    polls = db.Column(db.Integer)

    def __repr__(self):
        return f'<ExtrapolationData {self.store_id} {self.day_of_week} {self.window} {self.value} {self.polls}>'

class MenuHours(db.Model):
    store_id = db.Column(db.Integer, primary_key=True)
    day_of_week = db.Column(db.Integer, primary_key=True)
    start_time_local = db.Column(db.String(30))
    end_time_local = db.Column(db.String(30))

    def __repr__(self):
        return f'<ExtrapolationData {self.store_id} {self.day_of_week} {self.start_time_local} {self.end_time_local}>'

class Timezone(db.Model):
    store_id = db.Column(db.Integer, primary_key=True)
    timezone = db.Column(db.String(30))

    def __repr__(self):
        return f'<ExtrapolationData {self.store_id} {self.timezone}>'

