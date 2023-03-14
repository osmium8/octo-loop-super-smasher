def get_day(timestamp):
    return timestamp.weekday()

def get_week_of_year(timestamp):
    return timestamp.isocalendar().week

def get_window(timestamp):
    return timestamp.time().hour

def decrement_day(day):
    if (day == 0):
        return 6
    else:
        return day - 1