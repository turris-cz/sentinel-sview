# Sentinel View

A component visualising reports gathered by **Sentinel**. It consists of several
smaller components, or blueprints, like
 - *statistics*: for statistics of raw reports sent by all the Sentinel probes
 - *greylist*: for current greylist data in CSV


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
- Run some workers with all queues using `flask rq worker aggregation
  quick-cache slow-cache`. (Using only `rq worker` would lack
  any configuration and would end up working outside the application context).


## Statistics component

Statistics component - or *blueprint* - aggregates, caches and visualizes
reports sent by Sentinel probes in raw form. It gives the users the opportunity
to see the exact data the network sends and also the exact data they own probe
sends. The data are shown in several time scales - or *periods*.

### Database

TimescaleDB is used as the main storage for Sentinel statistics. This section
describes it's expected structure. It's expected structure is described inside
[scheme.sql](sview/scheme.sql).

Generally, it consists of three main tables - one for incidents, one for
passwords and one for port scans. These tables are used to store raw reports as
they are only roughly processed by the Sentinel pipelines and stored by
[dumper](https://gitlab.nic.cz/turris/sentinel/dumper).

Due to aggregation (more about aggregation later in this document),
the mentioned tables are also present in their aggregated form with aggregated
data. The aggregation is carried out by Sview statistics itself.

For caching, Redis DB is used. It used to keep precached data for the most
queried resources and for all the recently queried resources. No resource
data could be provided to the user without being previously cached in redis.

Therefore, a resource caching task is suggested to run whenever a resource is
needed. During such a suggestion, resource refresh timeout is checked. When it's
pending, the resource is up to date or already being refreshed and no caching
task is deployed. Meanwhile, the user is served data from the cache.

### Time scales / buckets & aggregation

Using sview statistics, it is possible to display the user data from different
time periods. Each period displays the data with a different precision and a
different max age. Therefore, data with different precision may be used for
displaying different periods.
The following matrix defines the relations between chosen period,
aggregation window, TTL used for caching the result the used bucket and
precision. The following precisions are available:
 - `quarterly`: Incidents summarized by quarters of hour
 - `hourly`: Incidents summarized by hours
 - `daily`: Incidents summarized by days
The table also shows column called Windows Per Range which says how many point there
will be in the graph. The aggregation can be omitted or modified one day if the
plotting technology will be more user friendly.

| Period | Range    | Window  | WPR   | Cache TTL | Source precision |
| :---:  | :---:    | :---:   | :---: | :--:      | :--:             |
| `1h`   | 1 hour   | 1 min   | 60    | 5 mins    | native           |
| `12h`  | 12 hours | 15 mins | 48    | 25 mins   | quarterly        |
| `1d`   | 1 day    | 30 mins | 48    | 50 mins   | quarterly        |
| `1w`   | 1 week   | 3 hours | 56    | 4 hours   | hourly           |
| `1m`   | 1 month  | 1 day   | ~30   | 25 hours  | daily            |
| `3m`   | 3 months | 2 days  | ~45   | 25 hours  | daily            |
| `1y`   | 1 year   | 2 weeks | ~26   | 25 hours  | daily            |

For more details (and possibly more up-to-date values), see the
[source file](sview/statistics/tasks/periods/__init__.py).

### Aggregation tasks

Sview statistics is able to maintain different tables with different data
precision. To achieve this, sview runs periodic task to aggregate data and move
them between these tables.
Currently, there are 3 main aggregation tasks - each for one precision, also
called *aggregation period*. The mechanism is very similar to caching resources.
It means that every aggregation period (e.g. every hour) a task is deployed
which aggregates the last period (hour) from higher precision (quarterly) to
lower precision (hourly) and moves it to proper table (one of `*_hourly` tables,
e.g. `ports_hourly`).

Like in case of resources, *aggragation timeouts* are used to keep knowledge
whether is is the right time to run an aggregation task. When aggregation
timeout expires the task is triggered.

The need for aggregation is automatically checked with every resource request
and with every `flask refresh` command and the aggregation is triggered when
needed.

### Production notes

There are 3 different job queues (from highest to lowest priority):
  - `aggregation`: for aggregation tasks, which are usually quick and take
     around minute
  - `quick-cache`: for quick caching tasks, which are quick and should take up
     to ~5 minutes (never more than 10 minutes!!) (so theres space for
     aggregation tasks to take place before them)
  - `slow-cache`: for slow caching tasks which may take to much time (more than
     ~5 minutes and definitely more than quarter of hour) and there's probability
     they would block quarterly aggregation tasks

The optimal number of workers is 6 for `aggregation` and `quick-cache`, run like

```
flask rq worker aggregation quick-cache
```

and 6 workers for `slow-cache`, run like:

```
flask rq worker slow-cache
```

### Data processing

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

## Have i been pawned backend implementation.

### Workflow

1. Recieves request in form of json posted to `http://page.xyz/api/leaked`
2. Selects hashes in database that starts with request hash.
3. Return matching hashes with counts.

step 3. is heavily influenced by how the schema is planned.

## Request/response json schema

Refer to [schema](schema/passy.json)

## Table schema

The schema for `passwords` is as follows

| id        | password_hash | count      | password_source |
| --------- | ------------- | ---------- | --------------- |
| BIGSERIAL | TEXT          | BIGINT     | ARRAY(ENUM)     |

```sql
------ common passwords database scheme
--

CREATE TYPE data_source AS ENUM ('telnet', 'smtp', 'ftp', 'http', 'haas');
CREATE TABLE IF NOT EXISTS passwords(
    id BIGSERIAL PRIMARY KEY,
    password_hash TEXT NOT NULL,
    count BIGINT CHECK (count > 0),
    password_source data_source[]
);
```

# Development (local test)

- create virtual environment
- install ``pip install -e .``
- install `pip install pytest psycopg2`
- create postgres database
    - install in system
    - Docker image (that's actually pretty flawless)
- setup the database
- use [config_example.py](config_example.py) as template for setting database credentials for application
- follow procedure to populate the database with testing data in `/data/README.md` 
- run
```sh
export FLASK_ENV=development
export FLASK_APP=src/passy
```
