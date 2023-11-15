import sys
import mysql.connector
from tabulate import tabulate

import Customers
import Products
import discount
import db
import employee_dao
import Orders
import OLAP

mydb = mysql.connector.connect(
        host=db.host,
        user=db.user,
        password=db.password,

        database=db.database
)
main_menu = '''
    Welcome to CS425 POS System. 
    Please select a menu option:
        0 Exit Program
        1 Orders
        2 Customers
        3 Discounts
        4 Employees
        5 Products
        6 OLAP
'''

def handle_main_menu_option(menu_option):
    if menu_option == "1":  # orders
        Orders.handle_order_menu_option()
    elif menu_option == "2":  # customers
        Customers.handle_customer_menu_option()
    elif menu_option == "3":  # discounts
        discount.handle_discount_menu_option()
    elif menu_option == "4":  # employee
        employee_dao.handle_employee_menu_option()
    elif menu_option == "5":  # products
        Products.handle_product_menu_option()
    elif menu_option == "6": # OLAP
        OLAP.handle_OLAP_menu_option()
    else:
        print("Please enter a valid option")


def print_with_formating(description, result):
    header_names = [i[0] for i in description]
    print(tabulate(result, headers=header_names))


if __name__ == '__main__':
    should_run = True
    while should_run:
        user_input = input(main_menu)
        if user_input == "0":
            print("Good bye!")
            should_run = False
            sys.exit()
        handle_main_menu_option(user_input)
