------ common passwords database scheme
--

CREATE TYPE data_source AS ENUM ('telnet', 'smtp', 'ftp', 'http', 'haas');
CREATE TABLE IF NOT EXISTS passwords(
    id BIGSERIAL PRIMARY KEY,
    password_hash TEXT NOT NULL,
    count BIGINT CHECK (count > 0),
    password_source data_source[]
);
