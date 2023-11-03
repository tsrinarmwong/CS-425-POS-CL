import main
product_menu = '''
    You have selected Products. 
    Please select a menu option:
        0 Return
        1 View Products
        2 Add Product
        3 Edit Product
        4 Delete Product
'''

def handle_product_menu_option():
    user_input = input(product_menu)
    is_valid_input = False
    while not is_valid_input:
        is_valid_input = True
        if user_input == "0":
            return
        if user_input == "1": #view
            get_products()
        elif user_input == "2": #add
            add_product()
        elif user_input == "3": #edit
            edit_product()
        elif user_input == "4": #delete
            delete_product()
        else:
            is_valid_input = False

def get_product_by_id(product_id):
    cursor = main.mydb.cursor(prepared=True)
    stmt = "SELECT * FROM Product WHERE product_id = %s"
    cursor.execute(stmt, [product_id])
    result = cursor.fetchall()
    if result:
        main.print_with_formating(cursor.description, result)
    return result

def get_products():
    cursor = main.mydb.cursor(prepared=True)
    cursor.execute("SELECT * FROM Product")
    result = cursor.fetchall()
    main.print_with_formating(cursor.description, result)
    return result

def add_product():
    # category, product name, price, product description
    category = input("Please enter the category of the product")
    product_name = input("Please enter the product Name of the product")
    price = input("Please enter the price of the product")
    product_description = input("Please enter the product description of the product")
    
    # TO DO: add validation for category, product name, price, product description
    print("The product you want to add has the following details",
          "\nCategory: ", category,
          "\nProduct Name: ", product_name,
          "\nPrice: ", price,
          "\nProduct Description", product_description)
    confirm_input = input("Please enter 'y' to confirm action and 'n' to cancel action")
    if confirm_input == 'n':
        return
    else:
        cursor = main.mydb.cursor(prepared=True)
        stmt = "INSERT INTO Product values(%s, %s, %s, %s, %s)"
        tuple = (0, category, product_name, price, product_description)
        cursor.execute(stmt, tuple)
        main.mydb.commit()
        print("Product added. Here is the updated Product table")
        get_products()

def edit_product():
    is_valid_input = False
    while not is_valid_input:
        product_id = input("Please input the ID of the product you want to edit. Press q to return")
        if product_id == "q":
            return
        else:
            try:
                product_id = int(product_id)
                is_valid_input = True
                product = get_product_by_id(product_id)
                if not product:
                    print ("No such Product")
                else:
                    category = input("Please enter the Category of the product or NA if you do not want to edit this field")
                    product_name = input("Please enter the Product Name of the product or NA if you do not want to edit this field")
                    price = input("Please enter the Price of the product or NA if you do not want to edit this field")
                    product_description = input("Please enter the Product Description of the product or NA if you do not want to edit this field")
                    print("The product you want to edit has the following details",
                          "\nCustomer ID: ", product_id,
                          "\nCategory: ", category,
                          "\nProduct Name: ", product_name,
                          "\nPrice: ", price,
                          "\nProduct Description", product_description)
                    confirm_input = input("Please enter 'y' to confirm action and 'n' to cancel action")
                    if confirm_input == 'n':
                        return
                    else:
                        cursor = main.mydb.cursor(prepared=True)
                        stmt = "UPDATE Product SET "  # WHERE product_id = %s
                        tuple = []
                        if category.upper() != "NA":
                            stmt = stmt + "category = %s"
                            tuple.append(category)
                        if product_name.upper() != "NA":
                            if len(tuple) > 0:
                                stmt = stmt + ", "
                            stmt = stmt + "product_name = %s"
                            tuple.append(product_name)
                        if price.upper() != "NA":
                            if len(tuple) > 0:
                                stmt = stmt + ", "
                            stmt = stmt + "price = %s"
                            tuple.append(price)
                        if product_description.upper() != "NA":
                            if len(tuple) > 0:
                                stmt = stmt + ", "
                            stmt = stmt + "product_description = %s"
                            tuple.append(product_description)
                        if len(tuple) == 0:
                            print("No fields updated to this customer.")
                        else:
                            stmt = stmt + " WHERE Product_ID = %s"
                            tuple.append(product_id)
                            print(stmt, tuple)
                            cursor.execute(stmt, tuple)
                            main.mydb.commit()
                            print("Prodcut", product_id, "edited. Here is the updated Product")
                            get_product_by_id(product_id)
            except ValueError:
                print("Please enter an integer")

def delete_product():
    is_valid_input = False
    while not is_valid_input:
        product_id = input("Please input the ID of the product you want to delete. Press q to return")
        if product_id == "q":
            is_valid_input = True
            return
        else:
            try:
                product_id = int(product_id)
                is_valid_input = True
                cursor = main.mydb.cursor(prepared=True)
                stmt = "DELETE FROM Product WHERE product_id = %s"
                cursor.execute(stmt, [product_id])
                main.mydb.commit()
                print("Product", product_id, "deleted. Here is the updated Product table")
                get_products()
            except ValueError:
                print("Please enter an integer")