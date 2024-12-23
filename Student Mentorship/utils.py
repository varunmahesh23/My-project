import mysql.connector
from mysql.connector import Error
from tkinter import messagebox
from config import Config
from PIL import Image, ImageTk
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Connect to the database
def connect_to_database():
    """Establishes a connection to the MySQL database using the configuration from config.py"""
    try:
        conn = mysql.connector.connect(
            host=Config.db_host,
            user=Config.db_user,
            password=Config.db_password,
            database=Config.db_name
        )
        if conn.is_connected():
            return conn
    except Error as e:
        messagebox.showerror("Database Error", f"Error connecting to database: {e}")
        return None

# Authenticate user during Sign-In
def authenticate_user(email, password):
    """Authenticates a user based on email and password."""
    conn = connect_to_database()
    if not conn:
        return None, None, "Database connection failed"

    try:
        cursor = conn.cursor()
        query = "SELECT password, user_id, role FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        if result:
            stored_password = result[0]
            if stored_password == password:
                # Authentication successful, return user_id and role
                return result[1], result[2], None
            else:
                # Password does not match
                return None, None, "Incorrect password"
        else:
            # Email not found in the database
            return None, None, "Email not found"
    except Exception as e:
        return None, None, f"Error authenticating user: {e}"
    finally:
        conn.close()

# Save new user during Sign-Up
def save_user(first_name, last_name, email, role, password, security_question, security_answer):
    """Saves a new user to the database with additional security question and answer."""
    conn = connect_to_database()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        query = """INSERT INTO users (first_name, last_name, email, role, password, security_question, security_answer) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (first_name, last_name, email, role, password, security_question, security_answer))
        conn.commit()
        return True
    except Error as e:
        print(f"Error saving user: {e}")
        return False
    finally:
        conn.close()

# Fetch security question for a user based on their email
def get_security_question(email):
    """Fetches the security question for a user based on their email."""
    conn = connect_to_database()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        query = "SELECT security_question FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        if result:
            return result[0]  # Return the security question
        else:
            return None
    except Error as e:
        print(f"Error fetching security question: {e}")
        return None
    finally:
        conn.close()

# Validate security answer for a user
def validate_security_answer(email, answer):
    """Validates the security answer for a user based on their email."""
    conn = connect_to_database()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        query = "SELECT security_answer FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        if result[0] == answer:
            return True  # Security answer matches
        else:
            return False  # Security answer does not match
    except Error as e:
        print(f"Error validating security answer: {e}")
        return False
    finally:
        conn.close()

# Resize image for buttons and icons
def resize_image(size, image_path):
    """Resizes an image to the specified size for use in UI elements."""
    try:
        img = Image.open(image_path)
        img = img.resize(size)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        messagebox.showerror("Image Error", f"Error resizing image: {e}")
        return None

# Fetch user role based on email
def get_user_role(email):
    """Fetches the role (student, mentor, admin) of a user based on email."""
    conn = connect_to_database()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        query = "SELECT role FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        if result:
            return result[0]  # Return the role (student, mentor, admin)
        else:
            messagebox.showerror("Error", "User not found.")
            return None
    except Error as e:
        messagebox.showerror("Database Error", f"Error fetching user role: {e}")
        return None
    finally:
        conn.close()

# Fetch user name based on email
def get_user_name(email):
    """Fetches the full name of a user based on their email."""
    conn = connect_to_database()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        query = "SELECT first_name, last_name FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        if result:
            return f"{result[0]} {result[1]}"  # Return the full name
        else:
            messagebox.showerror("Error", "User not found.")
            return None
    except Error as e:
        messagebox.showerror("Database Error", f"Error fetching user name: {e}")
        return None
    finally:
        conn.close()

# Fetch sessions for a student or mentor
def fetch_sessions(user_id, role):
    """Fetches mentoring sessions for students or mentors."""
    conn = connect_to_database()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        if role == "student":
            query = "SELECT session_id, mentor_id, date_time, status FROM sessions WHERE student_id = %s"
        elif role == "mentor":
            query = "SELECT session_id, student_id, date_time, status FROM sessions WHERE mentor_id = %s"
        else:
            return []

        cursor.execute(query, (user_id,))
        return cursor.fetchall()
    except Error as e:
        messagebox.showerror("Database Error", f"Error fetching sessions: {e}")
        return []
    finally:
        conn.close()

# Fetch reports for admins
def fetch_reports(admin_id):
    """Fetches reports generated by admins."""
    conn = connect_to_database()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        query = "SELECT report_id, report_name, date_generated FROM reports WHERE generated_by = %s"
        cursor.execute(query, (admin_id,))
        return cursor.fetchall()
    except Error as e:
        messagebox.showerror("Database Error", f"Error fetching reports: {e}")
        return []
    finally:
        conn.close()

# Update session status
def update_session_status(session_id, status):
    """Updates the status of a session."""
    conn = connect_to_database()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        query = "UPDATE sessions SET status = %s WHERE session_id = %s"
        cursor.execute(query, (status, session_id))
        conn.commit()
        return True
    except Error as e:
        messagebox.showerror("Database Error", f"Error updating session status: {e}")
        return False
    finally:
        conn.close()

# Get user ID by email
def get_user_id(email):
    """Fetches user ID based on email."""
    conn = connect_to_database()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        query = "SELECT user_id FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            messagebox.showerror("Error", "User ID not found.")
            return None
    except Error as e:
        messagebox.showerror("Database Error", f"Error fetching user ID: {e}")
        return None
    finally:
        conn.close()

# Fetch notifications for a user
def fetch_notifications(user_id):
    """Fetch notifications for the given user ID."""
    notifications = []
    conn = connect_to_database()
    if not conn:
        return notifications

    try:
        cursor = conn.cursor()
        query = """
            SELECT message, date_sent 
            FROM notifications 
            WHERE user_id = %s 
            ORDER BY date_sent DESC
        """
        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()

        for row in rows:
            message, date_sent = row
            notification = f"{date_sent}: {message}"
            notifications.append(notification)
    except Error as e:
        print(f"Error fetching notifications: {e}")
    finally:
        cursor.close()
        conn.close()

    return notifications

# Reset password for a user
def reset_password(email, new_password):
    """Resets the password for a user based on their email."""
    conn = connect_to_database()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        query = "UPDATE users SET password = %s WHERE email = %s"
        cursor.execute(query, (new_password, email))
        conn.commit()
        print("Password reset successful")
        return True
    except Error as e:
        print(f"Error resetting password: {e}")
        return False
    finally:
        conn.close()
