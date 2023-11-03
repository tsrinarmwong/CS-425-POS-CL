import main
from employee import Employee

EMPLOYEE_OPERATION_MENU = '''
    You have selected the employee table. 
    Operations:
        0 Return
        1 View employees
        2 Add employees
        3 Edit employees
        4 Delete employees
'''


def handle_employee_menu_option():
    while True:
        user_input = input(EMPLOYEE_OPERATION_MENU)
        if user_input == "1":  # view
            get_employees()
        elif user_input == "2":  # add
            add_employee()
        elif user_input == "3":  # edit
            edit_employee_by_id(input("Enter the employee ID of the employee to edit: "))
        elif user_input == "4":  # delete
            delete_employee_by_id(input("Enter the employee ID of the employee to delete: "))
        else:
            break


def get_employee_by_id(employee_id):
    cursor = main.mydb.cursor(prepared=True)
    stmt = "SELECT * FROM Employee WHERE employee_id = %s"
    cursor.execute(stmt, [employee_id])
    result = cursor.fetchone()
    employee = None
    if result:
        employee = Employee(*result)
        print(employee)

    cursor.close()
    return employee


def get_employees():
    cursor = main.mydb.cursor(prepared=True)
    cursor.execute("SELECT * FROM Employee")
    result = cursor.fetchall()
    employees = []

    if result:
        for row in result:
            employee = Employee(*row)
            employees.append(employee)
            print(employee)

    cursor.close()
    return employees


def add_employee():
    employees = get_employees()
    name_first_name = input("Please enter the First Name of the employee")
    name_last_name = input("Please enter the Last Name of the employee")
    employee_role = input("Please enter the employee_role of the employee")
    phone_number = input("Please enter the phone_number of the employee has")
    employee_email = input("Please enter the employee_email of the employee")
    employee_password = input("Please enter the employee_password of the employee")
    cursor = main.mydb.cursor(prepared=True)
    stmt = "INSERT INTO Employee values(%s, %s, %s, %s, %s, %s, %s)"
    inputs = (employees[-1].employee_id + 1, name_first_name, name_last_name, employee_role,
              phone_number, employee_email, employee_password)
    cursor.execute(stmt, inputs)
    main.mydb.commit()
    print("The Employee added. Here is the updated employees")
    get_employees()


def edit_employee_by_id(employee_id):
    try:
        employee = get_employee_by_id(employee_id)
        if employee:
            print("Enter new values (leave blank to keep current value):")
            name_first_name = input(f"First Name [{employee.name_first_name}]: ") or employee.name_first_name
            name_last_name = input(f"Last Name [{employee.name_last_name}]: ") or employee.name_last_name
            employee_role = input(f"Role [{employee.employee_role}]: ") or employee.employee_role
            phone_number = input(f"Phone Number [{employee.phone_number}]: ") or employee.phone_number
            employee_email = input(f"Email [{employee.employee_email}]: ") or employee.employee_email
            employee_password = input(f"Password [{employee.employee_password}]: ") or employee.employee_password

            cursor = main.mydb.cursor(prepared=True)
            stmt = """
                UPDATE Employee
                SET name_first_name = %s, name_last_name = %s, employee_role = %s, phone_number = %s, employee_email = %s, employee_password = %s
                WHERE employee_id = %s
            """
            inputs = (name_first_name, name_last_name, employee_role, phone_number, employee_email, employee_password,
                      employee_id)
            cursor.execute(stmt, inputs)
            main.mydb.commit()
            print("Employee details have been updated successfully.")
        else:
            print(f"No employee found with ID: {employee_id}")

    except Exception as e:
        print(f"An error occurred while editing the employee: {e}")
    finally:
        cursor.close()


def delete_employee_by_id(employee_id):
    try:
        cursor = main.mydb.cursor(prepared=True)
        stmt = "DELETE FROM Employee WHERE employee_id = %s"
        cursor.execute(stmt, (employee_id,))
        main.mydb.commit()
        print(f"Employee with ID: {employee_id} has been deleted successfully.")
    except Exception as e:
        print(f"An error occurred while deleting the employee: {e}")
    finally:
        cursor.close()
