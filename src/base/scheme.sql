---- scheme.sql
--

-- A scheme for saving (serial number, device token) tuples
CREATE TABLE IF NOT EXISTS identity (
    id BIGSERIAL PRIMARY KEY,
    sn VARCHAR(16) NOT NULL,
    device_token VARCHAR(64),
    UNIQUE(sn, device_token)
);

-- A scheme for saving minipot-telnet messages
-- CREATE TYPE telnet_action_t AS ENUM ('connect', 'login', 'invalid');
CREATE TABLE IF NOT EXISTS minipot_telnet (
    id BIGSERIAL PRIMARY KEY,
    identity_id BIGINT REFERENCES identity(id),
    ts BIGINT NOT NULL,
    action VARCHAR(16) NOT NULL,
    ip INET NOT NULL,
    country VARCHAR(2),
    asn INTEGER,
    username TEXT,
    password TEXT
);

-- A scheme for saving minipot-http messages
-- CREATE TYPE http_action_t AS ENUM ('connect', 'login', 'invalid', 'message');
CREATE TABLE IF NOT EXISTS minipot_http (
    id BIGSERIAL PRIMARY KEY,
    identity_id BIGINT REFERENCES identity(id),
    ts BIGINT NOT NULL,
    action VARCHAR(16) NOT NULL,
    ip INET NOT NULL,
    country VARCHAR(2),
    asn INTEGER,
    method TEXT,
    url TEXT,
    user_agent TEXT,
    username TEXT,
    password TEXT
);

-- A scheme for saving minipot-ftp messages
-- CREATE TYPE ftp_action_t AS ENUM ('connect', 'login', 'invalid');
CREATE TABLE IF NOT EXISTS minipot_ftp (
    id BIGSERIAL PRIMARY KEY,
    identity_id BIGINT REFERENCES identity(id),
    ts BIGINT NOT NULL,
    action VARCHAR(16) NOT NULL,
    ip INET NOT NULL,
    country VARCHAR(2),
    asn INTEGER,
    username TEXT,
    password TEXT
);

-- A scheme for saving minipot-smtp messages
--CREATE TYPE smtp_action_t AS ENUM ('connect', 'login', 'invalid');
-- CREATE TYPE smtp_mechanism_t AS ENUM ('login', 'plain');
CREATE TABLE IF NOT EXISTS minipot_smtp (
    id BIGSERIAL PRIMARY KEY,
    identity_id BIGINT REFERENCES identity(id),
    ts BIGINT NOT NULL,
    action VARCHAR(16) NOT NULL,
    ip INET NOT NULL,
    country VARCHAR(2),
    asn INTEGER,
    mechanism VARCHAR(16),
    username TEXT,
    password TEXT
);

-- A scheme for saving fwlogs messages
-- CREATE TYPE protocol_t AS ENUM ('TCP', 'UDP', 'other');
CREATE TABLE IF NOT EXISTS fwlogs (
    id BIGSERIAL PRIMARY KEY,
    ts BIGINT NOT NULL,
    identity_id BIGINT REFERENCES identity(id),
    ip INET NOT NULL,
    country VARCHAR(2),
    asn INTEGER,
    protocol VARCHAR(16) NOT NULL,
    local_ip INET NOT NULL,
    local_ports INTEGER[],
    packet_count INTEGER NOT NULL
);
