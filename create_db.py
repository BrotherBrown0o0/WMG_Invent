import os
import sqlite3

def ensure_instance_folder():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    instance_path = os.path.join(current_dir, 'instance')
    
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)
        print(f"Created instance directory at: {instance_path}")
    
    return instance_path

def init_db():
    instance_path = ensure_instance_folder()
    db_path = os.path.join(instance_path, 'app.sqlite')

    print(f"Attempting to create database at: {db_path}")

    # Create a new SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'user'
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS category (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS product (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        stock_level INTEGER DEFAULT 0,
        min_stock_level INTEGER DEFAULT 10,
        category_id INTEGER,
        sku TEXT UNIQUE,
        FOREIGN KEY (category_id) REFERENCES category (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product_id INTEGER,
        quantity INTEGER NOT NULL,
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES user (id),
        FOREIGN KEY (product_id) REFERENCES product (id)
    )
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print(f"Database created at: {db_path}")

if __name__ == '__main__':
    init_db() 