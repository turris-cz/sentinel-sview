# Sentinel:View

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
flask queue-queries
```

In application context (`dotenv` or `FLASK_APP=sview`).

On production, this should be run via cron.


Data about attackers, passwords and other details are queued on-demand, when a
user attempt to access them via web.

## Database

TimescaleDB is used as the main storage. This section describes it's expected
structure. It's expected structure is described inside
[scheme.sql](sview/scheme.sql).

Generally, it consists of three main tables - one for incidents, one for
passwords and one for port scans.

## Time scales / buckets

Using sview, it is possible to display the user data from different time periods.
Each period displays the data with a different precision and a different max age.
The following matrix defines the relations between chosen period (Range),
aggregation window, TTL used for caching the result and the used bucket. It also
shows column called Windows Per Range which says how many point there will be in
the graph. The aggregation can be omitted or modified one day if the plotting
technology will be more user friendly.

| Range | Window | WPR   | Cache TTL |
| :---: | :---:  | :---: | :--:      |
| 1h    | 1m     | 60    | 30s       |
| 12h   | 15m    | 48    | 7m        |
| 1d    | 30m    | 48    | 40m       |
| 1w    | 3h     | 56    | 2h        |
| 1mo   | 1d     | ~30   | 12h       |
| 3mo   | 2d     | ~45   | 1d        |
| 1y    | 1w     | ~52   | 1d        |
