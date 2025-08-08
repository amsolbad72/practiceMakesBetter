import sqlite3
from datetime import datetime

def create_database():
    print("🔧 Creating database...")

    connection = sqlite3.connect('benches.db')
    cursor = connection.cursor()
    