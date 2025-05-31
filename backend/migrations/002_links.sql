CREATE TABLE link_project_category (
    hk_project_category UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hk_project          UUID NOT NULL REFERENCES hub_project(hk_project),
    hk_category         UUID NOT NULL REFERENCES hub_category(hk_category),
    load_dts            TIMESTAMPTZ NOT NULL DEFAULT now(),
    rec_src             TEXT NOT NULL DEFAULT 'app',
    UNIQUE (hk_project, hk_category)
);

CREATE TABLE link_project_question (
    hk_project_question UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hk_project          UUID NOT NULL REFERENCES hub_project(hk_project),
    hk_question         UUID NOT NULL REFERENCES hub_question(hk_question),
    load_dts            TIMESTAMPTZ NOT NULL DEFAULT now(),
    rec_src             TEXT NOT NULL DEFAULT 'app',
    UNIQUE (hk_project, hk_question)
);

