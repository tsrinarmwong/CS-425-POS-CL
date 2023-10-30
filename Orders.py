import main
import date_time
import Customers as cust

orders_menu = '''
    You have selected Orders. 
    Please select a menu option:
        0 Return
        1 Create an Order
        2 View Orders
        3 Edit an Order
        4 Delete an Order
'''

def handle_customer_menu_option():
    user_input = input(orders_menu)
    is_valid_input = False
    while not is_valid_input:
        is_valid_input = True
        if user_input == "1": #Create
            create_order()
        elif user_input == "2": #Read
            get_orders()
        elif user_input == "3": #Update
            edit_order()
        elif user_input == "4": #Delete
            delete_order()
        else:
            is_valid_input = False

def get_customer_id_by_phone(phone_number):
    cursor = main.mydb.cursor(prepared=True)
    stmt = "SELECT customer_id FROM Customer WHERE phone_number = %s"
    cursor.execute(stmt, [phone_number])
    result = cursor.fetchall()
    if result:
        main.print_with_formating(cursor.description, result)
    return result

def get_customer_id_latest():
    cursor = main.mydb.cursor(prepared=True)
    stmt = "SELECT customer_id FROM Customer ORDER BY customer_id DESC LIMIT 1"
    cursor.execute(stmt, [customer_id])
    result = cursor.fetchall()
    if result:
        main.print_with_formating(cursor.description, result)
    return result

def get_discount_id(discount_id):
    cursor = main.mydb.cursor(prepared=True)
    stmt = "SELECT discount_id FROM Discount WHERE discount_id = %s"
    cursor.execute(stmt, [discount_id])
    result = cursor.fetchall()
    if result:
        main.print_with_formating(cursor.description, result)
    return result

def get_employee_id(employee_id):
    cursor = main.mydb.cursor(prepared=True)
    stmt = "SELECT employee_id FROM Employee WHERE employee_id = %s"
    cursor.execute(stmt, [employee_id])
    result = cursor.fetchall()
    if result:
        main.print_with_formating(cursor.description, result)
    return result

def get_order_by_id(order_id):
    cursor = main.mydb.cursor(prepared=True)
    stmt = "SELECT * FROM Orders WHERE order_id = %s"
    cursor.execute(stmt, [order_id])
    result = cursor.fetchall()
    if result:
        main.print_with_formating(cursor.description, result)
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
    cursor.execute(stmt, [customer_id])
    result = cursor.fetchall()
    if result:
        main.print_with_formating(cursor.description, result)
    return result

def create_order():
    #order_id, date_time, customer_id, discount_id, *employee_id*

    # Ask for employee_id.
    # Unskippable! If they got it wrong, just restart right away.
    employee_id = input("Please enter the employee ID: ")
    valid_employee_id = get_employee_id(employee_id)
        if valid_employee_id:
            employee_id = valid_employee_id
        else:
            print("No employee found with the given ID.")
            return
    
    # Ask if customer_id will be attached?    
    attach_cust =  input("Will you attach a customer to this order? (y/n): ")
    
    if attach_cust.upper() == 'Y':
        # If attached, is it a new customer?
        new_or_existing = input("Are they a new customer? (y/n): ")
        
        # New customer case
        if new_or_existing.upper() == 'Y':        
            cust.add_customer()
            customer_id = get_customer_id_latest()
        
        # Existing customer case    
        elif new_or_existing.upper() == 'N':
            # if the phone number is not found, give them chance to try again. or skip with q
            while True:
                cust_phone_number = input("Please enter the customer's phone number(or type (q) to skip): ")
                
                # Quit attach customer
                if cust_phone_number.upper() == 'Q':
                    customer_id = None 
                    break
                else:
                    valid_customer_id = get_customer_id_by_phone(cust_phone_number):
                    if valid_customer_id:
                        customer_id = valid_customer_id
                        break
                    else:
                        print("No customer found with this phone number. Please enter again.")
        else:
            print("New or Existing invalid input! Please enter (y) or (n).")
    
    # No attached case
    elif attach_cust.upper() == 'N':
        customer_id = None        
    else:
        print("Attach Customer invalid input! Please enter (y) or (n).")        

    attach_disc =  input("Will you attach a discount to this order? (y/n): ")
    
    if attach_disc.upper() == 'Y':
        # If attached
        while True:
            discount_id = input("Please enter the discount ID(or type (q) to skip): ")

            # Quit attach discount
            if discount_id.upper() == 'Q':
                discount_id = None 
                break
            else:
                valid_discount_id = get_discount_id(discount_id):
                    if valid_discount_id:
                        discount_id = valid_discount_id
                        break
                    else:
                        print("No discount found with the given ID. Please enter again.")
    # No attached case
    elif attach_disc.upper() == 'N':
        discount_id = None        
    else:
        print("Attach Discount invalid input! Please enter (y) or (n).")

    # Get current date_time with the SQL format
    date_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    print("The order you want to add has the following details",
          "\nDate Time: ", date_time,
          "\nCustomer Id: ", customer_id,
          "\nDiscount Id: ", discount_id,
          "\nEmployee Id: ", employee_id)
    confirm_input = input("Please enter (y) to confirm action or (n) to cancel action")
    if confirm_input.upper() == 'N':
        return
    else:
        cursor = main.mydb.cursor(prepared=True)

        # Will hard setting '0' to the order_id cause it to not AUTO INCREMENT? 
        # I'll just add only on fields imputted then.
        stmt = "INSERT INTO Orders (date_time, customer_id, discount_id, employee_id) values(%s, %s, %s, %s)"
        tuple = (date_time, customer_id, discount_id, employee_id)
        cursor.execute(stmt, tuple)
        main.mydb.commit()
        print("Order added. Here is the order detail")
        get_latest_order()

def edit_order():
    is_valid_input = False
    while not is_valid_input:
        order_id = input("Please input the ID of the order you want to edit. Press (q) to return")
        if order_id.upper() == "Q":
            is_valid_input = True
            return
        else:
            try:
                order_id = int(order_id)
                is_valid_input = True
                order = get_order_by_id(order_id)
                if not order:
                    print ("No such order.")
                else:
                    print ("The order details: ",order)
                    
                    # date_time shouldn't be editable at all.

                    # Unskippable
                    while True:
                        employee_id = input("Please enter the new employee ID or (NA) if you do not want to edit this field")

                        if employee_id.upper() == "NA":
                            break
                        # Check validity
                        else:
                            valid_employee_id = get_employee_id(employee_id)
                            if valid_employee_id
                                employee_id = valid_employee_id
                                break
                            else:
                                print("No employee found with the given ID. Please enter again.")                                
                    
                    while True:
                        customer_id = input("Please enter the new customer's phone number or NA if you do not want to edit this field")
                        
                        if customer_id.upper() == "NA":
                            break
                        # Check validity
                        else:
                            valid_customer_id = get_customer_id_by_phone(customer_id)
                            if valid_customer_id:
                                customer_id = valid_customer_id
                                break
                        else:
                            print("No customer found with this phone number. Please enter again.")

                    while True:
                        discount_id = input("Please enter the new discount ID or NA if you do not want to edit this field")
                        
                        if discount_id.upper() == "NA":
                            break
                        # Check validity
                        else:
                            valid_discount_id = get_discount_id(discount_id)
                            if valid_discount_id:
                                discount_id = valid_discount_id
                                break
                        else:
                            print("No discount found with the given ID. Please enter again.")
                    
                    print("The order you want to edit has the following details",
                        "\nCustomer Id: ", customer_id,
                        "\nDiscount Id: ", discount_id,
                        "\nEmployee Id: ", employee_id)
                    confirm_input = input("Please enter (y) to confirm action and (n) to cancel action")
                    if confirm_input.upper() == 'N':
                        return
                    else:
                        cursor = main.mydb.cursor(prepared=True)
                        stmt = "UPDATE Orders SET "  # WHERE order_id = %s
                        tuple = []
                        if customer_id.upper() != "NA":
                            stmt = stmt + "customer_id = %s"
                            tuple.append(customer_id)
                        if discount_id.upper() != "NA":
                            if len(tuple) > 0:
                                stmt = stmt + ", "
                            stmt = stmt + "discount_id = %s"
                            tuple.append(discount_id)
                        if employee_id.upper() != "NA":
                            if len(tuple) > 0:
                                stmt = stmt + ", "
                            stmt = stmt + "employee_id = %s"
                            tuple.append(employee_id)
                        if len(tuple) == 0:
                            print("No fields updated to this order.")
                        else:
                            stmt = stmt + " WHERE order_id = %s"
                            tuple.append(order_id)
                            print(stmt, tuple)
                            cursor.execute(stmt, tuple)
                            main.mydb.commit()
                            print("Order ", order_id, " edited. Here is the updated Order:")
                            get_order_by_id(order_id)
            except ValueError:
                print("Please enter an integer")

def delete_order():
    is_valid_input = False
    while not is_valid_input:
        order_id = input("Please input the ID of the order you want to delete. Press (q) to return")
        if order_id.upper() == "Q":
            is_valid_input = True
            return
        else:
            try:
                order_id = int(order_id)
                is_valid_input = True
                cursor = main.mydb.cursor(prepared=True)
                stmt = "DELETE FROM Orders WHERE order_id = %s"
                cursor.execute(stmt, [order_id])
                main.mydb.commit()
                print("Order ", order_id, " deleted.")
            except ValueError:
                print("Please enter an integer")