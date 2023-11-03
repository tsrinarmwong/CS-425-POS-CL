import mysql.connector
import main
import Order_Product as ordp

payment_menu = '''
    You have selected Payment.
    Please select a menu option:
        0 Return
        1 View Payment
        2 Add Payment
        3 Edit Payment
        4 Delete Payment
'''

def handle_payment_menu_option():
    user_input = input(payment_menu)
    is_valid_input = False
    while not is_valid_input:
        is_valid_input = True
        if user_input == "1": #view
            get_payments()
        elif user_input == "2": #add
            create_payment(None)
        elif user_input == "3": #edit
            edit_payment()
        elif user_input == "4": #delete
            delete_payment()
        elif user_input == "0": #exit
            break
        else:
            print("Please enter a valid option")
            is_valid_input = False

def select_payment_choice():
	payment_choice = input("Please enter payment method from the choice:\n1)-Amex\n2)-Master\n3)-Visa\n4)-Cash\n")
	while True:
		if payment_choice == "1": 
			payment_choice = "Amex"
			return payment_choice
		elif payment_choice == "2": 
			payment_choice = "Master"
			return payment_choice
		elif payment_choice == "3": 
			payment_choice = "Visa"
			return payment_choice
		elif payment_choice == "4": 
			payment_choice = "Cash"
			return payment_choice
		else:
			print("Please enter a valid option")

def get_total_amount(order_id):
    cursor = main.mydb.cursor(prepared=True)
    stmt = "SELECT get_order_total(%s)"
    cursor.execute(stmt, [order_id])
    result = cursor.fetchone()
 
    if result:
        main.print_with_formating(cursor.description, [result])
        return result[0]
    return None

def get_payments():
    cursor = main.mydb.cursor(prepared=True)
    cursor.execute("SELECT * FROM Payment")
    result = cursor.fetchall()
    main.print_with_formating(cursor.description, result)
    return result

def get_latest_payment():
    cursor = main.mydb.cursor(prepared=True)
    stmt = "SELECT * FROM Payment ORDER BY payment_id DESC LIMIT 1"
    cursor.execute(stmt)
    result = cursor.fetchone()
    if result:
        main.print_with_formating(cursor.description, [result])
    return result

def get_payment_by_id(payment_id):
    cursor = main.mydb.cursor(prepared=True)
    stmt = "SELECT * FROM Payment WHERE payment_id = %s"
    cursor.execute(stmt, [payment_id])
    result = cursor.fetchone()
    if result:
        main.print_with_formating(cursor.description, [result])
    return result


def get_payment_id(payment_id):
    cursor = main.mydb.cursor(prepared=True)
    stmt = "SELECT payment_id FROM Payment WHERE payment_id = %s"
    cursor.execute(stmt, [payment_id])
    result = cursor.fetchone()
    if result:
        main.print_with_formating(cursor.description, [result])
        return result[0]
    return None

def get_valid_payment_id():
    while True:
        payment_id = input("Please enter the payment ID (or type (q) to skip): ")
        if payment_id.upper() == 'Q':
            return None
        valid_payment_id = get_payment_id(payment_id)
        if valid_payment_id:
            return valid_payment_id
        else:
            print("No payment found with the given ID. Please try again.")

def create_payment(order_id_continue):
	#payment_id,payment_method,payment_amount,order_id
	
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
		order_id = order_id_continue

	# payment_id = order_id
	payment_id = order_id

	# calc total amount
	total_amount = get_total_amount(order_id)
	print(f"Total amount for Order [{order_id}] is: [{total_amount}]")
	
	# ask for payment choice
	payment_choice = select_payment_choice()

	# CF?
	print(f"Order [{order_id}]: Payment method is [{payment_choice}] for total of [{total_amount}]")
	confirm_input = input("Please enter (y) to confirm action or (n) to cancel action: ")
	
	while True:
		if confirm_input.upper() == 'N':
			print(">>>Abort adding Payment to Order!")
			return
		# Actually Add
		elif confirm_input.upper() == 'Y':
			cursor = main.mydb.cursor(prepared=True)
			stmt = "INSERT INTO Payment values(%s, %s, %s, %s)"
			payment_tuple = (payment_id, payment_choice, total_amount, order_id)
			cursor.execute(stmt, payment_tuple)
			main.mydb.commit()
			print(">>>Payment added to Order. Here is the payment detail")
			get_latest_payment()
			break
		else:
			print(">>>Confirmation Invalid input! Please enter (y) or (n).")

def edit_payment():
	
	# Get & check payment_id
	while True:
		payment_id = get_valid_payment_id()
		if payment_id:
			break # Exit payment ID loop
		elif payment_id is None:
			print(">>>Unskippable value! Abort editing Payment to Order!")
			return

	# change only payment method
	new_payment_choice = select_payment_choice()

	while True:
		confirm_input = input("Please enter (y) to confirm action or (n) to cancel action: ")
				
		if confirm_input.upper() == 'N':
			print(">>>Abort editing Payment to Order!")
			return

		# Actually Edit
		elif confirm_input.upper() == 'Y':
			cursor = main.mydb.cursor(prepared=True)
			stmt = "UPDATE Payment SET "
			tuple = []

			if new_payment_choice != None: 
				stmt += "quantity = %s, "
				tuple.append(quantity)

			if len(tuple) == 0:
				print(">>>No fields updated to this order.")
				break

			else:
				stmt = stmt.rstrip(', ') + " WHERE payment_id = %s"
				tuple.append(payment_id)
				cursor.execute(stmt, tuple)
				main.mydb.commit()
				print(">>>Payment ", payment_id, " edited. Here is the updated details:")
				get_payment_by_id(payment_id)
				break
		else:
			print(">>>Confirmation Invalid input! Please enter (y) or (n).")	

def delete_payment():

	# Get & check payment_id
	while True:
		payment_id = get_valid_payment_id()
		if payment_id:
			break # Exit payment ID loop
		elif payment_id is None:
			print(">>>Unskippable value! Abort deleting Payment to Order!")
			return

	while True:
		confirm_input = input("Please enter (y) to confirm DELETE or (n) to cancel action: ")
				
		if confirm_input.upper() == 'N':
			print(">>>Abort deleting Payment to Order!")
			return

		# Actually Delete
		elif confirm_input.upper() == 'Y':
			cursor = main.mydb.cursor(prepared=True)
			delete_stmt = "DELETE FROM Payment WHERE payment_id = %s"
			cursor.execute(delete_stmt, (payment_id))
			main.mydb.commit()

			# Check rows affected after deletion
			if cursor.rowcount:
				print(f">>>Order {payment_id} Payment {payment_id} deleted.")
				break
			else:
				print(f">>>Failed to delete order {payment_id} payment {payment_id}.")
				break
		else:
			print(">>>Confirmation Invalid input! Please enter (y) or (n).")