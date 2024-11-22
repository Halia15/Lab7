import psycopg2
from psycopg2.extras import execute_values
from prettytable import PrettyTable

# Параметри підключення
conn = psycopg2.connect(
    dbname="haliadb", user="user", password="password", host="localhost", port="5432"
)

cursor = conn.cursor()


# Створення таблиць
def create_tables():
   cursor.execute("""
    CREATE TABLE IF NOT EXISTS warehouses (
        warehouse_id SERIAL PRIMARY KEY,
        address TEXT NOT NULL,
        manager TEXT NOT NULL,
        phone VARCHAR(15) CHECK (phone ~ '^\+?\d{10,15}$') NOT NULL
    );

    CREATE TABLE IF NOT EXISTS products (
        product_id SERIAL PRIMARY KEY,
        type VARCHAR(10) CHECK (type IN ('женский', 'мужской', 'детский')) NOT NULL,
        name TEXT NOT NULL,
        manufacturer TEXT NOT NULL,
        warehouse_id INTEGER REFERENCES warehouses(warehouse_id),
        stock_quantity INTEGER NOT NULL,
        price DECIMAL(10, 2) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS clients (
        client_id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        address TEXT NOT NULL,
        phone VARCHAR(15) CHECK (phone ~ '^\+?\d{10,15}$') NOT NULL,
        contact_person TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS sales (
        sale_id SERIAL PRIMARY KEY,
        sale_date DATE NOT NULL,
        client_id INTEGER REFERENCES clients(client_id),
        product_id INTEGER REFERENCES products(product_id),
        quantity INTEGER NOT NULL,
        discount DECIMAL(5, 2) DEFAULT 0.0 NOT NULL
    );
    """)
   conn.commit()


def insert_data():
    cursor.execute("INSERT INTO warehouses (address, manager, phone) VALUES (%s, %s, %s)", ('Київ, вул. 1', 'Іванов Іван', '+380501234567'))
    cursor.execute("INSERT INTO warehouses (address, manager, phone) VALUES (%s, %s, %s)", ('Львів, вул. 2', 'Петров Петро', '+380682345678'))
    cursor.execute("INSERT INTO warehouses (address, manager, phone) VALUES (%s, %s, %s)", ('Одеса, вул. 3', 'Сидоров Сидір', '+380933456789'))

    cursor.execute("INSERT INTO products (type, name, manufacturer, warehouse_id, stock_quantity, price) VALUES (%s, %s, %s, %s, %s, %s)",
                   ('женский', 'Топ', 'Brand A', 1, 100, 199.99))
    cursor.execute("INSERT INTO products (type, name, manufacturer, warehouse_id, stock_quantity, price) VALUES (%s, %s, %s, %s, %s, %s)",
                   ('мужской', 'Футболка', 'Brand B', 2, 150, 299.99))

    cursor.execute("INSERT INTO clients (name, address, phone, contact_person) VALUES (%s, %s, %s, %s)",
                   ('Клієнт 1', 'Київ, вул. 5', '+380681234567', 'Петро Петров'))
    cursor.execute("INSERT INTO clients (name, address, phone, contact_person) VALUES (%s, %s, %s, %s)",
                   ('Клієнт 2', 'Львів, вул. 6', '+380683456789', 'Ірина Іванова'))

    cursor.execute("INSERT INTO sales (sale_date, client_id, product_id, quantity, discount) VALUES (%s, %s, %s, %s, %s)",
                   ('2024-11-17', 1, 1, 2, 5.0))
    cursor.execute("INSERT INTO sales (sale_date, client_id, product_id, quantity, discount) VALUES (%s, %s, %s, %s, %s)",
                   ('2024-11-18', 2, 2, 1, 10.0))

    # Фіксація змін
    conn.commit()


def print_table(description, rows):
    table = PrettyTable()
    table.field_names = [desc[0] for desc in description]
    for row in rows:
        table.add_row(row)
    print(table)


def print_all_tables():
    tables = ["warehouses", "products", "clients", "sales"]

    for i in tables:
        cursor.execute(f"""SELECT * FROM {i}""")
        print(f"Таблиця {i}")
        print(print_table(cursor.description, cursor.fetchall()))
