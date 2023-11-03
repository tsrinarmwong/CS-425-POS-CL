import mysql.connector
import main
discount_menu = '''
    You have selected Discounts. 
    Please select a menu option:
        0 Return
        1 View Discounts available
        2 Add Discounts
        3 Edit Discounts
        4 Delete Discounts
'''

def handle_discount_menu_option():
    user_input = input(discount_menu)
    is_valid_input = False
    while not is_valid_input:
        is_valid_input = True
        if user_input == "0":
            return
        if user_input == "1":  # view
            get_discounts()
        elif user_input == "2":  # add
            add_discount()
        elif user_input == "3":  # edit
            edit_discount()
        elif user_input == "4":  # delete
            delete_discount()
        else:
            print("Please enter a valid option")
            is_valid_input = False

def get_discounts():
    cursor = main.mydb.cursor(prepared=True)
    cursor.execute("SELECT * FROM DISCOUNT")
    result = cursor.fetchall()
    main.print_with_formating(cursor.description, result)
    return result


def get_discount_by_id(discount_id):
    cursor = main.mydb.cursor(prepared=True)
    stmt = "SELECT * FROM DISCOUNT WHERE discount_id = %s"
    cursor.execute(stmt, [discount_id])
    result = cursor.fetchall()
    if result:
        main.print_with_formating(cursor.description, result)
    return result


def get_discount_details_by_id(discount_id):
    cursor = main.mydb.cursor(prepared=True)
    stmt = "SELECT * FROM DISCOUNT WHERE discount_id = %s"
    cursor.execute(stmt, [discount_id])
    result = cursor.fetchall()
    if result:
        return result, cursor.description
    return None, None



def add_discount():
    discount_amount = input("Enter the discount amount: ")
    discount_description = input("Enter a description for the discount: ")
    coupon_code = input("Enter a coupon code for the discount: ")
# TO DO: add validation for the above changes
    print("The customer you want to add has the following details",
          "\nDiscount Amount: ", discount_amount,
          "\nDescription: ", discount_description,
          "\nCoupon Code: ", coupon_code)
    confirm_input = input("Please enter 'y' to confirm action and 'n' to cancel action")
    if confirm_input == 'n':
        print("no changes made in discount table and following is the table for reference")
        return
    elif confirm_input == 'y':
        cursor = main.mydb.cursor(prepared=True)
        stmt = "INSERT INTO DISCOUNT (discount_amount, discount_description, coupon_code) VALUES (%s, %s, %s)"
        cursor.execute(stmt, (discount_amount, discount_description, coupon_code))
        main.mydb.commit()
        print("Discount added successfully! and these are all the discounts available")
    else:
        print("Please enter the correct option only")
        return
    get_discounts()


def edit_discount():
    discount_id = input("Enter the ID of the discount you want to edit: ")
    try:
        discount_id = int(discount_id)
    except ValueError:
        print("Invalid input. Please enter a number.")
        return
    
    existing_discount, description = get_discount_details_by_id(discount_id)
    if not existing_discount:
        print("Discount not found!")
        return

    print("Existing discount details:")
    main.print_with_formating(description, existing_discount)

    discount_amount = input("Enter the new discount amount (or 'NA' to leave unchanged): ")
    discount_description = input("Enter a new description for the discount (or 'NA' to leave unchanged): ")
    coupon_code = input("Enter a new coupon code for the discount (or 'NA' to leave unchanged): ")

    updates = []
    values = []
    if discount_amount.upper() != 'NA':
        updates.append("discount_amount = %s")
        values.append(discount_amount)
    if discount_description.upper() != 'NA':
        updates.append("discount_description = %s")
        values.append(discount_description)
    if coupon_code.upper() != 'NA':
        updates.append("coupon_code = %s")
        values.append(coupon_code)

    if not updates:
        print("No fields updated for this discount.")
        return

    stmt = "UPDATE DISCOUNT SET " + ", ".join(updates) + " WHERE discount_id = %s"
    values.append(discount_id)

    cursor = main.mydb.cursor(prepared=True)
    cursor.execute(stmt, values)
    main.mydb.commit()

    print("Discount updated successfully!")
    get_discounts()


def delete_discount():
    discount_id = input("Enter the ID of the discount you want to delete: ")
    existing_discount = get_discount_by_id(discount_id)
    if not existing_discount:
        print("Discount not found!")
        return

    confirm = input(f"Are you sure you want to delete the discount with ID {discount_id}? (y/n) ")
    if confirm.lower() == 'y':
        cursor = main.mydb.cursor(prepared=True)
        stmt = "DELETE FROM DISCOUNT WHERE discount_id = %s"
        cursor.execute(stmt, [discount_id])
        main.mydb.commit()
        print("Discount deleted successfully!")
    else:
        print("Operation cancelled.")
    
    get_discounts()

    