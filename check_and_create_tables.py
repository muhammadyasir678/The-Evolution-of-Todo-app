#!/usr/bin/env python3
"""
Check and create database tables in Neon PostgreSQL
"""
import os
from sqlmodel import create_engine, Session, SQLModel, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv("phase-3/backend/.env")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")
print(f"Connecting to database...")

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Import models to register them
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "phase-3", "backend", "app"))
from models import Task, Conversation, Message

# Check existing tables
with Session(engine) as session:
    result = session.execute(text("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name
    """))
    existing_tables = [row[0] for row in result.all()]
    print(f"\nExisting tables: {existing_tables}")

# Create all tables (safe to run - won't recreate existing tables)
print("\nCreating tables if they don't exist...")
SQLModel.metadata.create_all(engine)

# Verify tables were created
with Session(engine) as session:
    result = session.execute(text("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name
    """))
    final_tables = [row[0] for row in result.all()]
    print(f"\nFinal tables in database: {final_tables}")

    # Check columns for each table
    for table in ['task', 'conversation', 'message']:
        if table in final_tables:
            print(f"\nTable '{table}' columns:")
            cols = session.execute(text(f"""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = '{table}'
                ORDER BY ordinal_position
            """))
            for col in cols:
                print(f"   - {col[0]}: {col[1]} (nullable: {col[2]})")

print("\nDatabase tables check complete!")
