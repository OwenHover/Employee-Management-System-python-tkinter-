# Employee Management System

A desktop application for managing employee records, built with Python, CustomTkinter, and MySQL. It supports adding, viewing, updating, and deleting employee data through a simple graphical interface.

## Features

- Add, view, update, and delete employee records
- Search and filter employees
- Clean, modern GUI built with CustomTkinter
- MySQL database integration for persistent storage

## Tech Stack

- **Language:** Python
- **GUI Framework:** CustomTkinter
- **Database:** MySQL

## Getting Started

### Prerequisites

- Python 3.x
- MySQL Server
- Required Python packages (see below)

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/your-username/employee-management-system.git
   cd employee-management-system
   ```

2. Install dependencies
   ```bash
   pip install customtkinter mysql-connector-python
   ```

3. Set up the MySQL database
   - Create a database (e.g. `employee_db`)
   - Update the database connection details (host, user, password, database name) in the project's config/connection file

4. Run the application
   ```bash
   python main.py
   ```

## Project Structure

```
employee-management-system/
├── main.py
├── database/
├── ui/
└── README.md
```

## Acknowledgements

The UI layout (CustomTkinter widgets and structure) was based on this YouTube tutorial: [Employee Management System in Python with CustomTkinter & MySQL](https://www.youtube.com/watch?v=a5iCRrygWxk). Credit to the original creator for the interface design.

