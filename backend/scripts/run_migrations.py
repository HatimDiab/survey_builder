#!/usr/bin/env python3
"""
Script to run Data Vault migrations
"""
import os
import sys
import psycopg2
from pathlib import Path

# Add the backend directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

def run_migration(migration_file):
    """Run a single migration file"""
    try:
        # Database connection parameters
        db_params = {
            'host': os.getenv('DB_HOST', 'db'),
            'port': os.getenv('DB_PORT', '5432'),
            'database': os.getenv('DB_NAME', 'survey_builder'),
            'user': os.getenv('DB_USER', 'survey'),
            'password': os.getenv('DB_PASSWORD', 'survey')
        }
        
        # Connect to database
        conn = psycopg2.connect(**db_params)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Read and execute migration
        migration_path = Path(__file__).parent.parent / 'migrations' / migration_file
        with open(migration_path, 'r') as f:
            sql = f.read()
        
        print(f"Running migration: {migration_file}")
        cursor.execute(sql)
        print(f"Migration {migration_file} completed successfully")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error running migration {migration_file}: {str(e)}")
        # Don't exit on migration errors - they might already exist
        print(f"Continuing with next migration...")
        return False
    
    return True

def main():
    """Run all migrations in order"""
    migrations = [
        '001_hubs.sql',
        '002_links.sql', 
        '003_satellites.sql',
        '004_objectives_and_customization.sql'
    ]
    
    print("Starting Data Vault migrations...")
    
    successful_migrations = 0
    for migration in migrations:
        if run_migration(migration):
            successful_migrations += 1
    
    print(f"Migration process completed. {successful_migrations}/{len(migrations)} migrations executed successfully.")
    if successful_migrations == len(migrations):
        print("All migrations completed successfully!")
    else:
        print("Some migrations may have already been applied or encountered errors.")

if __name__ == "__main__":
    main() 