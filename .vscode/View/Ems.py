# VIEW layer — GUI layout and display only
# All logic is handled by EmployeeServlet.py
# This file only: builds widgets, collects input, shows results

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))   # find controller/model from view/

from customtkinter import *
from PIL import Image
from tkinter import ttk, messagebox
import math
from Controller import EmployeeServlet as controller

selected_id = ''
all_records = []       # full list of employees currently displayed
current_page = 1       # which page we are on
PAGE_SIZE = 10         # how many rows per page

# PAGINATION CORE
def refresh_page():
    """Slice all_records to current page and display in treeview"""
    global current_page

    total_pages = max(1, math.ceil(len(all_records) / PAGE_SIZE))

    # Keep current_page in bounds
    if current_page < 1:
        current_page = 1
    if current_page > total_pages:
        current_page = total_pages

    # Slice the records for this page
    start = (current_page - 1) * PAGE_SIZE
    end   = start + PAGE_SIZE
    page_records = all_records[start:end]

    # Rebuild treeview
    tree.delete(*tree.get_children())
    for emp in page_records:
        display = list(emp)
        raw_id = str(display[0])              # raw DB value e.g. '001' or 'ws'
        display[0] = str(display[0]).zfill(3) # padded for display e.g. '001'
        tree.insert('', END, iid=raw_id, values=display)

    # Update page label and button states
    pageLabel.configure(text=f'Page {current_page} / {total_pages}')
    prevButton.configure(state='normal' if current_page > 1 else 'disabled')
    nextButton.configure(state='normal' if current_page < total_pages else 'disabled')

def go_prev():
    global current_page
    current_page -= 1
    refresh_page()

def go_next():
    global current_page
    current_page += 1
    refresh_page()


# VIEW HELPER FUNCTIONS
def treeview_data():
    """Fetch all employees, reset to page 1, display"""
    global all_records, current_page
    all_records = list(controller.get_all_employees())
    current_page = 1
    refresh_page()

def clear(value=False):
    """Reset all input fields to their defaults"""
    global selected_id
    selected_id = ''
    if value:
        tree.selection_remove(tree.focus())
    idEntry.configure(state='normal')
    idEntry.delete(0, END)
    nameEntry.delete(0, END)
    departmentBox.set(department_options[0])
    positionBox.set(position_options[0])
    hireDateEntry.delete(0, END)
    salaryGradeBox.set(salary_grade_options[0])
    contactEntry.delete(0, END)

def selection(event):
    global selected_id
    selected_item = tree.selection()
    if selected_item:
        row = tree.item(selected_item)['values']
        clear()
        selected_id = selected_item[0]   # ← now after clear()
        idEntry.configure(state='normal')
        idEntry.insert(0, str(row[0]))
        idEntry.configure(state='disabled')
        nameEntry.insert(0, row[1])
        departmentBox.set(row[2])
        positionBox.set(row[3])
        hireDateEntry.insert(0, row[4])
        salaryGradeBox.set(row[5])
        contactEntry.insert(0, row[6])

# BUTTON HANDLERS

def handle_add():
    success, message = controller.add_employee(
        idEntry.get(), nameEntry.get(), departmentBox.get(),
        positionBox.get(), hireDateEntry.get(),
        salaryGradeBox.get(), contactEntry.get()
    )
    if success:
        treeview_data()
        clear()
        messagebox.showinfo('Success', message)
    else:
        messagebox.showerror('Error', message)

def handle_update():
    if not tree.selection():
        messagebox.showerror('Error', 'Select a record to update')
        return
    success, message = controller.update_employee(
        selected_id,
        nameEntry.get(), departmentBox.get(),
        positionBox.get(), hireDateEntry.get(),
        salaryGradeBox.get(), contactEntry.get()
    )
    if success:
        treeview_data()
        clear()
        messagebox.showinfo('Success', message)
    else:
        messagebox.showerror('Error', message)

def handle_delete():
    if not tree.selection():
        messagebox.showerror('Error', 'Select a record to delete')
        return
    success, message = controller.delete_employee(selected_id)
    if success:
        treeview_data()
        clear()
        messagebox.showinfo('Success', message)
    else:
        messagebox.showerror('Error', message)

def handle_search():
    global all_records, current_page
    column_map = {
        'ID': 'ID', 'Name': 'Name', 'Department': 'Department',
        'Position': 'Position', 'Hire Date': 'Hire_Date',
        'Salary Grade': 'Salary_Grade', 'Contact': 'Contact'
    }
    results, message = controller.search_employee(
        column_map.get(searchBox.get(), ''),
        searchEntry.get(),
        searchBox.get()
    )
    if results is None:
        messagebox.showerror('Error', message)
    else:
        all_records = list(results)
        current_page = 1
        refresh_page()

def handle_show_all():
    searchEntry.delete(0, END)
    searchBox.set('Search By')
    treeview_data()

def handle_sort():
    sort_window = CTkToplevel(window)
    sort_window.title('Sort Options')
    sort_window.geometry('300x200')
    sort_window.resizable(False, False)

    CTkLabel(sort_window, text='Sort By:', font=('arial', 14)).pack(pady=10)

    sort_options = [
        'Name (A-Z)', 'Name (Z-A)',
        'Hire Date (ASC)', 'Hire Date (DESC)',
        'Salary Grade (ASC)', 'Salary Grade (DESC)'
    ]
    sort_var = StringVar(value=sort_options[0])
    CTkComboBox(sort_window, values=sort_options, variable=sort_var).pack(pady=10)

    def apply_sort():
        global all_records, current_page
        sorted_employees = controller.sort_employees(sort_var.get())
        all_records = list(sorted_employees)
        current_page = 1
        refresh_page()
        sort_window.destroy()

    CTkButton(sort_window, text='Apply Sort', command=apply_sort).pack(pady=20)

def handle_stats():
    results = controller.get_grade_statistics()

    stats_window = CTkToplevel(window)
    stats_window.title('Salary Grade Statistics')
    stats_window.geometry('400x300')
    stats_window.resizable(False, False)

    CTkLabel(stats_window,
             text='Employees by Salary Grade',
             font=('arial', 16, 'bold')).pack(pady=10)

    if not results:
        CTkLabel(stats_window, text='No data available.', font=('arial', 14)).pack(pady=10)
    else:
        for grade, count in results:
            CTkLabel(stats_window,
                     text=f'{grade}:  {count} employee(s)',
                     font=('arial', 14)).pack(pady=4)

    CTkButton(stats_window, text='Close', command=stats_window.destroy).pack(pady=20)

# ══════════════════════════════════════════════════════════════════════════════
# GUI LAYOUT
# ══════════════════════════════════════════════════════════════════════════════

window = CTk()
window.geometry('1100x660')
window.resizable(False, False)
window.title('Employee Management System')
window.configure(fg_color='#161C30')

# Banner image
logo = CTkImage(Image.open('coverems4.png'), size=(1100, 158))
logoLabel = CTkLabel(window, image=logo, text='')
logoLabel.grid(row=0, column=0, columnspan=2)

# LEFT FRAME
leftFrame = CTkFrame(window, fg_color='#161C30')
leftFrame.grid(row=1, column=0, padx=10)

CTkLabel(leftFrame, text='Employee ID', font=('arial', 18, 'bold'), text_color='white').grid(
    row=0, column=0, padx=20, pady=12, sticky='w')
idEntry = CTkEntry(leftFrame, font=('arial', 15, 'bold'), width=200)
idEntry.grid(row=0, column=1)

CTkLabel(leftFrame, text='Name', font=('arial', 18, 'bold'), text_color='white').grid(
    row=1, column=0, padx=20, pady=12, sticky='w')
nameEntry = CTkEntry(leftFrame, font=('arial', 15, 'bold'), width=200)
nameEntry.grid(row=1, column=1)

CTkLabel(leftFrame, text='Department', font=('arial', 18, 'bold'), text_color='white').grid(
    row=2, column=0, padx=20, pady=12, sticky='w')
department_options = ['HR', 'Engineering', 'Finance', 'Marketing',
                      'Operations', 'IT', 'Sales', 'Administration']
departmentBox = CTkComboBox(leftFrame, values=department_options, width=200,
                             font=('arial', 15, 'bold'), state='readonly')
departmentBox.grid(row=2, column=1)
departmentBox.set(department_options[0])

CTkLabel(leftFrame, text='Position', font=('arial', 18, 'bold'), text_color='white').grid(
    row=3, column=0, padx=20, pady=12, sticky='w')
position_options = ['Intern', 'Junior Staff', 'Senior Staff',
                    'Team Lead', 'Manager', 'Director', 'Consultant']
positionBox = CTkComboBox(leftFrame, values=position_options, width=200,
                           font=('arial', 15, 'bold'), state='readonly')
positionBox.grid(row=3, column=1)
positionBox.set(position_options[0])

CTkLabel(leftFrame, text='Hire Date', font=('arial', 18, 'bold'), text_color='white').grid(
    row=4, column=0, padx=20, pady=12, sticky='w')
hireDateEntry = CTkEntry(leftFrame, font=('arial', 15, 'bold'), width=200,
                          placeholder_text='YYYY-MM-DD')
hireDateEntry.grid(row=4, column=1)

CTkLabel(leftFrame, text='Salary Grade', font=('arial', 18, 'bold'), text_color='white').grid(
    row=5, column=0, padx=20, pady=12, sticky='w')
salary_grade_options = ['Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5']
salaryGradeBox = CTkComboBox(leftFrame, values=salary_grade_options, width=200,
                              font=('arial', 15, 'bold'), state='readonly')
salaryGradeBox.grid(row=5, column=1)
salaryGradeBox.set(salary_grade_options[0])

CTkLabel(leftFrame, text='Contact', font=('arial', 18, 'bold'), text_color='white').grid(
    row=6, column=0, padx=20, pady=12, sticky='w')
contactEntry = CTkEntry(leftFrame, font=('arial', 15, 'bold'), width=200)
contactEntry.grid(row=6, column=1)

# RIGHT FRAME
rightFrame = CTkFrame(window)
rightFrame.grid(row=1, column=1, padx=10)

search_options = ['ID', 'Name', 'Department', 'Position', 'Hire Date', 'Salary Grade', 'Contact']
searchBox = CTkComboBox(rightFrame, values=search_options, state='readonly', width=130)
searchBox.grid(row=0, column=0, padx=5, pady=5)
searchBox.set('Search By')

searchEntry = CTkEntry(rightFrame, width=160)
searchEntry.grid(row=0, column=1, padx=5)

CTkButton(rightFrame, text='Search',   width=90, command=handle_search).grid(row=0, column=2, padx=5)
CTkButton(rightFrame, text='Show All', width=90, command=handle_show_all).grid(row=0, column=3, padx=5)

# Treeview
tree = ttk.Treeview(rightFrame, height=10)
tree.grid(row=1, column=0, columnspan=4)

tree['columns'] = ('ID', 'Name', 'Department', 'Position', 'Hire Date', 'Salary Grade', 'Contact')
for col, w in zip(
    ('ID', 'Name', 'Department', 'Position', 'Hire Date', 'Salary Grade', 'Contact'),
    (90,   140,    120,          110,         100,         110,            110)
):
    tree.heading(col, text=col)
    tree.column(col, anchor=CENTER, width=w)

tree.config(show='headings')

style = ttk.Style()
style.configure('Treeview.Heading', font=('arial', 13, 'bold'))
style.configure('Treeview', font=('arial', 12), rowheight=28,
                background='#161C30', foreground='white')

scrollbar = ttk.Scrollbar(rightFrame, orient=VERTICAL, command=tree.yview)
scrollbar.grid(row=1, column=4, sticky='ns')
tree.configure(yscrollcommand=scrollbar.set)

# PAGINATION CONTROLS
paginationFrame = CTkFrame(rightFrame, fg_color='#161C30')
paginationFrame.grid(row=2, column=0, columnspan=4, pady=6)

prevButton = CTkButton(paginationFrame, text='◀  Prev', width=100,
                       font=('arial', 13, 'bold'), corner_radius=10,
                       command=go_prev, state='disabled')
prevButton.grid(row=0, column=0, padx=10)

pageLabel = CTkLabel(paginationFrame, text='Page 1 / 1',
                     font=('arial', 13, 'bold'), text_color='white')
pageLabel.grid(row=0, column=1, padx=20)

nextButton = CTkButton(paginationFrame, text='Next  ▶', width=100,
                       font=('arial', 13, 'bold'), corner_radius=10,
                       command=go_next, state='disabled')
nextButton.grid(row=0, column=2, padx=10)

# BOTTOM BUTTONS
buttonFrame = CTkFrame(window, fg_color='#161C30')
buttonFrame.grid(row=2, column=0, columnspan=2, pady=8)

CTkButton(buttonFrame, text='Clear',           font=('arial', 15, 'bold'), width=150,
          corner_radius=15, command=lambda: clear(True)).grid(row=0, column=0, padx=5)

CTkButton(buttonFrame, text='Add Employee',    font=('arial', 15, 'bold'), width=150,
          corner_radius=15, command=handle_add).grid(row=0, column=1, padx=5)

CTkButton(buttonFrame, text='Update Employee', font=('arial', 15, 'bold'), width=150,
          corner_radius=15, command=handle_update).grid(row=0, column=2, padx=5)

CTkButton(buttonFrame, text='Delete Employee', font=('arial', 15, 'bold'), width=150,
          corner_radius=15, command=handle_delete).grid(row=0, column=3, padx=5)

CTkButton(buttonFrame, text='Sort',            font=('arial', 15, 'bold'), width=150,
          corner_radius=15, command=handle_sort).grid(row=0, column=4, padx=5)

CTkButton(buttonFrame, text='Grade Stats',     font=('arial', 15, 'bold'), width=150,
          corner_radius=15, command=handle_stats).grid(row=0, column=5, padx=5)

# START
treeview_data()
tree.bind('<<TreeviewSelect>>', selection)
window.mainloop()