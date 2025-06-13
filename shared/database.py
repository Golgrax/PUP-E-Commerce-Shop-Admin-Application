import mysql.connector
from mysql.connector import errorcode
import hashlib

DB_CONFIG = {
    'user': 'root',
    'password': 'Test1234!',
    'host': '127.0.0.1',
}
DB_NAME = 'pup_shop_db'

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_connection():
    try:
        cnx = mysql.connector.connect(**DB_CONFIG)
        return cnx
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def setup_database():
    cnx = create_connection()
    if not cnx:
        print("Could not establish connection to MySQL. Aborting setup.")
        return
        
    cursor = cnx.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET 'utf8'")
        print(f"Database '{DB_NAME}' created or already exists.")
        DB_CONFIG['database'] = DB_NAME
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        exit(1)
    
    cnx.close()

    db_cnx = mysql.connector.connect(**DB_CONFIG)
    cursor = db_cnx.cursor()

    tables = {}
    tables['users'] = (
        "CREATE TABLE `users` ("
        "  `id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `name` varchar(255) NOT NULL,"
        "  `email` varchar(255) NOT NULL UNIQUE,"
        "  `password_hash` varchar(255) NOT NULL,"
        "  `address1` text,"
        "  `address2` text,"
        "  PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB")

    tables['products'] = (
        "CREATE TABLE `products` ("
        "  `id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `name` varchar(255) NOT NULL,"
        "  `description` text,"
        "  `price` decimal(10, 2) NOT NULL,"
        "  `image_url` varchar(255) NOT NULL,"
        "  `stock` int(11) NOT NULL DEFAULT 0,"
        "  `variations` varchar(255),"
        "  `sold_count` INT NOT NULL DEFAULT 0,"
        "  PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB")
    
    for table_name in tables:
        table_description = tables[table_name]
        try:
            print(f"Creating table {table_name}: ", end='')
            cursor.execute(table_description)
            print("OK")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)

    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        print("Inserting placeholder products...")
        placeholder_products = [
            ('PUP Minimalist Baybayin Lanyard', 'Stylish lanyard with Baybayin script.', 140.00, '/static/images/product_lanyard_1.png', 100, 'Coquette,Classic', 50),
            ('PUP Jeepney Signage', 'Fun sticker for your laptop.', 20.00, '/static/images/product_jeepney.png', 200, 'Iskolar Script', 120),
            ('PUP Iskolar TOTE BAG (V1)', 'Canvas tote bag for every Iskolar.', 160.00, '/static/images/product_tote_1.png', 150, 'White', 30),
            ('PUP Iskolar TOTE BAG (V2)', 'Another great tote bag design.', 160.00, '/static/images/product_tote_2.png', 150, 'Cream', 45),
            ('PUP STUDY WITH STYLE Shirt', 'Premium quality shirt.', 450.00, '/static/images/product_shirt.png', 80, 'S,M,L,XL', 22),
            ('PUP Baybayin Lanyard (Classic)', 'Classic edition lanyard.', 140.00, '/static/images/product_lanyard_2.png', 100, 'Classic', 65),
        ]
        insert_query = ("INSERT INTO products "
                        "(name, description, price, image_url, stock, variations, sold_count) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s)")
        cursor.executemany(insert_query, placeholder_products)
        db_cnx.commit()
        print("Placeholder products inserted.")
    
    cursor.close()
    db_cnx.close()

def get_db_connection():
    try:
        if 'database' not in DB_CONFIG:
            DB_CONFIG['database'] = DB_NAME
        cnx = mysql.connector.connect(**DB_CONFIG)
        return cnx
    except mysql.connector.Error as err:
        print(f"Database connection failed: {err}")
        return None

def get_all_products():
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products ORDER BY id DESC")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products

def get_product_by_id(product_id):
    conn = get_db_connection()
    if not conn: return None
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    cursor.close()
    conn.close()
    return product

def add_product(name, quantity, price):
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    image_url = '/static/images/pup_logo.png'
    description = 'Newly added item.'
    try:
        cursor.execute(
            "INSERT INTO products (name, stock, price, image_url, description) VALUES (%s, %s, %s, %s, %s)",
            (name, quantity, price, image_url, description)
        )
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Failed to add product: {err}")
        return False
    finally:
        cursor.close()
        conn.close()

def update_product(product_id, name, quantity, price):
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE products SET name = %s, stock = %s, price = %s WHERE id = %s",
            (name, quantity, price, product_id)
        )
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Failed to update product: {err}")
        return False
    finally:
        cursor.close()
        conn.close()

def delete_product(product_id):
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Failed to delete product: {err}")
        return False
    finally:
        cursor.close()
        conn.close()

def create_user(name, email, password):
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    hashed_pw = hash_password(password)
    try:
        cursor.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)",
            (name, email, hashed_pw)
        )
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error creating user: {err}")
        return False
    finally:
        cursor.close()
        conn.close()
