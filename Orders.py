import mysql.connector
import main
import datetime
import Customers as cust

orders_menu = '''
    You have selected Orders.
    Please select a menu option:
        0 Return
        1 View Orders
        2 Add an Order
        3 Edit an Order
        4 Delete an Order
'''

def handle_order_menu_option():
    user_input = input(orders_menu)
    is_valid_input = False
    while not is_valid_input:
        is_valid_input = True
        if user_input == "1": #view
            get_orders()
        elif user_input == "2": #add
            create_order()
        elif user_input == "3": #edit
            edit_order()
        elif user_input == "4": #delete
            delete_order()
        elif user_input == "0": #exit
            break
        else:
            print("Please enter a valid option")
            is_valid_input = False

def get_customer_id_by_phone(phone_number):
    cursor = main.mydb.cursor(prepared=True)
    stmt = "SELECT customer_id FROM Customer WHERE phone_number = %s"
    cursor.execute(stmt, [phone_number])
    result = cursor.fetchone()
    if result:
        main.print_with_formating(cursor.description, [result])
        return result[0]
    return None

def get_customer_id_latest():
    cursor = main.mydb.cursor(prepared=True)
    stmt = "SELECT customer_id FROM Customer ORDER BY customer_id DESC LIMIT 1"
    cursor.execute(stmt)
    result = cursor.fetchone()
    if result:
        main.print_with_formating(cursor.description, [result])
        return result[0]
    return None

def get_discount_id(discount_id):
    cursor = main.mydb.cursor(prepared=True)
    stmt = "SELECT discount_id FROM Discount WHERE discount_id = %s"
    cursor.execute(stmt, [discount_id])
    result = cursor.fetchone()
    if result:
        main.print_with_formating(cursor.description, [result])
        return result[0]
    return None

def get_employee_id(employee_id):
    cursor = main.mydb.cursor(prepared=True)
    stmt = "SELECT employee_id FROM Employee WHERE employee_id = %s"
    cursor.execute(stmt, [employee_id])
    result = cursor.fetchone()
    if result:
        main.print_with_formating(cursor.description, [result])
        return result[0]
    return None

def get_order_by_id(order_id):
    cursor = main.mydb.cursor(prepared=True)
    stmt = "SELECT * FROM Orders WHERE order_id = %s"
    cursor.execute(stmt, [order_id])
    result = cursor.fetchone()
    if result:
        main.print_with_formating(cursor.description, [result])
    return result

def get_orders():
    cursor = main.mydb.cursor(prepared=True)
    cursor.execute("SELECT * FROM Orders")
    result = cursor.fetchall()
    main.print_with_formating(cursor.description, result)
    return result

def get_latest_order():
    cursor = main.mydb.cursor(prepared=True)
    stmt = "SELECT * FROM Orders ORDER BY order_id DESC LIMIT 1"
    cursor.execute(stmt)
    result = cursor.fetchone()
    if result:
        main.print_with_formating(cursor.description, [result])
    return result

def get_valid_employee_id():
    while True:
        employee_id = input("Please enter the employee ID (or type (q) to skip): ")
        if employee_id.upper() == 'Q':
            return None
        valid_employee_id = get_employee_id(employee_id)
        if valid_employee_id:
            return valid_employee_id
        else:
            print("No employee found with the given ID. Please try again.")

def get_valid_customer_id_by_phone():
    while True:
        cust_phone_number = input("Please enter the customer's phone number [10-digits NO DASH '-'] (or type (q) to skip): ")
        if cust_phone_number.upper() == 'Q':
            return None
        valid_customer_id = get_customer_id_by_phone(cust_phone_number)
        if valid_customer_id:
            return valid_customer_id
        else:
            print("No customer found with this phone number. Please enter again.")

def get_valid_discount_id():
    while True:
        discount_id = input("Please enter the discount ID (or type (q) to skip): ")
        if discount_id.upper() == 'Q':
            return None
        valid_discount_id = get_discount_id(discount_id)
        if valid_discount_id:
            return valid_discount_id
        else:
            print("No discount found with the given ID. Please enter again.")

def create_order():
    #order_id, date_time, customer_id, discount_id, *employee_id*

    # Ask for employee_id.
    while True:
        employee_id = get_valid_employee_id()
        if employee_id:
            break
        elif employee_id is None:
            print(">>>Unskippable value! Abort adding order!")
            return
        
    # Attach or skip customer.
    while True:
        attach_cust = input("Will you attach a CUSTOMER to this order? (y/n): ")
        
        if attach_cust.upper() == 'Y':
            while True:
                new_or_existing = input("Are they a NEW customer? (y/n): ")

                if new_or_existing.upper() == 'Y':
                    # add customer can be ABORTED. Need to check if they actually added a new cust
                    print(">>>Latest customer BEFORE adding");
                    prev_last_customer = get_customer_id_latest()
                    cust.add_customer()
                    print(">>>Latest customer AFTER adding");
                    curr_last_customer = get_customer_id_latest()

                    if prev_last_customer == curr_last_customer:
                        print(">>>No customer was added. Abort attaching customer.")
                        customer_id = None
                    else:
                        customer_id = curr_last_customer
                    break
                elif new_or_existing.upper() == 'N':
                    customer_id = get_valid_customer_id_by_phone()
                    if customer_id:
                        break
                    elif customer_id is None:
                        break
                else:
                    print(">>>New/Existing customer Invalid input! Please enter (y) for NEW or (n) for EXISITNG customer.")
            break

        elif attach_cust.upper() == 'N':
            customer_id = None
            break
        else:
            print(">>>Attach customer Invalid input! Please enter (y) to attach a customer or (n) not to.")

    # Attach or skip discount.
    while True:
        attach_disc = input("Will you attach a DISCOUNT to this order? (y/n): ")
        if attach_disc.upper() == 'Y':
            discount_id = get_valid_discount_id()
            if discount_id:
                break
            elif discount_id is None:
                break
        elif attach_disc.upper() == 'N':
            discount_id = None
            break
        else:
            print(">>>Attach discount Invalid input! Please enter (y) or (n).")

    # Get current date_time with the SQL format.
    date_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    print("The order you want to add has the following details",
          "\n\tDate Time: ", date_time,
          "\n\tCustomer Id: ", customer_id,
          "\n\tDiscount Id: ", discount_id,
          "\n\tEmployee Id: ", employee_id)
    confirm_input = input("Please enter (y) to confirm action or (n) to cancel action: ")
    if confirm_input.upper() == 'N':
        print(">>>Abort adding Order!")
        return
    else:
        cursor = main.mydb.cursor(prepared=True)
        stmt = "INSERT INTO Orders (date_time, customer_id, discount_id, employee_id) values(%s, %s, %s, %s)"
        order_tuple = (date_time, customer_id, discount_id, employee_id)
        cursor.execute(stmt, order_tuple)
        main.mydb.commit()
        print(">>>Order added. Here is the order detail")
        get_latest_order()

def edit_order():
    is_valid_input = False
    while not is_valid_input:
        order_id = input("Please input the ID of the order you want to edit. Press (q) to return: ")
        if order_id.upper() == "Q":
            is_valid_input = True
            return
        else:
            try:
                order_id = int(order_id)
                is_valid_input = True
                order = get_order_by_id(order_id)
                if not order:
                    print (">>>No such order.")
                else:
                    print ("The order details: ",order)
                    
                    # date_time shouldn't be editable at all.

                    employee_id = get_valid_employee_id()
                    customer_id = get_valid_customer_id_by_phone()
                    discount_id = get_valid_discount_id()

                    print("The order you want to edit has the following details",
                        "\n\tCustomer Id: ", customer_id,
                        "\n\tDiscount Id: ", discount_id,
                        "\n\tEmployee Id: ", employee_id)

                    confirm_input = input("Please enter (y) to confirm action and (n) to cancel action: ")
                    if confirm_input.upper() == 'N':
                        print(">>>Abort editing Order!")
                        return
                    else:
                        cursor = main.mydb.cursor(prepared=True)
                        stmt = "UPDATE Orders SET "
                        tuple = []

                        if customer_id != None:
                            stmt += "customer_id = %s, "
                            tuple.append(customer_id)
                        
                        if discount_id != None:
                            stmt += "discount_id = %s, "
                            tuple.append(discount_id)
                        
                        if employee_id != None:
                            stmt += "employee_id = %s, "
                            tuple.append(employee_id)

                        if len(tuple) == 0:
                            print(">>>No fields updated to this order.")
                        else:
                            stmt = stmt.rstrip(', ') + " WHERE order_id = %s"
                            tuple.append(order_id)
                            cursor.execute(stmt, tuple)
                            main.mydb.commit()
                            print(">>>Order ", order_id, " edited. Here is the updated Order:")
                            get_order_by_id(order_id)

            except ValueError:
                print(">>>Please enter an integer")

def delete_order():
    is_valid_input = False
    while not is_valid_input:
        order_id = input("Please input the ID of the order you want to delete. Press (q) to return: ")
        if order_id.upper() == "Q":
            is_valid_input = True
            return
        else:
            try:
                order_id = int(order_id)
                order = get_order_by_id(order_id)
                if not order:
                    print (">>>No such order.")
                else:
                    is_valid_input = True
                    # Delete order
                    cursor = main.mydb.cursor(prepared=True)
                    delete_stmt = "DELETE FROM Orders WHERE order_id = %s"
                    cursor.execute(delete_stmt, [order_id])
                    main.mydb.commit()

                    # Check rows affected after deletion
                    if cursor.rowcount:
                        print(f">>>Order {order_id} deleted.")
                    else:
                        print(f">>>Failed to delete order {order_id}.")
                        
            except ValueError:
                print(">>>Please enter a valid integer for the order ID.")
            except Exception as e:
                print(f">>>An error occurred: {e}")
