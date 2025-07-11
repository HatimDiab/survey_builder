-- Migration 004: Add objectives and customization tables
-- This migration adds the new Data Vault tables for objectives and client customization

-- Hub table for objectives (replacing categories)
CREATE TABLE IF NOT EXISTS hub_objective (
    hk_objective  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    bk_objective  TEXT NOT NULL UNIQUE,
    load_dts      TIMESTAMPTZ NOT NULL DEFAULT now(),
    rec_src       TEXT NOT NULL DEFAULT 'app'
);

-- Link table connecting projects to objectives
CREATE TABLE IF NOT EXISTS link_project_objective (
    hk_project_objective UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hk_project          UUID NOT NULL REFERENCES hub_project(hk_project),
    hk_objective        UUID NOT NULL REFERENCES hub_objective(hk_objective),
    load_dts            TIMESTAMPTZ NOT NULL DEFAULT now(),
    rec_src             TEXT NOT NULL DEFAULT 'app',
    UNIQUE (hk_project, hk_objective)
);

-- Satellite table for objective attributes
CREATE TABLE IF NOT EXISTS sat_objective (
    hk_objective   UUID NOT NULL REFERENCES hub_objective(hk_objective),
    label          TEXT NOT NULL,
    display_order  INT NOT NULL,
    load_dts       TIMESTAMPTZ NOT NULL DEFAULT now(),
    rec_src        TEXT NOT NULL DEFAULT 'app',
    PRIMARY KEY (hk_objective, load_dts)
);

-- Satellite table for client attributes (customization)
CREATE TABLE IF NOT EXISTS sat_client (
    hk_client      UUID NOT NULL REFERENCES hub_client(hk_client),
    company_name   TEXT NOT NULL,
    logo_url       TEXT,
    primary_color  TEXT,
    secondary_color TEXT,
    load_dts       TIMESTAMPTZ NOT NULL DEFAULT now(),
    rec_src        TEXT NOT NULL DEFAULT 'app',
    PRIMARY KEY (hk_client, load_dts)
);

-- Update sat_question to include options field for multiple choice questions
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'sat_question' AND column_name = 'options') THEN
        ALTER TABLE sat_question ADD COLUMN options TEXT;
    END IF;
END $$;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_hub_objective_bk ON hub_objective(bk_objective);
CREATE INDEX IF NOT EXISTS idx_link_project_objective_project ON link_project_objective(hk_project);
CREATE INDEX IF NOT EXISTS idx_link_project_objective_objective ON link_project_objective(hk_objective);
CREATE INDEX IF NOT EXISTS idx_sat_objective_hk ON sat_objective(hk_objective);
CREATE INDEX IF NOT EXISTS idx_sat_client_hk ON sat_client(hk_client); 