#!/usr/bin/env python3
"""
Check if Phase 5 database tables exist in Neon database
"""
import os
from sqlmodel import create_engine, Session, SQLModel, text
from dotenv import load_dotenv

# Load environment variables from Phase 5 backend
load_dotenv("phase-5/backend/.env")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set in phase-5/backend/.env")

print(f"Connecting to database: {DATABASE_URL}")

# Create engine
engine = create_engine(DATABASE_URL)

# Import Phase 5 models to register them
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "phase-5", "backend", "app"))
from models import Task, Conversation, Message, AuditLog

# Check existing tables
with Session(engine) as session:
    result = session.execute(text("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name
    """))
    existing_tables = [row[0] for row in result.all()]
    print(f"\nExisting tables in database: {existing_tables}")

    # Check if our expected tables exist
    expected_tables = ['task', 'conversation', 'message', 'auditlog']
    missing_tables = []
    
    for table in expected_tables:
        if table not in existing_tables:
            missing_tables.append(table)
    
    if missing_tables:
        print(f"\n❌ Missing tables: {missing_tables}")
        print("Tables need to be created.")
    else:
        print(f"\n✅ All expected tables exist: {expected_tables}")
        
        # Check columns for each table
        for table in expected_tables:
            print(f"\nTable '{table}' columns:")
            cols = session.execute(text(f"""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = '{table}'
                ORDER BY ordinal_position
            """))
            for col in cols:
                print(f"   - {col[0]}: {col[1]} (nullable: {col[2]})")

print("\nDatabase check complete!")