# Unit 9 Assignment - Security-Enhanced Version
# Long Vy
# Cloned and modified from Unit 3 Project

# Original Unit 3 sources:
# w3resource. (2025, August 12). Create a login form in Python with Tkinter.
#   https://www.w3resource.com/python-exercises/tkinter/python-tkinter-basic-exercise-16.php
# GeeksforGeeks. (2025, July 12). Create MySQL database login page in Python using Tkinter.
#   https://www.geeksforgeeks.org/python/create-mysql-database-login-page-in-python-using-tkinter/

# Unit 9 security sources:
# Amezola, M. (2023, February 9). Protecting your code from SQL injection attacks when using
#   raw SQL in Python. Medium. https://medium.com/@miguel.amezola/protecting-your-code-from-sql-
#   injection-attacks-when-using-raw-sql-in-python-916466961c97
# Bourque, P., & Fairley, R. E. (Eds.). (2014). SWEBOK Guide V3.0. IEEE Computer Society.
# Cymulate. (2025, September 7). Input validation.
#   https://cymulate.com/cybersecurity-glossary/input-validation/
# G, V. (2025, December 2). BCrypt vs MD5 SHA: Why BCRYPT is safer for member ids. LinkedIn.
#   https://www.linkedin.com/posts/vaishnavi-g-a87961224_why-bcrypt-is-better-than-md5-or-sha-
#   for-activity-7401453825334898690-jEMO/
# Imperva. (2023, December 20). What is credential stuffing. Imperva Learning Center.
#   https://www.imperva.com/learn/application-security/credential-stuffing/

# Security Change 1: Input Validation & Sanitization
#   Source: Cymulate (2025); SWEBOK p. 13-26
# Security Change 2: Parameterized Queries & Application Service Account
#   Source: Amezola (2023); SWEBOK p. 13-26
# Security Change 3: Password Hashing with bcrypt
#   Source: G, V. (2025); SWEBOK p. 13-26
# Security Change 4: Login Attempt Rate Limiting / Account Lockout
#   Source: Imperva (2023); SWEBOK p. 13-26

import tkinter as Tk
from tkinter import messagebox, ttk
import psycopg2
import bcrypt          # Security Change 3
import re              # Security Change 1
import time            # Security Change 4

# ------------------------------------------------------------------
# Security Change 4: Track login attempts per username
# Imperva (2023) identifies credential stuffing as automated attacks
# using large sets of credentials; rate limiting and lockout are
# recommended defenses. Neither w3resource (2025) nor GeeksforGeeks
# (2025) included this protection in their reference implementations.
# ------------------------------------------------------------------
MAX_ATTEMPTS = 5
LOCKOUT_SECONDS = 60
login_attempts = {}   # { username: {"count": int, "first_attempt_time": float} }

def is_locked_out(username):
    """Return True if the username is currently locked out."""
    if username not in login_attempts:
        return False
    record = login_attempts[username]
    elapsed = time.time() - record["first_attempt_time"]
    if elapsed > LOCKOUT_SECONDS:
        del login_attempts[username]
        return False
    return record["count"] >= MAX_ATTEMPTS

def record_failed_attempt(username):
    """Increment the failed-attempt counter for a username."""
    now = time.time()
    if username not in login_attempts:
        login_attempts[username] = {"count": 1, "first_attempt_time": now}
    else:
        elapsed = time.time() - login_attempts[username]["first_attempt_time"]
        if elapsed > LOCKOUT_SECONDS:
            login_attempts[username] = {"count": 1, "first_attempt_time": now}
        else:
            login_attempts[username]["count"] += 1

def clear_attempts(username):
    """Clear the attempt record on successful login."""
    if username in login_attempts:
        del login_attempts[username]

# ------------------------------------------------------------------
# Security Change 1: Input Validation
# Cymulate (2025) defines input validation as verifying data meets
# predefined criteria before it is processed or stored. SWEBOK lists
# "Validate input" as the first CERT security practice (p. 13-26).
# Only alphanumeric characters and underscores, max 50 chars, accepted.
# ------------------------------------------------------------------
def is_valid_username(username):
    """Return True only if the username contains safe characters."""
    return bool(re.match(r'^[a-zA-Z0-9_]{1,50}$', username))

def login():
    username = entry_username.get().strip()
    password = entry_password.get()

    # Check for empty fields
    if not username or not password:
        messagebox.showerror("Login", "Username and password are required.")
        return

    # Security Change 1: Validate username format before touching the DB
    if not is_valid_username(username):
        messagebox.showerror("Login", "Invalid username format.")
        return

    # Security Change 4: Check lockout before attempting authentication
    if is_locked_out(username):
        messagebox.showerror(
            "Login",
            f"Account temporarily locked after {MAX_ATTEMPTS} failed attempts. "
            f"Please wait {LOCKOUT_SECONDS} seconds before trying again."
        )
        return

    try:
        # ------------------------------------------------------------------
        # Security Change 2: Parameterized Queries & Application Service Account
        # The original GeeksforGeeks (2025) pattern passed end-user credentials
        # directly to psycopg2.connect(). Amezola (2023) explains this creates
        # SQL injection risk when user input is concatenated into queries.
        # Fix: connect via a fixed service account and use %s placeholders to
        # bind user input as data, never as executable SQL (Amezola, 2023).
        # SWEBOK recommends the principle of least privilege (p. 13-26).
        # ------------------------------------------------------------------
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="app_service_account",      # fixed application-level DB user
            password="app_service_password"  # stored securely in env/config
        )

        cursor = conn.cursor()

        # Parameterized query — user input is bound, never concatenated
        cursor.execute(
            "SELECT password_hash, role FROM app_users WHERE username = %s",
            (username,)
        )
        row = cursor.fetchone()

        if row is None:
            record_failed_attempt(username)
            messagebox.showerror("Login", "Invalid username or password.")
            return

        stored_hash, role = row

        # ------------------------------------------------------------------
        # Security Change 3: bcrypt password verification
        # G, V. (2025) explains bcrypt is safer than MD5 or SHA because it is
        # intentionally slow and automatically salts each hash, making
        # brute-force and rainbow-table attacks computationally impractical.
        # The original GeeksforGeeks (2025) pattern did not hash passwords.
        # ------------------------------------------------------------------
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
            clear_attempts(username)
            messagebox.showinfo("Login", "Login successful!")
            open_table_viewer(conn, username, role)
        else:
            record_failed_attempt(username)
            remaining = MAX_ATTEMPTS - login_attempts.get(username, {}).get("count", 0)
            messagebox.showerror(
                "Login",
                f"Invalid username or password. {max(remaining, 0)} attempt(s) remaining."
            )

    except psycopg2.OperationalError:
        messagebox.showerror("Login", "Could not connect to the database.")
    except Exception as e:
        # Security Change 1: Do not expose raw exception details to the user
        # (original w3resource and GeeksforGeeks patterns showed raw errors)
        messagebox.showerror("Error", "An unexpected error occurred. Please contact support.")
        print(f"[Internal Error] {e}")   # log to console/server log only

def open_table_viewer(conn, username, role):
    viewer = Tk.Toplevel(root)
    viewer.title(f"Table Viewer - {username}")

    # Role-based table access
    if role == "admin":
        tables = ["in450a", "in450b", "in450c"]
    elif role == "user_b":
        tables = ["in450b"]
    elif role == "user_c":
        tables = ["in450c"]
    else:
        tables = []

    def load_table(table_name):
        # Security Change 2: Table name validated against a whitelist before
        # interpolation — psycopg2 cannot parameterize identifiers, so the
        # whitelist is the equivalent protection (Amezola, 2023).
        ALLOWED_TABLES = {"in450a", "in450b", "in450c"}
        if table_name not in ALLOWED_TABLES:
            messagebox.showerror("Error", "Invalid table selection.")
            return
        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            col_names = [desc[0] for desc in cursor.description]

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

    for table in tables:
        btn = Tk.Button(viewer, text=f"View {table}", command=lambda t=table: load_table(t))
        btn.pack(pady=2)

    tree = ttk.Treeview(viewer)
    tree.pack(expand=True, fill="both", padx=10, pady=10)

# --- Login Window ---
# GUI structure based on w3resource (2025) and GeeksforGeeks (2025)
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
