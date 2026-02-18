import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path='/mnt/f/The-Evolution-of-Todo-app/phase-5/backend/.env')

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("DATABASE_URL not found in environment variables")
    exit(1)

try:
    # Parse the database URL
    # Format: postgresql://user:password@host:port/database?params
    import re
    match = re.match(r'postgresql://([^:]+):([^@]+)@([^:]+):(\d+)/([^?\s]+)', DATABASE_URL)
    if not match:
        print("Invalid DATABASE_URL format")
        exit(1)
    
    user, password, host, port, database = match.groups()
    
    # Connect to the database
    conn = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )
    
    cursor = conn.cursor()
    
    # Query to check if the 'user' table exists (lowercase because of SQLModel's convention)
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND LOWER(table_name) = 'user';
    """)
    
    user_table_exists = cursor.fetchone()
    
    if user_table_exists:
        print("✓ User table exists in the database")
    else:
        print("✗ User table does not exist in the database")
    
    # Query to check if the 'task' table exists
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND LOWER(table_name) = 'task';
    """)
    
    task_table_exists = cursor.fetchone()
    
    if task_table_exists:
        print("✓ Task table exists in the database")
    else:
        print("✗ Task table does not exist in the database")
    
    # List all tables in the database
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    
    all_tables = cursor.fetchall()
    print(f"\nAll tables in the database ({len(all_tables)}):")
    for table in all_tables:
        print(f"- {table[0]}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"Error connecting to the database: {str(e)}")