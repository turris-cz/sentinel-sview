# Sentinel:View

A component visualising data gathered by **Sentinel**.

## Python requirements

Python Package Index requirements (including the development ones) are stated in
`setup.py`

## Infrastructure requirements

- InfluxDB
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

## InfluxDB

InfluxDB is used as the main storage. This section describes it's expected
structure.

### InfluxDB measurements

InfluxDB is expected to provide at least the following measurements:

#### (General) Incident count

| `_measurement`     | `_field` = source  | `_value` | tag: `action` |
| :---:              | :---:              | :---:    | :---:         |
| `"incident_count"` | `"minipot_telnet"` | `1`      | `"connect"`   |
| `"incident_count"` | `"minipot_ftp"`    | `1`      | `"connect"`   |
| `"incident_count"` | `"minipot_smtp"`   | `1`      | `"login"`     |

#### Attacker incident count

| `_measurement`              | `_field` = src_addr | `_value` | tag: `country` |
| :---:                       | :---:               | :---:    | :---:          |
| `"attacker_incident_count"` | `"192.0.2.10"`      | `1`      | "CZ"           |
| `"attacker_incident_count"` | `"192.0.2.245"`     | `1`      | "GB"           |
| `"attacker_incident_count"` | `"192.0.2.89"`      | `1`      | "US"           |

#### User incident count

| `_measurement`          | `_field` = device_token | `_value` | tag: `country` | tag: `source`   |
| :---:                   | :---:                   | :---:    | :---:          | :---:           |
| `"user_incident_count"` | `"a"*64`                | `1`      | `"CZ"`         | `"minipot_ftp"` |
| `"user_incident_count"` | `"bf45..78ad`           | `1`      | `"SK"`         | `"minipot_http"` |
| `"user_incident_count"` | `"dead..beef`           | `1`      | `"MN"`         | `"minipot_http"` |

#### Password count

| `_measurement`     | `_field` = password | `_value` | tag: `username` |
| :---:              | :---:               | :---:    | :---:           |
| `"password_count"` | `"heslo"`           | `1`      | `"jmeno"`       |
| `"password_count"` | `"p4ssw0rd"`        | `1`      | `"usern4me"`    |
| `"password_count"` | `"secretpass"`      | `1`      | `"vojta"`       |

#### Port count

| `_measurement` | `_field` = port | `_value` | tag: `protocol` |
| :---:          | :---:           | :---:    | :---:           |
| `"port_count"` | `"8888"`        | `1`      | `"TCP"`         |
| `"port_count"` | `"53"`          | `1`      | `"UDP"`         |
| `"port_count"` | `"443"`         | `1`      | `"TCP"`         |

### Buckets

The listed measurements are stored in few different buckets which ensure right
retention policy. All the buckets must be present in InfluxDB prior to sview
deployment and should be filled with meaningful data. Currently, the following
buckets are expected:

| Name                | Retention |
| :---:               | :---:     |
| `sentinel-base`     | 2h        |
| `sentinel-minutely` | 2d        |
| `sentinel-hourly`   | 4mo       |
| `sentinel-daily`    | 13mo      |
| `sentinel-weekly`   | -         |

### Time scales

Using sview, it is possible to display the user data from different time periods.
Each period displays the data with a different precision and a different max age.
The following matrix defines the relations between choosen period (Range),
aggregation window, TTL used for caching the result and the used bucket. It also
shows column called Windows Per Range which says how many point there will be in
the graph. The aggregation can be ommited one day if the plotting technology
will be more user friendly.

| Range | Window | WPR   | Cache TTL | Bucket              |
| :---: | :---:  | :---: | :--:      | :---:               |
| 1h    | 1m     | 60    | 30s       | `sentinel-base`     |
| 12h   | 15m    | 48    | 7m        | `sentinel-minutely` |
| 1d    | 30m    | 48    | 40m       | `sentinel-minutely` |
| 1w    | 3h     | 56    | 2h        | `sentinel-hourly`   |
| 1mo   | 1d     | ~30   | 12h       | `sentinel-hourly`   |
| 3mo   | 2d     | ~45   | 1d        | `sentinel-hourly`   |
| 1y    | 1w     | ~52   | 1d        | `sentinel-daily`    |
