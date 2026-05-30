import os
import sqlite3
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SQLITE_DB_PATH = "vehicle_rental.db"

# Cached DB mode: None, 'supabase', or 'sqlite'
_db_mode = None
_supabase_client = None

def check_db_mode():
    """
    Checks if Supabase is available and reachable.
    If yes, uses Supabase. Otherwise, falls back to SQLite.
    """
    global _db_mode, _supabase_client
    if _db_mode is not None:
        return _db_mode

    if not SUPABASE_URL or not SUPABASE_KEY:
        _db_mode = "sqlite"
        init_sqlite_db()
        return _db_mode

    try:
        from supabase import create_client
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        # Attempt a quick light-weight query to check actual connectivity
        client.table("customers").select("id").limit(1).execute()
        _supabase_client = client
        _db_mode = "supabase"
    except Exception:
        # Fall back to SQLite on connection errors or timeouts
        _db_mode = "sqlite"
        init_sqlite_db()
    
    return _db_mode

def get_db_mode():
    """Returns 'supabase' or 'sqlite' depending on connection status."""
    return check_db_mode()

@lru_cache()
def get_supabase():
    """Returns the cached Supabase client if connected, else raises error."""
    global _supabase_client
    if _supabase_client is not None:
        return _supabase_client
    
    mode = check_db_mode()
    if mode == "supabase":
        return _supabase_client
    raise RuntimeError("Supabase client is not available in SQLite mode")

def get_sqlite_conn():
    """Establishes and returns a connection to the local SQLite database."""
    conn = sqlite3.connect(SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    # Enable foreign keys support
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_sqlite_db():
    """Initializes the local SQLite tables and loads realistic seed data if empty."""
    conn = get_sqlite_conn()
    cursor = conn.cursor()

    # 1. Create Customers Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT,
        license_no TEXT,
        address TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 2. Create Vehicles Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vehicles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plate TEXT UNIQUE NOT NULL,
        model TEXT NOT NULL,
        type TEXT NOT NULL,
        rate REAL NOT NULL,
        available BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 3. Create Rentals Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rentals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicle_id INTEGER NOT NULL,
        customer_id INTEGER NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE,
        FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
    );
    """)

    # 4. Create Payments Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rental_id INTEGER NOT NULL,
        customer_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        payment_date TEXT NOT NULL,
        payment_type TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (rental_id) REFERENCES rentals(id) ON DELETE CASCADE,
        FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
    );
    """)

    # 5. Create Maintenance Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS maintenance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicle_id INTEGER NOT NULL,
        description TEXT NOT NULL,
        cost REAL NOT NULL,
        date TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE
    );
    """)

    conn.commit()

    # --- Seed Data Insertion ---
    # Check if empty before seeding
    cursor.execute("SELECT COUNT(*) FROM customers;")
    if cursor.fetchone()[0] == 0:
        print("🌱 Seeding SQLite database with professional mock data...")
        
        # Customers
        customers_seed = [
            ("Alice Smith", "alice@example.com", "+1-555-0199", "DL-WASH48291", "123 Maple St, Seattle, WA"),
            ("Bob Johnson", "bob@example.com", "+1-555-0143", "DL-MASS90123", "456 Pine St, Boston, MA"),
            ("Charlie Brown", "charlie@example.com", "+1-555-0187", "DL-COLO55678", "789 Oak St, Denver, CO"),
            ("David Miller", "david@example.com", "+1-555-0112", "DL-ILLI11234", "101 Elm St, Chicago, IL")
        ]
        cursor.executemany("""
            INSERT INTO customers (name, email, phone, license_no, address)
            VALUES (?, ?, ?, ?, ?);
        """, customers_seed)

        # Vehicles
        vehicles_seed = [
            ("AP-01-A-1234", "Toyota Innova Crysta", "Car", 2500.0, 1),
            ("TS-09-B-5678", "Royal Enfield Classic 350", "Motorcycle", 800.0, 1),
            ("MH-12-C-9012", "Mahindra Thar 4x4", "Car", 3500.0, 1),
            ("KA-51-D-3456", "Tata Winger", "Van", 4000.0, 0), # Currently rented
            ("DL-01-E-7890", "Ashok Leyland Dost", "Truck", 2000.0, 1)
        ]
        cursor.executemany("""
            INSERT INTO vehicles (plate, model, type, rate, available)
            VALUES (?, ?, ?, ?, ?);
        """, vehicles_seed)

        # Rentals (Vehicle 4 rented by Customer 2)
        cursor.execute("""
            INSERT INTO rentals (vehicle_id, customer_id, start_date, end_date)
            VALUES (4, 2, '2026-05-25', '2026-05-31');
        """)

        # Payments (Payment for Rental 1)
        cursor.execute("""
            INSERT INTO payments (rental_id, customer_id, amount, payment_date, payment_type)
            VALUES (1, 2, 24000.00, '2026-05-25', 'Card');
        """)

        # Maintenance (Vehicle 3 in maintenance)
        cursor.execute("""
            INSERT INTO maintenance (vehicle_id, description, cost, date)
            VALUES (3, 'Scheduled oil change, brake caliper cleaning, and multi-point safety inspection.', 1500.00, '2026-05-29');
        """)
        # Set vehicle 3 as unavailable due to maintenance
        cursor.execute("UPDATE vehicles SET available = 0 WHERE id = 3;")

        conn.commit()

    conn.close()
