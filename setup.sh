#!/usr/bin/env bash
# set -eu  # stop on first error

# --- project root ---
touch docker-compose.yml  # optional placeholder

# --- backend ---
mkdir -p backend/{migrations,scripts,app/{api,core,db,crud,schemas},tests}

# core backend files
touch backend/{Dockerfile,requirements.txt}
touch backend/scripts/migrate.py
touch backend/app/main.py
touch backend/app/db/connection.py

# migration stubs
touch backend/migrations/{001_hubs.sql,002_links.sql,003_satellites.sql}

# package-level __init__ files (helps import hygiene)
touch backend/app/{__init__.py,api/__init__.py,core/__init__.py,db/__init__.py,crud/__init__.py,schemas/__init__.py}

# --- frontend ---
mkdir -p frontend/src/{routes,components,hooks}
touch frontend/{Dockerfile,package.json,vite.config.ts,tailwind.config.cjs}
touch frontend/src/main.tsx

# route stubs
touch frontend/src/routes/{Splash.tsx,Category.tsx,Question.tsx,Review.tsx,WhiteLabel.tsx}

# component placeholders
touch frontend/src/components/{ProgressBar.tsx,DragList.tsx,ExportMenu.tsx,Layout.tsx}

echo "Scaffold complete."

