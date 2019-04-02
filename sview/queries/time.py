import datetime


def ts_today():
    d = datetime.datetime.utcnow()
    tr = datetime.datetime(d.year, d.month, d.day)
    return int(tr.timestamp())


def ts_this_week():
    d = datetime.datetime.utcnow()
    tr = datetime.datetime(d.year, d.month, d.day)
    tr = tr - datetime.timedelta(days=d.weekday())

    return int(tr.timestamp())


def ts_this_month():
    d = datetime.datetime.utcnow()
    tr = datetime.datetime(d.year, d.month, 1)

    return int(tr.timestamp())


def ts_this_year():
    d = datetime.datetime.utcnow()
    tr = datetime.datetime(d.year, 1, 1)

    return int(tr.timestamp())
