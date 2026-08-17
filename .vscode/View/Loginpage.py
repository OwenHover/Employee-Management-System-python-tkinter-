# VIEW layer — Login page UI only
# Login logic (credential check) is handled by employee_controller.py

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))   # find controller/model from view/

from customtkinter import *
from PIL import Image
from tkinter import messagebox
from Controller import EmployeeServlet as controller


# BUTTON HANDLER
def handle_login():
    """Collect credentials → pass to controller → react to result"""
    success, message = controller.login(usernameEntry.get(), passwordEntry.get())
    if success:
        messagebox.showinfo('Success', message)
        root.destroy()          # close login window
        import View.Ems      # open main EMS window
    else:
        messagebox.showerror('Error', message)


# GUI LAYOUT  
root = CTk()
root.geometry('930x478')
root.resizable(0, 0)
root.title('Login Page')

# Background image
image = CTkImage(Image.open('cover6.png'), size=(930, 478))
imageLabel = CTkLabel(root, image=image, text='')
imageLabel.place(x=0, y=0)

# Heading
headingLabel = CTkLabel(root, text='Employee Management System',
                        bg_color='white', font=('Goudy Old Style', 23, 'bold'),
                        text_color='black')
headingLabel.place(x=20, y=100)

# Username field
usernameEntry = CTkEntry(root, placeholder_text='Enter Your Username', width=180)
usernameEntry.place(x=50, y=150)

# Password field
passwordEntry = CTkEntry(root, placeholder_text='Enter Your Password',
                         width=180, show='*')
passwordEntry.place(x=50, y=200)

# Login button — calls handle_login(), not logic directly
loginButton = CTkButton(root, text='Login', cursor='hand2',
                        command=handle_login, width=180, height=30,
                        font=('Arial', 16, 'bold'))
loginButton.place(x=50, y=250)

root.mainloop()