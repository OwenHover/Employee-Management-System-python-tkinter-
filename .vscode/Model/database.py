#connect to database 
import pymysql
from tkinter import messagebox

# Q15 Employee Management fields:
# ID, Name, Department, Position, Hire Date, Salary Grade, Contact

def connect_database():
    global mycursor, conn             # to use functions anywhere
    try:
        conn = pymysql.connect(host='localhost', user='root', password='w3NW3n2005')
        mycursor = conn.cursor()
    except:
        messagebox.showerror('Error', 'Something went wrong, please open MySQL before running again')
        return

    # New separate database and table for Q15 project
    mycursor.execute('CREATE DATABASE IF NOT EXISTS employee_management_q15')
    mycursor.execute('USE employee_management_q15')
    mycursor.execute('''
        CREATE TABLE IF NOT EXISTS employees(
            ID           VARCHAR(20)  PRIMARY KEY,
            Name         VARCHAR(50)  NOT NULL,
            Department   VARCHAR(50)  NOT NULL,
            Position     VARCHAR(50)  NOT NULL,
            Hire_Date    DATE         NOT NULL,
            Salary_Grade VARCHAR(20)  NOT NULL,
            Contact      VARCHAR(20)  NOT NULL
        )
    ''')

# INSERT 
def insert(id, name, department, position, hire_date, salary_grade, contact):
    mycursor.execute(
        'INSERT INTO employees VALUES(%s,%s,%s,%s,%s,%s,%s)',
        (id, name, department, position, hire_date, salary_grade, contact)
    )
    conn.commit()

# ID DUPLICATE CHECK 
def id_exists(id):
    mycursor.execute('SELECT COUNT(*) FROM employees WHERE ID=%s', (id,))
    result = mycursor.fetchone()
    return result[0] > 0              # True if duplicate, False if new

# FETCH ALL 
def fetch_employees():
    mycursor.execute('SELECT * FROM employees')
    return mycursor.fetchall()

# UPDATE (ID is the key and cannot be changed) 
def update(id, new_name, new_department, new_position, new_hire_date, new_salary_grade, new_contact):
    mycursor.execute(
        '''UPDATE employees 
           SET Name=%s, Department=%s, Position=%s, 
               Hire_Date=%s, Salary_Grade=%s, Contact=%s 
           WHERE ID=%s''',
        (new_name, new_department, new_position,
         new_hire_date, new_salary_grade, new_contact, id)
    )
    conn.commit()

# DELETE
def delete(id):
    mycursor.execute('DELETE FROM employees WHERE ID=%s', (id,))
    print(f"DEBUG rows affected: {mycursor.rowcount}")
    conn.commit()

# SEARCH 
def search(option, value):
    # option is a column name chosen from the dropdown (safe, not user-typed)
    mycursor.execute(f'SELECT * FROM employees WHERE {option} LIKE %s', (f'%{value}%',))
    return mycursor.fetchall()

# SALARY GRADE STATISTICS 
def count_by_salary_grade():
    """Return a count of employees grouped by salary grade"""
    mycursor.execute('SELECT Salary_Grade, COUNT(*) FROM employees GROUP BY Salary_Grade ORDER BY Salary_Grade')
    return mycursor.fetchall()   # list of (grade, count) tuples

connect_database()