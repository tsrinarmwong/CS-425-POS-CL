class Employee:
    def __init__(self, employee_id, name_first_name, name_last_name, employee_role, phone_number, employee_email, employee_password):
        self.employee_id = employee_id
        self.name_first_name = name_first_name
        self.name_last_name = name_last_name
        self.employee_role = employee_role
        self.phone_number = phone_number
        self.employee_email = employee_email
        self.employee_password = employee_password

    def __str__(self):
        return (f"Employee ID: {self.employee_id}, "
                f"Name: {self.name_first_name} {self.name_last_name}, "
                f"employee_role: {self.employee_role}, "
                f"phone_number: {self.phone_number}, "
                f"employee_email: {self.employee_email},"
                f"employee_password: {self.employee_password}")

