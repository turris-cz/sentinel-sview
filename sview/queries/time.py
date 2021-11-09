import datetime

HOUR = datetime.timedelta(hours=1)
HOUR12 = datetime.timedelta(hours=12)
DAY = datetime.timedelta(days=1)
WEEK = datetime.timedelta(days=7)
MONTH = datetime.timedelta(days=30)
MONTH3 = datetime.timedelta(days=90)
YEAR = datetime.timedelta(days=378)  # 27 * 14 days


def construct_last_before(function, before=datetime.timedelta()):
    return lambda: function(before)


def ts_last_midnight_before(before):
    dt = datetime.datetime.now(datetime.timezone.utc) - before
    tr = datetime.datetime(dt.year, dt.month, dt.day, tzinfo=datetime.timezone.utc)
    return int(tr.timestamp())


def ts_last_3hour_before(before):
    dt = datetime.datetime.now(datetime.timezone.utc) - before
    hour = dt.hour - dt.hour % 3
    tr = datetime.datetime(
        dt.year, dt.month, dt.day, hour, tzinfo=datetime.timezone.utc
    )
    return int(tr.timestamp())


def ts_last_half_before(before):
    dt = datetime.datetime.now(datetime.timezone.utc) - before
    minute = dt.minute - dt.minute % 30
    tr = datetime.datetime(
        dt.year, dt.month, dt.day, dt.hour, minute, tzinfo=datetime.timezone.utc
    )
    return int(tr.timestamp())


def ts_last_quarter_before(before):
    dt = datetime.datetime.now(datetime.timezone.utc) - before
    minute = dt.minute - dt.minute % 15
    tr = datetime.datetime(
        dt.year, dt.month, dt.day, dt.hour, minute, tzinfo=datetime.timezone.utc
    )
    return int(tr.timestamp())


def ts_last_minute_before(before):
    dt = datetime.datetime.now(datetime.timezone.utc) - before
    tr = datetime.datetime(
        dt.year, dt.month, dt.day, dt.hour, dt.minute, tzinfo=datetime.timezone.utc
    )
    return int(tr.timestamp())
