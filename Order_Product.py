import mysql.connector
import main

orders_product_menu = '''
    You have selected Orders Product.
    Please select a menu option:
        0 Return
        1 View Order Product
        2 Add Product to Order
        3 Edit Product in Order
        4 Delete Product in Order
'''

def handle_order_product_menu_option():
    user_input = input(orders_product_menu)
    is_valid_input = False
    while not is_valid_input:
        is_valid_input = True
        if user_input == "1": #view
            get_Order_Product()
        elif user_input == "2": #add
            create_Order_Product(None)
        elif user_input == "3": #edit
            edit_Order_Product()
        elif user_input == "4": #delete
            delete_Order_Product()
        elif user_input == "0": #exit
            break
        else:
            print("Please enter a valid option")
            is_valid_input = False

def get_Order_Product():
    cursor = main.mydb.cursor(prepared=True)
    cursor.execute("SELECT * FROM Order_Product")
    result = cursor.fetchall()
    main.print_with_formating(cursor.description, result)
    return result

def get_order_id(order_id):
    cursor = main.mydb.cursor(prepared=True)
    stmt = "SELECT order_id FROM Orders WHERE order_id = %s"
    cursor.execute(stmt, [order_id])
    result = cursor.fetchone()
    if result:
        main.print_with_formating(cursor.description, [result])
        return result[0]
    return None

def get_product_id(product_id):
    cursor = main.mydb.cursor(prepared=True)
    stmt = "SELECT product_id FROM Product WHERE product_id = %s"
    cursor.execute(stmt, [product_id])
    result = cursor.fetchone()
    if result:
        main.print_with_formating(cursor.description, [result])
        return result[0]
    return None

def get_Order_Product_by_id(order_id, product_id):
    cursor = main.mydb.cursor(prepared=True)
    stmt = "SELECT * FROM Order_Product WHERE order_id = %s AND product_id = %s"
    cursor.execute(stmt, (order_id, product_id))
    result = cursor.fetchone()
    
    if result:
        main.print_with_formating(cursor.description, [result])
        return result
    return None

def get_latest_Order_Product():
    cursor = main.mydb.cursor(prepared=True)
    stmt = "SELECT * FROM Order_Product ORDER BY order_id DESC LIMIT 1"
    cursor.execute(stmt)
    result = cursor.fetchone()
    if result:
        main.print_with_formating(cursor.description, [result])
    return result

def get_valid_order_id():
    while True:
        order_id = input("Please enter the order ID (or type (q) to skip): ")
        if order_id.upper() == 'Q':
            return None
        valid_order_id = get_order_id(order_id)
        if valid_order_id:
            return valid_order_id
        else:
            print("No order found with the given ID. Please try again.")

def get_valid_product_id():
    while True:
        product_id = input("Please enter the product ID (or type (q) to skip): ")
        if product_id.upper() == 'Q':
            return None
        valid_product_id = get_product_id(product_id)
        if valid_product_id:
            return valid_product_id
        else:
            print("No product found with the given ID. Please try again.")

def get_quantity_integer():
	while True:
		    try:  # Get & check integer
		        quantity = input("Please enter the product quantity amount (minimum 1): ")
		        quantity = int(quantity)
		        if quantity > 0:
		        	return quantity
		        else:
		        	print("Minimum quantity is 1.")
		    except ValueError:  
		        print("Please enter a valid integer quantity.")

def is_duplicate_Order_Product(order_id, product_id):
	Order_Product = get_Order_Product_by_id(order_id, product_id)
	return Order_Product is not None

def create_Order_Product(order_id_continue):

	# Starting from user input
	if order_id_continue is None:
		# Get & check order_id
		while True:
			order_id = get_valid_order_id()
			if order_id:
				break # Exit order ID loop
			elif order_id is None:
				print(">>>Unskippable value! Abort adding Product to Order!")
				return
	# Starting after orders created
	else:
		order_id = order_id_continue[0]
	
	# Add item loop
	while True:

		# Get & check product_id
		while True:		
			product_id = get_valid_product_id()
			if product_id:
				break # Exit product ID loop
			elif product_id is None:
				print(">>>Unskippable value! Abort adding Product to Order!")
				return
	
		if is_duplicate_Order_Product(order_id, product_id):
			print("This order and product combination already exists!")
			return
		else:
			# Ask for quantity amount
			quantity = get_quantity_integer()

			print("The Product you want to add to Orders has the following details",
				"\n\tOrder Id: ", order_id,
				"\n\tProduct Id: ", product_id,
				"\n\tQuantity: ", quantity)

			confirm_input = input("Please enter (y) to confirm action or (n) to cancel action: ")
			
			if confirm_input.upper() == 'N':
				print(">>>Abort adding Product to Order!")
				return

			# Actually Add
			elif confirm_input.upper() == 'Y':
				cursor = main.mydb.cursor(prepared=True)
				stmt = "INSERT INTO Order_Product (order_id, product_id, quantity) values(%s, %s, %s)"
				Order_Product_tuple = (order_id, product_id, quantity)
				cursor.execute(stmt, Order_Product_tuple)
				main.mydb.commit()
				print(">>>Product add to Order. Here is the Order Product detail")
				get_latest_Order_Product()

				# Add more item?
				add_more = input("Do you want to add more Product to this Order?\nEnter (y) to add more or (n) to finish: ")
				if add_more.upper() == 'N':
					print(">>>Finish adding Product to Order")
					return
				elif add_more.upper() == 'Y':
					print(">>>Returning to select product ID")
				else:
					print(">>>Add more Invalid input! Please enter (y) or (n).")
			else:
				print(">>>Confirmation Invalid input! Please enter (y) or (n).")

def edit_Order_Product():

	# Get & check order_id
	while True:
		order_id = get_valid_order_id()
		if order_id:
			break # Exit order ID loop
		elif order_id is None:
			print(">>>Unskippable value! Abort editing Product to Order!")
			return
	# Get & check product_id
	while True:		
		product_id = get_valid_product_id()
		if product_id:
			break # Exit product ID loop
		elif product_id is None:
			print(">>>Unskippable value! Abort editing Product to Order!")
			return

	Order_Product = get_Order_Product_by_id(order_id, product_id)
	if Order_Product is None:
		print("This order and product doesn't exists!")
	else:
		print("The order product pair is found")
		
		quantity = get_quantity_integer()

		# CF?
		print("The Order_Product you want to edit to has the following details",
				"\n\tOrder Id: ", order_id,
				"\n\tProduct Id: ", product_id,
				"\n\tQuantity: ", quantity)

		confirm_input = input("Please enter (y) to confirm action or (n) to cancel action: ")
			
		if confirm_input.upper() == 'N':
			print(">>>Abort editing Product to Order!")
			return

		# Actually Edit
		elif confirm_input.upper() == 'Y':
			cursor = main.mydb.cursor(prepared=True)
			stmt = "UPDATE Order_Product SET "
			tuple = []

			if quantity != None: # I mean qty is never null but for readability...
				stmt += "quantity = %s, "
				tuple.append(quantity)

			if len(tuple) == 0:
				print(">>>No fields updated to this order.")

			else:
				stmt = stmt.rstrip(', ') + " WHERE order_id = %s"
				tuple.append(order_id)
				cursor.execute(stmt, tuple)
				main.mydb.commit()
				print(">>>Order_Product ", order_id, " edited. Here is the updated details:")
				get_Order_Product_by_id(order_id, product_id)

		else:
			print(">>>Confirmation Invalid input! Please enter (y) or (n).")

def delete_Order_Product():

	# Get & check order_id
	while True:
		order_id = get_valid_order_id()
		if order_id:
			break # Exit order ID loop
		elif order_id is None:
			print(">>>Unskippable value! Abort editing Product to Order!")
			return
	# Get & check product_id
	while True:		
		product_id = get_valid_product_id()
		if product_id:
			break # Exit product ID loop
		elif product_id is None:
			print(">>>Unskippable value! Abort editing Product to Order!")
			return
	Order_Product = get_Order_Product_by_id(order_id, product_id)
	if Order_Product is None:
		print("This order and product doesn't exists!")
	else:
		print("The order product pair is found")

		confirm_input = input("Please enter (y) to confirm action or (n) to cancel action: ")
			
		if confirm_input.upper() == 'N':
			print(">>>Abort deleting Product to Order!")
			return

		# Actually Delete
		elif confirm_input.upper() == 'Y':
			cursor = main.mydb.cursor(prepared=True)
			delete_stmt = "DELETE FROM Order_Product WHERE order_id = %s AND product_id = %s"
			cursor.execute(delete_stmt, (order_id, product_id))
			main.mydb.commit()

			# Check rows affected after deletion
			if cursor.rowcount:
				print(f">>>Order {order_id} Product {product_id} deleted.")
			else:
				print(f">>>Failed to delete order {order_id} product {product_id}.")
		else:
			print(">>>Confirmation Invalid input! Please enter (y) or (n).")
