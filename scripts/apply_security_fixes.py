import sqlite3
import json

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

try:
    print("Applying critical security fixes...")
    
    # Fix #2: Add unique constraint on (theater_id, seat_number)
    print("1. Adding unique constraint on seats...")
    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS movies_seat_theater_seat_unique 
        ON movies_seat(theater_id, seat_number)
    """)
    
    # Add index for performance
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS movies_seat_theater_status_idx 
        ON movies_seat(theater_id, status)
    """)
    
    # Fix #5: Create webhook event tracking table
    print("2. Creating webhook event tracking table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movies_stripewebhookevent (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id VARCHAR(255) UNIQUE NOT NULL,
            event_type VARCHAR(100) NOT NULL,
            processed_at DATETIME NOT NULL,
            payload TEXT
        )
    """)
    
    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS movies_stripewebhookevent_event_id 
        ON movies_stripewebhookevent(event_id)
    """)
    
    # Note: Fix #15 (OneToOne to ForeignKey) doesn't require schema change in SQLite
    # The constraint is enforced at Django ORM level
    
    conn.commit()
    print("✅ All migrations applied successfully!")
    
except sqlite3.Error as e:
    print(f"❌ Error: {e}")
    conn.rollback()
finally:
    conn.close()
