from .queries.time import MINUTE
from .queries.time import MINUTE15
from .queries.time import MINUTE30
from .queries.time import HOUR
from .queries.time import HOUR3
from .queries.time import HOUR12
from .queries.time import DAY
from .queries.time import WEEK
from .queries.time import MONTH
from .queries.time import MONTH3
from .queries.time import YEAR


"""Time periods of displayed data. If you divide period length by length of
flux window, you will get the number of displayed data points. Each period has
defined cache TTL. It seems reasonable for TTL to be half a length of flux
window. Cache TTL is defined in seconds and should be used on both server and
client sides.
"""
PERIOD_HOUR = {
    "handle": "1h",
    "label": "Hour",
    "bucket": "1 minute",
    "cache_ttl": 5 * 60,
    "user_cache_ttl": 2 * 60,
    "refresh_interval": MINUTE,
    "display_interval": HOUR,
    "last_ts_before_function": "ts_last_minute_before",
}
PERIOD_12_HOURS = {
    "handle": "12h",
    "label": "12 Hours",
    "bucket": "15 minutes",
    "cache_ttl": 20 * 60,
    "user_cache_ttl": 5 * 60,
    "refresh_interval": MINUTE15,
    "display_interval": HOUR12,
    "last_ts_before_function": "ts_last_quarter_before",
}
PERIOD_DAY = {
    "handle": "1d",
    "label": "Day",
    "bucket": "30 minutes",
    "cache_ttl": 25 * 60,
    "user_cache_ttl": 5 * 60,
    "refresh_interval": MINUTE30,
    "display_interval": DAY,
    "last_ts_before_function": "ts_last_half_before",
}
PERIOD_WEEK = {
    "handle": "1w",
    "label": "Week",
    "bucket": "3 hours",
    "cache_ttl": 3 * 60 * 60 + 10 * 60,
    "user_cache_ttl": 5 * 60,
    "refresh_interval": HOUR3,
    "display_interval": WEEK,
    "last_ts_before_function": "ts_last_3hour_before",
}
PERIOD_MONTH = {
    "handle": "1m",
    "label": "Month",
    "bucket": "1 day",
    "cache_ttl": 25 * 60 * 60,
    "user_cache_ttl": 5 * 60,
    "refresh_interval": DAY,
    "display_interval": MONTH,
    "last_ts_before_function": "ts_last_midnight_before",
}
PERIOD_3_MONTHS = {
    "handle": "3m",
    "label": "3 Months",
    "bucket": "2 days",
    "cache_ttl": 25 * 60 * 60,
    "user_cache_ttl": 5 * 60,
    "refresh_interval": DAY,
    "display_interval": MONTH3,
    "last_ts_before_function": "ts_last_midnight_before",
}
PERIOD_YEAR = {
    "handle": "1y",
    "label": "Year",
    "bucket": "14 days",
    "cache_ttl": 25 * 60 * 60,
    "user_cache_ttl": 5 * 60,
    "refresh_interval": DAY,
    "display_interval": YEAR,
    "last_ts_before_function": "ts_last_midnight_before",
}


DEFAULT_PERIOD = "1y"
PERIODS = {
    "1h": PERIOD_HOUR,
    "12h": PERIOD_12_HOURS,
    "1d": PERIOD_DAY,
    "1w": PERIOD_WEEK,
    "1m": PERIOD_MONTH,
    "3m": PERIOD_3_MONTHS,
    "1y": PERIOD_YEAR,
}