import main
customer_menu = '''
    You have selected Customers. 
    Please select a menu option:
        0 Return
        1 View Customers
        2 Add Customer
        3 Edit Customer
        4 Delete Customer
'''

def handle_customer_menu_option():
    user_input = input(customer_menu)
    is_valid_input = False
    while not is_valid_input:
        is_valid_input = True
        if user_input == "1": #view
            get_customers()
        elif user_input == "2": #add
            add_customer()
        elif user_input == "3": #edit
            edit_customer()
        elif user_input == "4": #delete
            delete_customer()
        else:
            is_valid_input = False

def get_customer_by_id(customer_id):
    cursor = main.mydb.cursor(prepared=True)
    stmt = "SELECT * FROM Customer WHERE customer_id = %s"
    cursor.execute(stmt, [customer_id])
    result = cursor.fetchall()
    if result:
        main.print_with_formating(cursor.description, result)
    return result

def get_customers():
    cursor = main.mydb.cursor(prepared=True)
    cursor.execute("SELECT * FROM CUSTOMER")
    result = cursor.fetchall()
    main.print_with_formating(cursor.description, result)
    return result

def add_customer():
    # first name, last name, email, loyalty points, phone numbers
    name_first_name = input("Please enter the First Name of the customer")
    name_last_name = input("Please enter the Last Name of the customer")
    email = input("Please enter the email of the customer")
    loyalty_points = input("Please enter the number of loyalty points the customer has")
    phone_number = input("Please enter the phone number of the customer")
    # TO DO: add validation for email, loyalty_points, phone_number
    print("The customer you want to add has the following details",
          "\nFirst Name: ", name_first_name,
          "\nLast Name: ", name_last_name,
          "\nEmail: ", email,
          "\nLoyalty Points", loyalty_points,
          "\nPhone number", phone_number)
    confirm_input = input("Please enter 'y' to confirm action and 'n' to cancel action")
    if confirm_input == 'n':
        return
    else:
        cursor = main.mydb.cursor(prepared=True)
        stmt = "INSERT INTO Customer values(%s, %s, %s, %s, %s, %s)"
        tuple = (0, name_first_name, name_last_name, email, loyalty_points, phone_number)
        cursor.execute(stmt, tuple)
        main.mydb.commit()
        print("Customer added. Here is the updated Customer table")
        get_customers()

def edit_customer():
    is_valid_input = False
    while not is_valid_input:
        customer_id = input("Please input the ID of the customer you want to delete. Press q to return")
        if customer_id == "q":
            return
        else:
            try:
                customer_id = int(customer_id)
                is_valid_input = True
                customer = get_customer_by_id(customer_id)
                print(customer)
                if not customer:
                    print ("No such Customer")
                else:
                    name_first_name = input("Please enter the First Name of the customer or NA if you do not want to edit this field")
                    name_last_name = input("Please enter the Last Name of the customer  or NA if you do not want to edit this field")
                    email = input("Please enter the email of the customer  or NA if you do not want to edit this field")
                    loyalty_points = input("Please enter the number of loyalty points the customer or NA if you do not want to edit this field")
                    phone_number = input("Please enter the phone number of the customer  or NA if you do not want to edit this field")
                    print("The customer you want to edit has the following details",
                          "\nCustomer ID: ", customer_id,
                          "\nFirst Name: ", name_first_name,
                          "\nLast Name: ", name_last_name,
                          "\nEmail: ", email,
                          "\nLoyalty Points", loyalty_points,
                          "\nPhone number", phone_number)
                    confirm_input = input("Please enter 'y' to confirm action and 'n' to cancel action")
                    if confirm_input == 'n':
                        return
                    else:
                        cursor = main.mydb.cursor(prepared=True)
                        stmt = "UPDATE Customer SET "  # WHERE customer_id = %s
                        tuple = []
                        if name_first_name.upper() != "NA":
                            stmt = stmt + "name_first_name = %s"
                            tuple.append(name_first_name)
                        if name_last_name.upper() != "NA":
                            if len(tuple) > 0:
                                stmt = stmt + ", "
                            stmt = stmt + "name_last_name = %s"
                            tuple.append(name_last_name)
                        if email.upper() != "NA":
                            if len(tuple) > 0:
                                stmt = stmt + ", "
                            stmt = stmt + "email = %s"
                            tuple.append(email)
                        if loyalty_points.upper() != "NA":
                            if len(tuple) > 0:
                                stmt = stmt + ", "
                            stmt = stmt + "loyalty_points = %s"
                            tuple.append(email)
                        if phone_number.upper() != "NA":
                            if len(tuple) > 0:
                                stmt = stmt + ", "
                            stmt = stmt + "phone_number = %s"
                            tuple.append(phone_number)
                        if len(tuple) == 0:
                            print("No fields updated to this customer.")
                        else:
                            stmt = stmt + " WHERE CUSTOMER_ID = %s"
                            tuple.append(customer_id)
                            print(stmt, tuple)
                            cursor.execute(stmt, tuple)
                            main.mydb.commit()
                            print("Customer", customer_id, "edited. Here is the updated Customer")
                            get_customer_by_id(customer_id)
            except ValueError:
                print("Please enter an integer")

def delete_customer():
    is_valid_input = False
    while not is_valid_input:
        customer_id = input("Please input the ID of the customer you want to delete. Press q to return")
        if customer_id == "q":
            is_valid_input = True
            return
        else:
            try:
                customer_id = int(customer_id)
                is_valid_input = True
                cursor = main.mydb.cursor(prepared=True)
                stmt = "DELETE FROM Customer WHERE customer_id = %s"
                cursor.execute(stmt, customer_id)
                main.mydb.commit()
                print("Customer", customer_id, "deleted. Here is the updated Customer table")
                get_customers()
            except ValueError:
                print("Please enter an integer")