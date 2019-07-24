CREATE TABLE IF NOT EXISTS minipot_telnet (
    id BIGSERIAL PRIMARY KEY,
    ts BIGINT NOT NULL,  -- Timestamp
    action TEXT NOT NULL CHECK (action IN ('connect', 'login')),
    ip TEXT NOT NULL,  -- e.g. 157.145.25.47
    country VARCHAR(2), -- e.g. cz
    username TEXT,
    password TEXT
);
