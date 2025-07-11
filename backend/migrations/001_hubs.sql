CREATE EXTENSION IF NOT EXISTS "pgcrypto";  -- for gen_random_uuid()

CREATE TABLE IF NOT EXISTS hub_project (
    hk_project   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    bk_project   TEXT NOT NULL UNIQUE,
    load_dts     TIMESTAMPTZ NOT NULL DEFAULT now(),
    rec_src      TEXT NOT NULL DEFAULT 'app'
);

CREATE TABLE IF NOT EXISTS hub_client (
    hk_client    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    bk_client    TEXT NOT NULL UNIQUE,
    load_dts     TIMESTAMPTZ NOT NULL DEFAULT now(),
    rec_src      TEXT NOT NULL DEFAULT 'app'
);

CREATE TABLE IF NOT EXISTS hub_category (
    hk_category  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    bk_category  TEXT NOT NULL UNIQUE,
    load_dts     TIMESTAMPTZ NOT NULL DEFAULT now(),
    rec_src      TEXT NOT NULL DEFAULT 'app'
);

CREATE TABLE IF NOT EXISTS hub_question (
    hk_question  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    bk_question  TEXT NOT NULL UNIQUE,
    load_dts     TIMESTAMPTZ NOT NULL DEFAULT now(),
    rec_src      TEXT NOT NULL DEFAULT 'app'
);

