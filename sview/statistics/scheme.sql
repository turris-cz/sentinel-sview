---- scheme.sql
--

-- A scheme for saving (serial number, device token) tuples
CREATE TABLE IF NOT EXISTS identity (
    id BIGSERIAL PRIMARY KEY,
    sn VARCHAR(16) NOT NULL,
    device_token VARCHAR(64) NOT NULL,
    UNIQUE(sn, device_token)
);

-- A scheme for saving incidents
CREATE TYPE trap_t AS ENUM ('minipot_ftp', 'minipot_smtp', 'minipot_telnet', 'minipot_http', 'fwlogs');
CREATE TYPE action_t AS ENUM ('connect', 'login', 'message', 'invalid', 'small_port_scan', 'big_port_scan');
CREATE TABLE IF NOT EXISTS incidents (
    time TIMESTAMPTZ NOT NULL,
    raw_count BIGINT DEFAULT 1,
    identity_id BIGINT REFERENCES identity(id) NOT NULL,
    trap trap_t NOT NULL,
    action action_t NOT NULL,
    ip inet NOT NULL,
    country VARCHAR(2)
);
SELECT create_hypertable('incidents', 'time');

CREATE TABLE IF NOT EXISTS incidents_quarterly (LIKE incidents INCLUDING DEFAULTS INCLUDING CONSTRAINTS);
SELECT create_hypertable('incidents_quarterly', 'time');

CREATE TABLE IF NOT EXISTS incidents_hourly (LIKE incidents INCLUDING DEFAULTS INCLUDING CONSTRAINTS);
SELECT create_hypertable('incidents_hourly', 'time');

CREATE TABLE IF NOT EXISTS incidents_daily (LIKE incidents INCLUDING DEFAULTS INCLUDING CONSTRAINTS);
SELECT create_hypertable('incidents_daily', 'time');

-- A scheme for saving passwords
CREATE TABLE IF NOT EXISTS passwords (
    time TIMESTAMPTZ NOT NULL,
    raw_count BIGINT DEFAULT 1,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);
SELECT create_hypertable('passwords', 'time');

CREATE TABLE IF NOT EXISTS passwords_quarterly (LIKE passwords INCLUDING DEFAULTS INCLUDING CONSTRAINTS);
SELECT create_hypertable('passwords_quarterly', 'time');

CREATE TABLE IF NOT EXISTS passwords_hourly (LIKE passwords INCLUDING DEFAULTS INCLUDING CONSTRAINTS);
SELECT create_hypertable('passwords_hourly', 'time');

CREATE TABLE IF NOT EXISTS passwords_daily (LIKE passwords INCLUDING DEFAULTS INCLUDING CONSTRAINTS);
SELECT create_hypertable('passwords_daily', 'time');

-- A scheme for saving scanned ports
CREATE TYPE protocol_t AS ENUM ('TCP', 'UDP', 'other');
CREATE TABLE IF NOT EXISTS ports (
    time TIMESTAMPTZ NOT NULL,
    raw_count BIGINT DEFAULT 1,
    port INTEGER NOT NULL,
    protocol protocol_t NOT NULL
);
SELECT create_hypertable('ports', 'time');

CREATE TABLE IF NOT EXISTS ports_quarterly (LIKE ports INCLUDING DEFAULTS INCLUDING CONSTRAINTS);
SELECT create_hypertable('ports_quarterly', 'time');

CREATE TABLE IF NOT EXISTS ports_hourly (LIKE ports INCLUDING DEFAULTS INCLUDING CONSTRAINTS);
SELECT create_hypertable('ports_hourly', 'time');

CREATE TABLE IF NOT EXISTS ports_daily (LIKE ports INCLUDING DEFAULTS INCLUDING CONSTRAINTS);
SELECT create_hypertable('ports_daily', 'time');


-- A schema for Sentinel's You Have Been Pwned
CREATE TYPE data_source AS ENUM ('telnet', 'smtp', 'ftp', 'http', 'haas');
CREATE TABLE IF NOT EXISTS passwords_pwned(
    id BIGSERIAL PRIMARY KEY,
    password_hash TEXT NOT NULL,
    count BIGINT CHECK (count > 0),
    password_source data_source[]
);