from .time import MINUTE
from .time import MINUTE15
from .time import MINUTE30
from .time import HOUR
from .time import HOUR3
from .time import HOUR6
from .time import DAY
from .time import WEEK
from .time import MONTH
from .time import MONTH3
from .time import YEAR


class PriorityQueue:
    AGGREGATION = "aggregation"
    QUICK_CACHE = "quick-cache"
    SLOW_CACHE = "slow-cache"


"""Time periods for data aggregation
"""
#  Not a real aggregation period. It just marks data with no aggregation
NATIVE_PERIOD = {
    "handle": "",
    "source_period": None,
}
QUARTERLY_PERIOD = {
    "handle": "quarterly",
    "source_period": NATIVE_PERIOD,
    "queue": PriorityQueue.AGGREGATION,
    "bucket": "15 minutes",
    "start_delay_bonus": 3 * 60,  # seconds
    "refresh_interval": MINUTE15,
    "display_interval": MINUTE15,
    "last_ts_before_function": "ts_last_quarter_before",
    "index": 1,
}
HOURLY_PERIOD = {
    "handle": "hourly",
    "source_period": QUARTERLY_PERIOD,
    "queue": PriorityQueue.AGGREGATION,
    "bucket": "1 hour",
    "start_delay_bonus": 10,  # seconds
    "refresh_interval": HOUR,
    "display_interval": HOUR,
    "last_ts_before_function": "ts_last_hour_before",
    "index": 2,
}
DAILY_PERIOD = {
    "handle": "daily",
    "source_period": HOURLY_PERIOD,
    "queue": PriorityQueue.AGGREGATION,
    "bucket": "1 day",
    "start_delay_bonus": 10,  # seconds
    "refresh_interval": DAY,
    "display_interval": DAY,
    "last_ts_before_function": "ts_last_midnight_before",
    "index": 3,
}

AGGREGATION_PERIODS = {
    "quarterly": QUARTERLY_PERIOD,
    "hourly": HOURLY_PERIOD,
    "daily": DAILY_PERIOD,
}


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
    "start_delay_bonus": 0,  # seconds
    "cache_ttl": 5 * 60,
    "user_cache_ttl": 30,  # should not be high - user could keep outdated data
    "source_period": NATIVE_PERIOD,
    "queue": PriorityQueue.QUICK_CACHE,
    "refresh_interval": MINUTE,
    "display_interval": HOUR,
    "last_ts_before_function": "ts_last_minute_before",
    "index": 1,
}
PERIOD_6_HOURS = {
    "handle": "6h",
    "label": "6 Hours",
    "bucket": "15 minutes",
    "start_delay_bonus": 5,  # seconds
    "cache_ttl": 25 * 60,
    "user_cache_ttl": 2 * 60,
    "source_period": QUARTERLY_PERIOD,
    "queue": PriorityQueue.QUICK_CACHE,
    "refresh_interval": MINUTE15,
    "display_interval": HOUR6,
    "last_ts_before_function": "ts_last_quarter_before",
    "index": 2,
}
PERIOD_DAY = {
    "handle": "1d",
    "label": "Day",
    "bucket": "30 minutes",
    "start_delay_bonus": 5,  # seconds
    "cache_ttl": 50 * 60,
    "user_cache_ttl": 5 * 60,
    "source_period": QUARTERLY_PERIOD,
    "queue": PriorityQueue.QUICK_CACHE,
    "refresh_interval": MINUTE30,
    "display_interval": DAY,
    "last_ts_before_function": "ts_last_half_before",
    "index": 3,
}
PERIOD_WEEK = {
    "handle": "1w",
    "label": "Week",
    "bucket": "3 hours",
    "start_delay_bonus": 5,  # seconds
    "cache_ttl": 4 * 60 * 60,
    "user_cache_ttl": 5 * 60,
    "source_period": HOURLY_PERIOD,
    "queue": PriorityQueue.SLOW_CACHE,
    "refresh_interval": HOUR3,
    "display_interval": WEEK,
    "last_ts_before_function": "ts_last_3hour_before",
    "index": 4,
}
PERIOD_MONTH = {
    "handle": "1m",
    "label": "Month",
    "bucket": "1 day",
    "start_delay_bonus": 5,  # seconds
    "cache_ttl": 25 * 60 * 60,
    "user_cache_ttl": 5 * 60,
    "source_period": DAILY_PERIOD,
    "queue": PriorityQueue.SLOW_CACHE,
    "refresh_interval": DAY,
    "display_interval": MONTH,
    "last_ts_before_function": "ts_last_midnight_before",
    "index": 5,
}
PERIOD_3_MONTHS = {
    "handle": "3m",
    "label": "3 Months",
    "bucket": "2 days",
    "start_delay_bonus": 5,  # seconds
    "cache_ttl": 25 * 60 * 60,
    "user_cache_ttl": 5 * 60,
    "source_period": DAILY_PERIOD,
    "queue": PriorityQueue.SLOW_CACHE,
    "refresh_interval": DAY,
    "display_interval": MONTH3,
    "last_ts_before_function": "ts_last_midnight_before",
    "index": 6,
}
PERIOD_YEAR = {
    "handle": "1y",
    "label": "Year",
    "bucket": "14 days",
    "start_delay_bonus": 5,  # seconds
    "cache_ttl": 25 * 60 * 60,
    "user_cache_ttl": 5 * 60,
    "source_period": DAILY_PERIOD,
    "queue": PriorityQueue.SLOW_CACHE,
    "refresh_interval": DAY,
    "display_interval": YEAR,
    "last_ts_before_function": "ts_last_midnight_before",
    "index": 7,
}


DEFAULT_PERIOD = "1w"

PERIODS = {
    "1h": PERIOD_HOUR,
    "6h": PERIOD_6_HOURS,
    "1d": PERIOD_DAY,
    "1w": PERIOD_WEEK,
    "1m": PERIOD_MONTH,
    "3m": PERIOD_3_MONTHS,
    "1y": PERIOD_YEAR,
}
