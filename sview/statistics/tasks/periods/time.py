import datetime

MINUTE = datetime.timedelta(minutes=1)
MINUTE15 = datetime.timedelta(minutes=15)
MINUTE30 = datetime.timedelta(minutes=30)
HOUR = datetime.timedelta(hours=1)
HOUR3 = datetime.timedelta(hours=3)
HOUR6 = datetime.timedelta(hours=6)
DAY = datetime.timedelta(days=1)
WEEK = datetime.timedelta(days=7)
MONTH = datetime.timedelta(days=30)
MONTH3 = datetime.timedelta(days=90)
YEAR = datetime.timedelta(days=378)  # 27 * 14 days


def utc_now_ts():
    return int(datetime.datetime.now(datetime.timezone.utc).timestamp())


def ts_last_midnight_before(before=datetime.timedelta()):
    dt = datetime.datetime.now(datetime.timezone.utc) - before
    tr = datetime.datetime(dt.year, dt.month, dt.day, tzinfo=datetime.timezone.utc)
    return int(tr.timestamp())


def ts_last_3hour_before(before=datetime.timedelta()):
    dt = datetime.datetime.now(datetime.timezone.utc) - before
    hour = dt.hour - dt.hour % 3
    tr = datetime.datetime(
        dt.year, dt.month, dt.day, hour, tzinfo=datetime.timezone.utc
    )
    return int(tr.timestamp())


def ts_last_hour_before(before=datetime.timedelta()):
    dt = datetime.datetime.now(datetime.timezone.utc) - before
    tr = datetime.datetime(
        dt.year, dt.month, dt.day, dt.hour, tzinfo=datetime.timezone.utc
    )
    return int(tr.timestamp())


def ts_last_half_before(before=datetime.timedelta()):
    dt = datetime.datetime.now(datetime.timezone.utc) - before
    minute = dt.minute - dt.minute % 30
    tr = datetime.datetime(
        dt.year, dt.month, dt.day, dt.hour, minute, tzinfo=datetime.timezone.utc
    )
    return int(tr.timestamp())


def ts_last_quarter_before(before=datetime.timedelta()):
    dt = datetime.datetime.now(datetime.timezone.utc) - before
    minute = dt.minute - dt.minute % 15
    tr = datetime.datetime(
        dt.year, dt.month, dt.day, dt.hour, minute, tzinfo=datetime.timezone.utc
    )
    return int(tr.timestamp())


def ts_last_minute_before(before=datetime.timedelta()):
    dt = datetime.datetime.now(datetime.timezone.utc) - before
    tr = datetime.datetime(
        dt.year, dt.month, dt.day, dt.hour, dt.minute, tzinfo=datetime.timezone.utc
    )
    return int(tr.timestamp())


LAST_TS_BEFORE_FUNCTIONS = {
    "ts_last_midnight_before": ts_last_midnight_before,
    "ts_last_3hour_before": ts_last_3hour_before,
    "ts_last_hour_before": ts_last_hour_before,
    "ts_last_half_before": ts_last_half_before,
    "ts_last_quarter_before": ts_last_quarter_before,
    "ts_last_minute_before": ts_last_minute_before,
}
