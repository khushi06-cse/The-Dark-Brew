import sqlite3

DB_NAME = "darkbrew.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Create Tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS menu (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        description TEXT
    )''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Purane incomplete menu ko clear karein taaki naya sahi data load ho sake
    cursor.execute("DELETE FROM menu")
    
    # Pura complete menu aapke frontend ke according
    full_menu = [
        # Signature Brews
        ('Midnight Latte', 'Signature Brews', 210.00, 'Velvety steamed milk poured over an intense ristretto shot.'),
        ('Neon Cold Brew', 'Signature Brews', 240.00, '14-hour slow steeped specialty cold brew coffee.'),
        ('Smoked Artisan Croissant', 'Signature Brews', 160.00, 'Flaky butter pastry infused with subtle wood-fire smoke.'),
        ('Cyber Espresso', 'Signature Brews', 140.00, 'Pure, intense extraction of dark roasted Arabica beans.'),
        ('Shadow Mocha', 'Signature Brews', 250.00, 'Rich espresso blended with dark Belgian chocolate premium syrup.'),
        ('Glitch Matcha Latte', 'Signature Brews', 280.00, 'Authentic Japanese green tea matcha whisked with oat milk.'),
        ('Dark Roast Macchiato', 'Signature Brews', 190.00, 'Espresso marked with a delicate dollop of velvety foam.'),
        ('Binary Cappuccino', 'Signature Brews', 220.00, 'Equal parts espresso, steamed milk, and heavy wet foam.'),
        ('AI Cold Irish Coffee', 'Signature Brews', 270.00, 'Non-alcoholic irish cream blend served over clear ice blocks.'),
        ('Crimson Hack Mocktail', 'Signature Brews', 180.00, 'Zesty blood orange mixed with fresh mint and sparkling soda.'),
        ('Node.js Hot Chocolate', 'Signature Brews', 230.00, 'Pure melted dark chocolate fudge with a marshmallow top.'),
        ('Quantum Glazed Donut', 'Signature Brews', 120.00, 'Dark chocolate coated donut sprinkled with charcoal sugar dust.'),
        
        # Premium Shakes
        ('Thick Belgian Chocolate', 'Premium Shakes', 220.00, 'Rich thick chocolate shake.'),
        ('Oreo Cookie Crunch', 'Premium Shakes', 240.00, 'Oreo blended milkshake.'),
        
        # Cyber Burgers
        ('Classic Veggie Crunch', 'Cyber Burgers', 150.00, 'Crispy veg patty burger.'),
        
        # Classic Hot Coffees
        ('Terminal Espresso', 'Classic Hot Coffees', 100.00, 'Pure intense shot of hot espresso.'),
        ('Admin Americano', 'Classic Hot Coffees', 120.00, 'Espresso shots topped with hot water.'),
        
        # Quick Bites
        ('Classic Salted Fries', 'Quick Bites', 110.00, 'Perfect crispy salted potato fries.')
    ]
    
    cursor.executemany("INSERT INTO menu (item_name, category, price, description) VALUES (?, ?, ?, ?)", full_menu)
    
    conn.commit()
    conn.close()
    print("Database Updated: Pure items sync ho gaye hain!")