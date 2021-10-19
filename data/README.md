# Data


## Requirements

```
pip install psycopg2
```


## Data import

Prepare database scheme:

```
psql --username=... --host=... --dbname=... < data/scheme.sql
```

Import example data to database:

```
python3 data/import.py --username=... --host=... --dbname=... data/passwords.csv
```
