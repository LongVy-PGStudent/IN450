# Unit 3 Assignment
# Long Vy

#Create a login form in python with Tkinter. w3resource. (2025, August 12). https://www.w3resource.com/python-exercises/tkinter/python-tkinter-basic-exercise-16.php 
#GeeksforGeeks. (2025a, July 12). Create mysql database login page in Python using Tkinter. https://www.geeksforgeeks.org/python/create-mysql-database-login-page-in-python-using-tkinter/ 


import tkinter as Tk
from tkinter import messagebox, ttk
import psycopg2

def login():
    username = entry_username.get()
    password = entry_password.get()

    # Check for empty fields first
    if not username or not password:
        messagebox.showerror("Login", "Username and password are required.")
        return

    try:
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user=username,
            password=password
        )
        messagebox.showinfo("Login", "Login successful!")
        open_table_viewer(conn, username)

    except psycopg2.OperationalError:
        messagebox.showerror("Login", "Invalid username or password.")
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error: {e}")

def open_table_viewer(conn, username):
    viewer = Tk.Toplevel(root)
    viewer.title(f"Table Viewer - {username}")

    # Determine which tables to show based on role
    if username == "in450a_security":
        tables = ["in450a", "in450b", "in450c"]
    elif username == "in450b_security":
        tables = ["in450b"]
    elif username == "in450c_security":
        tables = ["in450c"]
    else:
        tables = []

    def load_table(table_name):
        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            col_names = [desc[0] for desc in cursor.description]

            # Clear existing table
            tree.delete(*tree.get_children())
            tree["columns"] = col_names
            tree["show"] = "headings"

            for col in col_names:
                tree.heading(col, text=col)
                tree.column(col, width=150)

            for row in rows:
                tree.insert("", Tk.END, values=row)

        except psycopg2.errors.InsufficientPrivilege:
            messagebox.showerror("Access Denied", f"You do not have permission to view {table_name}.")

    # Buttons for each table
    for table in tables:
        btn = Tk.Button(viewer, text=f"View {table}", command=lambda t=table: load_table(t))
        btn.pack(pady=2)

    # Treeview to display table data
    tree = ttk.Treeview(viewer)
    tree.pack(expand=True, fill="both", padx=10, pady=10)

# --- Login Window ---
root = Tk.Tk()
root.title("Login Form")

label_username = Tk.Label(root, text="Username:")
label_username.pack()

entry_username = Tk.Entry(root)
entry_username.pack()

label_password = Tk.Label(root, text="Password:")
label_password.pack()

entry_password = Tk.Entry(root, show="*")
entry_password.pack()

button_login = Tk.Button(root, text="Login", command=login)
button_login.pack()

root.mainloop()