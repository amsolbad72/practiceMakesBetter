# database.py
# This file creates and manages our bench database
# Think of it as setting up a digital filing cabinet! 📁

import sqlite3
from datetime import datetime

def create_database():
    """
    This function creates our database and tables.
    It's like setting up a new notebook with specific page layouts!
    """
    
    # Connect to our database file (it will create one if it doesn't exist)
    # Think of this as opening our digital notebook
    connection = sqlite3.connect('benches.db')
    
    # A cursor is like a pen that we use to write in our notebook
    cursor = connection.cursor()
    
    # Create our benches table
    # This is like creating a template for each bench page in our notebook
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS benches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            description TEXT,
            is_available INTEGER DEFAULT 1,
            last_updated TEXT,
            added_by TEXT DEFAULT 'Anonymous'
        )
    ''')
    
    # Let me explain each column (like fields on a form):
    # - id: A unique number for each bench (like a student ID number)
    # - latitude: How far north/south the bench is (GPS coordinate)
    # - longitude: How far east/west the bench is (GPS coordinate)
    # - description: What the bench looks like or where exactly it is
    # - is_available: 1 means available, 0 means occupied (like a checkbox)
    # - last_updated: When someone last checked this bench
    # - added_by: Who found this bench and added it to our app
    
    # Create a table for tracking when people check benches
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bench_updates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bench_id INTEGER,
            is_available INTEGER,
            updated_at TEXT,
            updated_by TEXT DEFAULT 'Anonymous',
            FOREIGN KEY (bench_id) REFERENCES benches (id)
        )
    ''')
    
    # Save our changes (like closing and saving our notebook)
    connection.commit()
    
    # Close the connection (like putting our notebook away)
    connection.close()
    
    print("🎉 Database created successfully!")

def add_bench(latitude, longitude, description="", added_by="Anonymous"):
    """
    This function adds a new bench to our database.
    It's like writing a new entry in our bench notebook!
    
    Parameters (the information we need):
    - latitude: GPS coordinate (north/south position)
    - longitude: GPS coordinate (east/west position) 
    - description: What the bench looks like
    - added_by: Name of the person adding the bench
    """
    
    # Connect to our database
    connection = sqlite3.connect('benches.db')
    cursor = connection.cursor()
    
    # Get the current time (so we know when this bench was added)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Insert the new bench into our database
    # The ? marks are placeholders - Python will fill them in safely
    cursor.execute('''
        INSERT INTO benches (latitude, longitude, description, last_updated, added_by)
        VALUES (?, ?, ?, ?, ?)
    ''', (latitude, longitude, description, current_time, added_by))
    
    # Save the changes
    connection.commit()
    
    # Get the ID of the bench we just added
    bench_id = cursor.lastrowid
    
    # Close the connection
    connection.close()
    
    print(f"✅ New bench added with ID: {bench_id}")
    return bench_id

def get_all_benches():
    """
    This function gets all benches from our database.
    It's like reading through our entire bench notebook!
    """
    
    connection = sqlite3.connect('benches.db')
    cursor = connection.cursor()
    
    # Get all benches from our table
    cursor.execute('SELECT * FROM benches')
    
    # Fetch all the results
    benches = cursor.fetchall()
    
    connection.close()
    
    return benches

def update_bench_availability(bench_id, is_available, updated_by="Anonymous"):
    """
    This function updates whether a bench is available or not.
    It's like updating the status on a specific page in our notebook!
    
    Parameters:
    - bench_id: Which bench we're updating
    - is_available: 1 for available, 0 for occupied
    - updated_by: Who is making this update
    """
    
    connection = sqlite3.connect('benches.db')
    cursor = connection.cursor()
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Update the bench's availability
    cursor.execute('''
        UPDATE benches 
        SET is_available = ?, last_updated = ? 
        WHERE id = ?
    ''', (is_available, current_time, bench_id))
    
    # Also record this update in our updates table (like keeping a history)
    cursor.execute('''
        INSERT INTO bench_updates (bench_id, is_available, updated_at, updated_by)
        VALUES (?, ?, ?, ?)
    ''', (bench_id, is_available, current_time, updated_by))
    
    connection.commit()
    connection.close()
    
    status = "available" if is_available else "occupied"
    print(f"✅ Bench {bench_id} marked as {status}")

def get_bench_by_id(bench_id):
    """
    This function gets information about one specific bench.
    It's like looking up one specific page in our notebook!
    """
    
    connection = sqlite3.connect('benches.db')
    cursor = connection.cursor()
    
    cursor.execute('SELECT * FROM benches WHERE id = ?', (bench_id,))
    bench = cursor.fetchone()
    
    connection.close()
    
    return bench

# Test our database functions (only run when this file is executed directly)
if __name__ == "__main__":
    print("🔧 Setting up the database...")
    create_database()
    
    # Add some sample benches for testing
    print("📍 Adding sample benches...")
    add_bench(37.7749, -122.4194, "Bench in Golden Gate Park", "TestUser")
    add_bench(37.7849, -122.4094, "Bench near the playground", "TestUser")
    
    print("📋 Current benches in database:")
    benches = get_all_benches()
    for bench in benches:
        print(f"  Bench ID {bench[0]}: {bench[3]} at ({bench[1]}, {bench[2]})")