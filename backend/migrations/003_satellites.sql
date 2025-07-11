CREATE TABLE IF NOT EXISTS sat_project (
    hk_project    UUID NOT NULL REFERENCES hub_project(hk_project),
    name          TEXT NOT NULL,
    duration_min  INT NOT NULL,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    load_dts      TIMESTAMPTZ NOT NULL DEFAULT now(),
    rec_src       TEXT NOT NULL DEFAULT 'app',
    PRIMARY KEY (hk_project, load_dts)
);

CREATE TABLE IF NOT EXISTS sat_category (
    hk_category   UUID NOT NULL REFERENCES hub_category(hk_category),
    label         TEXT NOT NULL,
    display_order INT NOT NULL,
    load_dts      TIMESTAMPTZ NOT NULL DEFAULT now(),
    rec_src       TEXT NOT NULL DEFAULT 'app',
    PRIMARY KEY (hk_category, load_dts)
);

CREATE TABLE IF NOT EXISTS sat_question (
    hk_question   UUID NOT NULL REFERENCES hub_question(hk_question),
    text          TEXT NOT NULL,
    q_type        TEXT NOT NULL,
    est_seconds   INT NOT NULL,
    load_dts      TIMESTAMPTZ NOT NULL DEFAULT now(),
    rec_src       TEXT NOT NULL DEFAULT 'app',
    PRIMARY KEY (hk_question, load_dts)
);
