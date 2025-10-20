import sqlite3
from pathlib import Path
from datetime import datetime
from utils.auth import hash_password

DB_PATH = Path('database') / 'inventory.db'

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password BLOB NOT NULL,
        role TEXT NOT NULL DEFAULT 'user',
        created_at TEXT
    )''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        sku TEXT,
        category TEXT,
        quantity INTEGER NOT NULL DEFAULT 0,
        price REAL NOT NULL DEFAULT 0.0,
        supplier TEXT,
        image_path TEXT,
        description TEXT,
        added_date TEXT
    )''')
    conn.commit()
    # seed default users if not present
    cur.execute("SELECT COUNT(*) as c FROM users")
    if cur.fetchone()['c'] == 0:
        cur.execute('INSERT INTO users (username, password, role, created_at) VALUES (?, ?, ?, ?)', 
                    ('admin', hash_password('admin'), 'admin', datetime.utcnow().isoformat()))
        cur.execute('INSERT INTO users (username, password, role, created_at) VALUES (?, ?, ?, ?)', 
                    ('user', hash_password('user'), 'user', datetime.utcnow().isoformat()))
        conn.commit()
    conn.close()

def add_user(username, plain_password, role='user'):
    conn = get_connection(); cur = conn.cursor()
    cur.execute('INSERT INTO users (username, password, role, created_at) VALUES (?, ?, ?, ?)',
                (username, hash_password(plain_password), role, datetime.utcnow().isoformat()))
    conn.commit(); conn.close()

def find_user(username):
    conn = get_connection(); cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username=?', (username,))
    row = cur.fetchone(); conn.close()
    return row

def update_user_role(user_id, role):
    conn = get_connection(); cur = conn.cursor()
    cur.execute('UPDATE users SET role=? WHERE id=?', (role, user_id))
    conn.commit(); conn.close()

def fetch_users():
    conn = get_connection(); cur = conn.cursor()
    cur.execute('SELECT id, username, role, created_at FROM users ORDER BY id DESC')
    rows = cur.fetchall(); conn.close(); return rows

# product helpers
def fetch_products(search=None):
    conn = get_connection(); cur = conn.cursor()
    base = 'SELECT * FROM products'
    params = ()
    if search:
        q = '%' + search + '%'
        base += ' WHERE name LIKE ? OR sku LIKE ? OR category LIKE ? OR supplier LIKE ?'
        params = (q,q,q,q)
    base += ' ORDER BY id DESC'
    cur.execute(base, params)
    rows = cur.fetchall(); conn.close(); return rows

def add_product(data):
    conn = get_connection(); cur = conn.cursor()
    cur.execute('''INSERT INTO products (name, sku, category, quantity, price, supplier, image_path, description, added_date)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (data['name'], data.get('sku'), data.get('category'), data.get('quantity',0),
                 data.get('price',0.0), data.get('supplier'), data.get('image_path'), data.get('description'), data.get('added_date')))
    conn.commit(); conn.close()

def update_product(pid, data):
    conn = get_connection(); cur = conn.cursor()
    cur.execute('''UPDATE products SET name=?, sku=?, category=?, quantity=?, price=?, supplier=?, image_path=?, description=? WHERE id=?''',
                (data['name'], data.get('sku'), data.get('category'), data.get('quantity',0), data.get('price',0.0),
                 data.get('supplier'), data.get('image_path'), data.get('description'), pid))
    conn.commit(); conn.close()

def delete_product(pid):
    conn = get_connection(); cur = conn.cursor()
    cur.execute('DELETE FROM products WHERE id=?', (pid,))
    conn.commit(); conn.close()
