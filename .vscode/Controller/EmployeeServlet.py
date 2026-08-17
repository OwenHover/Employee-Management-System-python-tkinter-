# CONTROLLER layer — business logic and validation only
# Sits between the View (ems.py / loginpage.py) and the Model (database.py)
# Every function returns a result the View can directly use — no GUI code here

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))   # find model from controller/

import Model.database as database
import re


# LOGIN
def login(username, password):
    """Validate login credentials. Returns (success: bool, message: str)"""
    if username == '' or password == '':
        return False, 'All fields cannot be empty'
    elif username == 'Admin' and password == '1234':
        return True, 'Login successful'
    else:
        return False, 'Invalid username or password'
    
    

# VALIDATION HELPERS  (internal — not called by view directly)
def _validate_fields(id, name, hire_date, contact):
    """Check all mandatory text fields and formats. Returns (valid: bool, message: str)"""

    # Empty field check
    if id == '' or name == '' or hire_date == '' or contact == '':
        return False, 'All fields are required'

    # Hire date format: must be YYYY-MM-DD
    date_pattern = r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$'
    if not re.match(date_pattern, hire_date):
        return False, 'Hire Date must be in YYYY-MM-DD format (e.g. 2023-06-15)'

    # Contact: digits only, 7–15 characters
    if not re.match(r'^\d{7,15}$', contact):
        return False, 'Contact must be a phone number (7–15 digits, no spaces)'

    return True, 'OK'

# CRUD OPERATIONS
def add_employee(id, name, department, position, hire_date, salary_grade, contact):
    """Validate then insert a new employee. Returns (success: bool, message: str)"""
    valid, message = _validate_fields(id, name, hire_date, contact)
    if not valid:
        return False, message

    if database.id_exists(id):
        return False, 'Employee ID already exists'

    database.insert(id, name, department, position, hire_date, salary_grade, contact)
    return True, 'Employee added successfully'


def update_employee(id, name, department, position, hire_date, salary_grade, contact):
    """Validate then update an existing employee. Returns (success: bool, message: str)"""
    valid, message = _validate_fields(id, name, hire_date, contact)
    if not valid:
        return False, message

    database.update(id, name, department, position, hire_date, salary_grade, contact)
    return True, 'Employee updated successfully'


def delete_employee(id):
    """Delete an employee by ID. Returns (success: bool, message: str)"""
    if id == '':
        return False, 'No employee selected'

    database.delete(id)
    return True, 'Employee deleted successfully'


# FETCH & SEARCH
def get_all_employees():
    """Return all employee records from the database"""
    return database.fetch_employees()


def search_employee(column, value, display_label):
    """
    Search employees by column and value.
    Returns (results: list | None, message: str)
    Results is None when there is a validation error.
    """
    if value == '':
        return None, 'Enter a value to search'
    if display_label == 'Search By':
        return None, 'Please select a search option'

    results = database.search(column, value)
    return results, 'OK'


# SORT
def sort_employees(sort_option):
    """
    Sort all employees by the given option string.
    Returns a sorted list of employee tuples.
    Column index reference:
        0=ID, 1=Name, 2=Department, 3=Position, 4=Hire_Date, 5=Salary_Grade, 6=Contact
    """
    employees = database.fetch_employees()

    if sort_option == 'Name (A-Z)':
        return sorted(employees, key=lambda x: x[1].lower())

    elif sort_option == 'Name (Z-A)':
        return sorted(employees, key=lambda x: x[1].lower(), reverse=True)

    elif sort_option == 'Hire Date (ASC)':
        return sorted(employees, key=lambda x: str(x[4]))

    elif sort_option == 'Hire Date (DESC)':
        return sorted(employees, key=lambda x: str(x[4]), reverse=True)

    elif sort_option == 'Salary Grade (ASC)':
        return sorted(employees, key=lambda x: x[5])

    elif sort_option == 'Salary Grade (DESC)':
        return sorted(employees, key=lambda x: x[5], reverse=True)

    return employees     # fallback: unsorted

# STATISTICS
def get_grade_statistics():
    """Return employee count grouped by salary grade"""
    return database.count_by_salary_grade()