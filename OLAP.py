import mysql.connector
import main
import datetime

orders_menu = '''
    You have selected OLAP.
    Please select a menu option:
        0 Return
        1 Total Sales from Date Range.
        2 Raking item category by sales from Date Range.
        3 Raking item category by quantity from Date Range.
        4 Total discount from Date Range.
        5 Employee checkouts from Date Range. 
        6 Get Customer Retention from Date Range.
'''

def handle_OLAP_menu_option():
    user_input = input(orders_menu)
    is_valid_input = False
    while not is_valid_input:
        is_valid_input = True
        if user_input == "0":
            return
        elif user_input == "1": 
            get_total_sales_date_range()
        elif user_input == "2": 
            get_rank_prod_cat_sold_date_range()
        elif user_input == "3": 
            get_rank_prod_cat_qty_date_range()
        elif user_input == "4": 
            get_total_discount_date_range()
        elif user_input == "5": 
            get_employee_checkout_date_range()
        elif user_input == "6": 
            get_customer_retention_date_range()
        elif user_input == "0": #exit
            break
        else:
            print("Please enter a valid option")
            is_valid_input = False

import datetime

def get_valid_date(prompt):
    while True:
        date_str = input(prompt)
        try:
            date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
            return date_obj.date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD format.")

def get_total_sales_date_range():
    # Get date_from and date_to inputs
    date_from = get_valid_date("Enter the start date (YYYY-MM-DD): ")
    date_to = get_valid_date("Enter the end date (YYYY-MM-DD): ")

    # Extend the end date to the end of the day
    date_to_end_of_day = datetime.datetime.combine(date_to, datetime.time(23, 59, 59))

    cursor = main.mydb.cursor(prepared=True)
    stmt = """
        SELECT 
            YEAR(date_time) AS year, 
            MONTH(date_time) AS month, 
            DAY(date_time) AS day, 
            SUM(quantity * price) AS 'Total Sales'
        FROM 
            ORDERS 
            NATURAL JOIN ORDER_PRODUCT 
            NATURAL JOIN PRODUCT
        WHERE 
            date_time BETWEEN %s AND %s
        GROUP BY 
            year, month, day
        ORDER BY 
            year, month, day
        """
    cursor.execute(stmt, [date_from, date_to_end_of_day])
    results = cursor.fetchall()
    if results:
        main.print_with_formating(cursor.description, results)
        return results
    return None

def get_rank_prod_cat_sold_date_range():
    # Get date_from and date_to inputs
    date_from = get_valid_date("Enter the start date (YYYY-MM-DD): ")
    date_to = get_valid_date("Enter the end date (YYYY-MM-DD): ")

    # Extend the end date to the end of the day
    date_to_end_of_day = datetime.datetime.combine(date_to, datetime.time(23, 59, 59))

    cursor = main.mydb.cursor(prepared=True)
    stmt = """
        SELECT
            YEAR(ORDERS.date_time) AS year, 
            MONTH(ORDERS.date_time) AS month, 
            DAY(ORDERS.date_time) AS day,
            COALESCE(category, 'ALL') AS product_category,
            COALESCE(product_name, 'ALL') AS product_name, 
            SUM(quantity*price) AS PRODUCT_TOTAL_SALES_AMOUNT 
        FROM ORDERS
        JOIN ORDER_PRODUCT ON ORDERS.order_id = ORDER_PRODUCT.order_id
        JOIN PRODUCT ON ORDER_PRODUCT.product_id = PRODUCT.product_id
        WHERE date_time BETWEEN %s AND %s
        GROUP BY year, month, day, category, product_name 
        WITH ROLLUP
        HAVING year IS NOT NULL AND month IS NOT NULL AND day IS NOT NULL;
        """
    cursor.execute(stmt, [date_from, date_to_end_of_day])
    results = cursor.fetchall()
    if results:
        main.print_with_formating(cursor.description, results)
        return results
    return None

def get_rank_prod_cat_qty_date_range():
    # Get date_from and date_to inputs
    date_from = get_valid_date("Enter the start date (YYYY-MM-DD): ")
    date_to = get_valid_date("Enter the end date (YYYY-MM-DD): ")

    # Extend the end date to the end of the day
    date_to_end_of_day = datetime.datetime.combine(date_to, datetime.time(23, 59, 59))

    cursor = main.mydb.cursor(prepared=True)
    stmt = """
        SELECT
            YEAR(ORDERS.date_time) AS year, 
            MONTH(ORDERS.date_time) AS month, 
            DAY(ORDERS.date_time) AS day,
            COALESCE(category, 'ALL') AS product_category,
            COALESCE(product_name, 'ALL') AS product_name, 
            SUM(ORDER_PRODUCT.quantity) AS PRODUCT_TOTAL_QUANTITY
        FROM ORDERS
        JOIN ORDER_PRODUCT ON ORDERS.order_id = ORDER_PRODUCT.order_id
        JOIN PRODUCT ON ORDER_PRODUCT.product_id = PRODUCT.product_id
        WHERE date_time BETWEEN %s AND %s
        GROUP BY year, month, day, category, product_name 
        WITH ROLLUP
        HAVING year IS NOT NULL AND month IS NOT NULL AND day IS NOT NULL;
        """
    cursor.execute(stmt, [date_from, date_to_end_of_day])
    results = cursor.fetchall()
    if results:
        main.print_with_formating(cursor.description, results)
        return results
    return None

def get_total_discount_date_range():
    # Get date_from and date_to inputs
    date_from = get_valid_date("Enter the start date (YYYY-MM-DD): ")
    date_to = get_valid_date("Enter the end date (YYYY-MM-DD): ")

    # Extend the end date to the end of the day
    date_to_end_of_day = datetime.datetime.combine(date_to, datetime.time(23, 59, 59))

    cursor = main.mydb.cursor(prepared=True)
    stmt = """
        SELECT
            YEAR(ORDERS.date_time) AS year, 
            MONTH(ORDERS.date_time) AS month, 
            DAY(ORDERS.date_time) AS day,
            SUM(discount_amount) as total_discount_amount
        FROM orders NATURAL JOIN discount
        WHERE date_time BETWEEN %s AND %s
        GROUP BY year, month, day
        """
    cursor.execute(stmt, [date_from, date_to_end_of_day])
    results = cursor.fetchall()
    if results:
        main.print_with_formating(cursor.description, results)
        return results
    return None
    
def get_employee_checkout_date_range():
    # Get date_from and date_to inputs
    date_from = get_valid_date("Enter the start date (YYYY-MM-DD): ")
    date_to = get_valid_date("Enter the end date (YYYY-MM-DD): ")

    # Extend the end date to the end of the day
    date_to_end_of_day = datetime.datetime.combine(date_to, datetime.time(23, 59, 59))

    cursor = main.mydb.cursor(prepared=True)
    stmt = """
        SELECT 
            employee_id, 
            name_first_name, 
            name_last_name, 
            employee_no_orders AS "Order checkouts",
            RANK() OVER (ORDER BY Employee_No_Orders DESC) AS "Employee Rank" 
        FROM (
            SELECT 
                employee_id, 
                COUNT(*) AS Employee_No_Orders 
            FROM 
                ORDERS 
            WHERE 
                date_time BETWEEN %s AND %s
            GROUP BY 
                employee_id
        ) t1 
        NATURAL JOIN EMPLOYEE;
        """
    cursor.execute(stmt, [date_from, date_to_end_of_day])
    results = cursor.fetchall()
    if results:
        main.print_with_formating(cursor.description, results)
        return results
    return None

def get_customer_retention_date_range():
    # Get date_from and date_to inputs
    date_from = get_valid_date("Enter the start date (YYYY-MM-DD): ")
    date_to = get_valid_date("Enter the end date (YYYY-MM-DD): ")

    # Extend the end date to the end of the day
    date_to_end_of_day = datetime.datetime.combine(date_to, datetime.time(23, 59, 59))

    cursor = main.mydb.cursor(prepared=True)
    stmt = """
        WITH FirstOrderDate AS (
            SELECT 
                customer_id, 
                MIN(date_time) AS first_order_date
            FROM orders
            GROUP BY customer_id
        )
        SELECT
            o.customer_id,
            o.order_id,
            DATE(o.date_time) AS order_date,
            CASE 
                WHEN DATE(o.date_time) = DATE(f.first_order_date) THEN 'NEW' 
                ELSE 'OLD' 
            END AS retention
        FROM orders o
        JOIN FirstOrderDate f ON o.customer_id = f.customer_id
        WHERE o.date_time BETWEEN %s AND %s
          AND o.customer_id IS NOT NULL
        ORDER BY order_date ASC;
        """
    cursor.execute(stmt, [date_from, date_to_end_of_day])
    results = cursor.fetchall()
    if results:
        main.print_with_formating(cursor.description, results)
        return results
    return None