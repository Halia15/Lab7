from db import print_table, cursor


def query_1():
    cursor.execute(
        """SELECT s.sale_date, p.name AS product_name, c.name AS client_name, s.quantity, p.price
FROM sales s
JOIN products p ON s.product_id = p.product_id
JOIN clients c ON s.client_id = c.client_id
ORDER BY c.name;
"""
    )
    print_table(cursor.description, cursor.fetchall())


def query_2(source):
    cursor.execute(
        """SELECT * FROM products WHERE type = %s;
"""
    , ((source,)))
    print_table(cursor.description, cursor.fetchall())


def query_3():
    cursor.execute(
        """
SELECT c.name, COUNT(s.sale_id) AS purchase_count
FROM clients c
LEFT JOIN sales s ON c.client_id = s.client_id
GROUP BY c.name;


                   """
    )
    print_table(cursor.description, cursor.fetchall())


def query_4():
    cursor.execute(
        f"""
    SELECT s.sale_id, p.name, s.quantity, p.price,
       (s.quantity * p.price) AS total_price_without_discount,
       (s.quantity * p.price * (1 - s.discount / 100)) AS total_price_with_discount
FROM sales s
JOIN products p ON s.product_id = p.product_id;


"""
    )

    print_table(cursor.description, cursor.fetchall())


def query_5():
    cursor.execute(
        """
SELECT c.name, SUM(s.quantity * p.price * (1 - s.discount / 100)) AS total_spent
FROM clients c
JOIN sales s ON c.client_id = s.client_id
JOIN products p ON s.product_id = p.product_id
GROUP BY c.name;


"""
    )
    print_table(cursor.description, cursor.fetchall())


def query_6():
    cursor.execute(
        """
    SELECT w.address, p.type, SUM(p.stock_quantity)
FROM products p
JOIN warehouses w ON p.warehouse_id = w.warehouse_id
GROUP BY w.address, p.type;


"""
    )

    print_table(cursor.description, cursor.fetchall())
