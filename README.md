# Sentinel View

A component visualising data gathered by **Sentinel**.

## Python requirements

Python Package Index requirements (including the development ones) are stated in
`setup.py`

## Infrastructure requirements

- TimescaleDB)
- Redis server


## Development usage

- Establish python virtual environment (use
  [wrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) optionally)
  and install `sview` package. Consider using `-e` option: `pip install -e .`
- Create `.env` file with local environment variables (see `.env.example`)
- Set the configuration in `instance/local.cfg`. The default configuration
  can be found in `sview/default_settings.py`.
- Run the application using `flask run` (Use wsgi server for production!)
- Run some workers using `flask rq worker`. (Using only `rq worker` would lack
  any configuration and would end up working outside the application context).


## Data processing

To see up-to-date data, one should execute:

```
flask refresh
```

In production, this command should be executed every minute by cron.

In application context (`dotenv` or `FLASK_APP=sview`).

On production, this should be run via cron.


Data about attackers, passwords and other details are queued on-demand, when a
user attempt to access them via web.

All the data diplayed on web are dated in UTC.

In graphs, the values assigned to each date refers to time period between this
data (excuding) and the same date one period ago (including). See commit message
for more details.

## Database

TimescaleDB is used as the main storage. This section describes it's expected
structure. It's expected structure is described inside
[scheme.sql](sview/scheme.sql).

Generally, it consists of three main tables - one for incidents, one for
passwords and one for port scans.

## Time scales / buckets & aggregation

Using sview, it is possible to display the user data from different time periods.
Each period displays the data with a different precision and a different max age.
Therefore, data with different precision may be used for displaying different
periods.
The following matrix defines the relations between chosen period (Range),
aggregation window, TTL used for caching the result the used bucket and
precision. The following precisions are available:
 - `quarterly`: Incidents summarized by quarters of hour
 - `hourly`: Incidents summarized by hours
 - `daily`: Incidents summarized by days
The table also shows column called Windows Per Range which says how many point there
will be in the graph. The aggregation can be omitted or modified one day if the
plotting technology will be more user friendly.

| Range | Window | WPR   | Cache TTL | Source precision |
| :---: | :---:  | :---: | :--:      | :--:             |
| 1h    | 1m     | 60    | 30s       | native           |
| 12h   | 15m    | 48    | 7m        | quarterly        |
| 1d    | 30m    | 48    | 40m       | quarterly        |
| 1w    | 3h     | 56    | 2h        | hourly           |
| 1mo   | 1d     | ~30   | 12h       | daily            |
| 3mo   | 2d     | ~45   | 1d        | daily            |
| 1y    | 1w     | ~52   | 1d        | daily            |

### Aggregation tasks

Sview is able to maintain different tables with different data precision. To
achieve this, sview runs periodic task to aggregate data and move them between
these tables. Currently, there are 3 main aggregation tasks - each for one
precision, also called *aggregation period*. The mechanism is very similar to
caching resources. It means that every aggregation period (e.g. every hour) a
task is deployed which aggregates the last period (hour) from higher precision
(quarterly) to lower precision (hourly) and moves it to proper table (one of
`*_hourly` tables, e.g. `ports_hourly`).

Like in case of resources, *aggragation timeouts* are used to keep knowledge
whether is is the right time to run an aggregation task. When aggregation
timeout expires the task is triggered.

The need for aggregation is automatically checked with every resource request
and with every `flask refresh` command and the aggregation is triggered when
needed.

## Flask commands

Flask provides user-friendly command line interface. Using this interface a bunch
of semi-useful commands was prepared. Using these commands the user can view
state of jobs, cache and other things. The following commands are implemented:

- `flask aggregate-period <aggregation period name>`
  - Suggest aggregation of the specified period. The specified period is the
    destination period.
- `flask cache-period <resource period name>`
  - Suggest refresh of all cached resources with period
- `flask view-redis-cache`
  - Check state of data in redis. Prints list of cached and missing resource
    keys.
- `flask clear-cache`
  - Clear application cache, not the Redis cache
- `flask clear-redis-cache`
  - Clear Redis cache
- `flask clear-timeouts <aggregation/resource> <period name>`
  - Clear resource refresh or aggregation timeouts from selected period
    The period then can be freely cached or aggregated. Be sure no period is
    aggregated twice or more!!!
- `flask migrate-period <period name>`
  - Aggregates last few days from source period to period requested by
    `period_name`
  - This could be used as a development tools or during initial migration
    from non-aggregated DB. In the later case it would be used in three waves:
    - `flask migrate-period quarterly`
    - `flask migrate-period hourly`
    - `flask migrate-period daily`
    Each command must be executed only when the jobs deployed by the previous
    command are completed
- `flask refresh`
  - Suggest caching of all precached resources. Only missing or outdated
    resources are refreshed.
  - Using dry-run mode you can see what resources would be cached:
    `flask refresh -d`. The would-be run jobs would be marked with
    `Queueing` but new job `id` would be `None`.
- `flask cache-resource <resource name> <resource period> [-d]`
  - Suggest caching of a single resource. Proceed only if the resource is
    missing or outdated.
  - Resource name and period name are required
  - E.g. `flask cache-resource all_attackers_graph 1h`
  - Dry run mode available
- `flask view-jobs`
  - View running, failed, removed or other jobs.
- `flask view-timeouts`
  - View resource refresh timeouts and aggregation timeouts
