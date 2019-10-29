# Sentinel:View

A component visualising data gathered by **Sentinel**.

## Python requirements

Python Package Index requirements (including the development ones) are stated in
`setup.py`

## Infrastructure requirements

- Postgresql DB (example scheme in `/dev/scheme.sql`)
- Redis server


## Development usage

- Establish python virtual environment (use
  [wrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) optionally)
  and install `sview` package. Consider using `-e` option: `pip install -e ./sview`
- Set the configuration in `instance/local.cfg`. The default configuration
  can be found in `sview/default_settings.py`.
    - For postgres DB use syntax:
        ```
        SQLALCHEMY_DATABASE_URI = "postgresql://user:password@hostname/databasename"
        ```
    - For non-debug run it is also needed to specify `SECRET_KEY`
- Example database structure to work with can be seen in `dev/scheme.sql` and
  should be compatible with
  [Dumper scheme](https://gitlab.labs.nic.cz/turris/sentinel/dumper/blob/master/scheme.sql)
- Run the application using `flask run` (Use wsgi server for production!)
- Run some workers using `flask rq worker`. (Using only `rq worker` would lack
  any configuration and would end up working outside the application context).
- Populate Redis with initial database data using `flask queue-queries`
