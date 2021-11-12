# pwned-turris

Have i been pawned backend implementation.

## Workflow

1. Recieves request in form of json posted to `http://page.xyz/api/leaked`
2. Selects hashes in database that starts with request hash.
3. Return matching hashes with counts.

step 3. is heavily influenced by how the schema is planned.

## Request/response json schema

Refer to [schema](schema/pwned.json)

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
export FLASK_APP=src/pwned
```