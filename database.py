import sqlite3
from datetime import datetime

def create_database():
    print("🔧 Creating database...")

    database_connection = sqlite3.connect('benches.db')
    database_pen = database_connection.cursor()

    database_pen.execute('''
        CREATE TABLE IF NOT EXISTS benches (
        bench_id INTEGER PRIMARY KEY AUTOINCREMENT,
        bench_latitude REAL NOT NULL,
        bench_longitude REAL NOT NULL,
        bench_description TEXT,
        bench_is_available INTEGER DEFAULT 1,
        bench_last_updated TEXT,
        bench_added_by TEXT DEFAULT 'Anonymous'
        )
    ''')

    database_pen.execute('''
        CREATE TABLE IF NOT EXISTS bench_updates (
            update_id INTEGER PRIMARY KEY AUTOINCREMENT,
            which_bench_id INTEGER,
            new_availability_status INTEGER,
            when_updated TEXT,
            who_updated TEXT DEFAULT 'Anonymous',
            FOREIGN KEY (which_bench_id) REFERENCES benches (bench_id)
            )
        ''')
    database_connection.commit()
    database_connection.close()

    print("✅ Database created successfully!")

def add_new_bench(bench_north_south_position, bench_east_west_position, what_bench_looks_like="", person_who_found_bench="Anonymous"):
    print(f"📍 Adding new bench: {what_bench_looks_like}")

    database_connection = sqlite3.connect('benches.db')
    database_pen = database_connection.cursor()

    right_now_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    database_pen.execute('''
        INSERT INTO benches (bench_latitude, bench_longitude, bench_description, bench_added_by)
        VALUES (?, ?, ?, ?)
        ''', (bench_north_south_position, bench_east_west_position, what_bench_looks_like, person_who_found_bench))
    
    database_connection.commit()

    new_bench_id_number = database_pen.lastrowid
    database_connection.close()
    print(f"✅ New bench added with ID: {new_bench_id_number}")
    return new_bench_id_number

def get_all_benches_from_database():
    print("📋 Getting all the benches from database...")

    database_connection = sqlite3.connect('benches.db')
    database_pen = database_connection.cursor()

    database_pen.execute('SELECT * FROM benches')
    
    list_of_all_benches = database_pen.fetchall()
    database_connection.close()

    print(f"Found {len(list_of_all_benches)} benches in database")
    return list_of_all_benches

def update_bench_availability_status(which_bench_to_update, new_available_or_occupied_status, person_making_update="Anonymous"):
    status_in_words = "available" if new_available_or_occupied_status else "occupied"

    print(f"🔄 Updating bench {which_bench_to_update} to {status_in_words}")

    database_connection = sqlite3.connect('benches.db')
    database_pen = database_connection.cursor()

    right_now_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    database_pen.execute('''
        UPDATE benches
        SET bench_is_available = ?, bench_last_updated = ?
        WHERE bench_id = ?
        ''', (new_available_or_occupied_status, right_now_timestamp, which_bench_to_update))
    database_connection.commit()
    database_connection.close()
    
    print(f"✅ Bench {which_bench_to_update} is marked as {status_in_words}")



def find_specific_bench_by_id(bench_id_to_find):
    print(f"🔍 Looking for bench with ID: {bench_id_to_find}")

    database_connection = sqlite3.connect('benches.db')
    database_pen = database_connection.cursor()

    database_pen.execute('SELECT * FROM benches WHERE bench_id = ?', (bench_id_to_find,))

    found_bench_info = database_pen.fetchone()
    database_connection.close()

    if found_bench_info:
        print(f"✅ Found bench: {found_bench_info[3]}")
    else:
        print("❌ Bench not found")
    return found_bench_info

if __name__ == "__main__":
    print("🚀 Testing our database functions...")
    print("=" * 50)
    
    # Step 1: Create the database
    create_database()
    
    # Step 2: Add some sample benches for testing
    print("\n📍 Adding sample benches...")
    first_bench_id = add_new_bench(37.7749, -122.4194, "Red bench in Golden Gate Park", "Sarah")
    second_bench_id = add_new_bench(37.7849, -122.4094, "Wooden bench near the playground", "Mike")
    third_bench_id = add_new_bench(37.7949, -122.3994, "Stone bench by the fountain", "Anna")
    
    # Step 3: Show all benches
    print("\n📋 Current benches in database:")
    all_benches_list = get_all_benches_from_database()
    for single_bench in all_benches_list:
        bench_id = single_bench[0]
        bench_description = single_bench[3]
        bench_lat = single_bench[1]
        bench_lon = single_bench[2]
        bench_creator = single_bench[6]
        print(f"  🪑 Bench {bench_id}: '{bench_description}' at ({bench_lat}, {bench_lon}) - Added by {bench_creator}")
    
    # Step 4: Test updating availability
    print("\n🔄 Testing bench availability updates...")
    update_bench_availability_status(first_bench_id, 0, "TestUser")  # Mark as occupied (0)
    update_bench_availability_status(second_bench_id, 1, "AnotherUser")  # Mark as available (1)
    
    # Step 5: Test getting specific bench
    print("\n🔍 Testing get specific bench...")
    specific_bench_info = find_specific_bench_by_id(first_bench_id)
    if specific_bench_info:
        bench_description = specific_bench_info[3]
        bench_availability = specific_bench_info[4]
        status_text = "Available" if bench_availability else "Occupied"
        print(f"  Bench details: {bench_description} - Status: {status_text}")
    
    print("\n🎉 All tests completed successfully!")
    print("=" * 50)



    

