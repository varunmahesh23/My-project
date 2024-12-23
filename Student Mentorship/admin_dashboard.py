import customtkinter as ctk
import pandas as pd
import os
import subprocess
from datetime import datetime
from CTkMessagebox import CTkMessagebox
from tkinter import ttk, messagebox
from utils import connect_to_database  # Assume this is a utility function that connects to the database
import sys
import tkinter as tk

# Generate PDF with alternate row coloring
from reportlab.lib.pagesizes import letter,landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib import enums

# Get admin_id from command-line arguments
admin_id = int(sys.argv[1]) if len(sys.argv) > 1 else 5

# Ensure admin_id is provided
if admin_id is None:
    print("Admin ID not provided. Exiting application.")
    sys.exit(1)

# Configure appearance for the application
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Function to center the application window on the screen
def centre_window(root_window, width=1200, height=700):
    """Centers the window on the screen."""
    root_window.geometry(f"{width}x{height}")
    screen_width = root_window.winfo_screenwidth()
    screen_height = root_window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root_window.geometry(f"{width}x{height}+{x}+{y}")

# Initialize the dashboard window
dashboard_window = ctk.CTk()
dashboard_window.title("Admin Dashboard - Student Mentorship Platform")
centre_window(dashboard_window, width=1200, height=700)
dashboard_window.resizable(False, False)


# Define colors and fonts
PRIMARY_COLOR = "#4A90E2"
SECONDARY_COLOR = "#FFFFFF"
BUTTON_COLOR = "#6A0032"
TEXT_COLOR = "#FFFFFF"
HEADING_FONT = ("San Francisco", 24, "bold")
SUBHEADING_FONT = ("San Francisco", 16)
BUTTON_FONT = ("San Francisco", 14, "bold")

# Fetch admin details from the database
def get_admin_details(admin_id):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        query = "SELECT first_name, last_name, role FROM users WHERE user_id = %s"
        cursor.execute(query, (admin_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            first_name, last_name, role = result
            return f"{first_name} {last_name}", role
    except Exception as e:
        print(f"Error fetching admin details: {e}")
    return "Admin User", "admin"

# Get admin's name and role
admin_name, admin_role = get_admin_details(admin_id)

# Wrapper frame for layout
wrapper = ctk.CTkFrame(dashboard_window, fg_color='transparent')
wrapper.pack(fill='both', expand=True)

# Left navigation panel
left_nav = ctk.CTkFrame(wrapper, width=200, fg_color='transparent')
left_nav.pack(fill='y', side="left", padx=10)

# Right section for the main content
right_section = ctk.CTkFrame(wrapper)
right_section.pack(fill='both', side="right", expand=True, padx=20)

# Title section with admin info and sign-out button
title_frame = ctk.CTkFrame(right_section, fg_color=SECONDARY_COLOR)
title_frame.pack(fill="x", pady=20)

# Greeting and role labels
greeting_label = ctk.CTkLabel(title_frame, text=f"Welcome, {admin_name}", font=HEADING_FONT, text_color=PRIMARY_COLOR)
greeting_label.pack(side="left", padx=20)

role_label = ctk.CTkLabel(title_frame, text=f"Role: {admin_role.capitalize()}", font=SUBHEADING_FONT, text_color=PRIMARY_COLOR)
role_label.pack(side="left", padx=20)

# Sign Out Button in top-right corner
signout_button = ctk.CTkButton(
    title_frame,
    text="Sign Out",
    font=BUTTON_FONT,
    fg_color=BUTTON_COLOR,
    text_color=TEXT_COLOR,
    width=100,
    command=lambda: dashboard_window.destroy()  # Simple sign-out action
)
signout_button.pack(side="right", padx=20)

# Function to switch frames (dynamic content)
def switch_frame(new_frame_func):
    for widget in right_section.winfo_children():
        widget.destroy()
    new_frame = new_frame_func()
    new_frame.pack(fill='both', expand=True)

# Dashboard Buttons in Left Navigation
def create_nav_button(frame, text, command, row):
    button = ctk.CTkButton(frame, text=text, font=BUTTON_FONT, fg_color=BUTTON_COLOR, text_color=TEXT_COLOR, width=150, height=40, command=command)
    button.grid(row=row, column=0, pady=20, padx=10)
    return button

# Navigation Buttons
create_nav_button(left_nav, "User Management", lambda: switch_frame(user_management_frame), 0)
create_nav_button(left_nav, "Session Management", lambda: switch_frame(session_management_frame), 1)
create_nav_button(left_nav, "Reports", lambda: switch_frame(reports_frame), 2)
# Sign Out Button at the bottom of the left navigation
def sign_out():
    dashboard_window.destroy()
    subprocess.Popen(["python", "home.py"])  # Redirect to home.py

signout_button = ctk.CTkButton(
    left_nav,
    text="Sign Out",
    font=BUTTON_FONT,
    fg_color=BUTTON_COLOR,
    text_color=TEXT_COLOR,
    width=150,
    command=sign_out
)
signout_button.grid(row=6, column=0, pady=20, padx=10)

def user_management_frame():
    frame = ctk.CTkFrame(right_section, fg_color='transparent')
    ctk.CTkLabel(frame, text="User Management", font=HEADING_FONT, text_color=PRIMARY_COLOR).pack(pady=20)

    # Main container frame
    content_frame = ctk.CTkFrame(frame, fg_color="white", width=1000, height=600)
    content_frame.pack_propagate(False)
    content_frame.pack(pady=10, padx=20)

    # Table frame
    table_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    table_frame.pack(pady=10, padx=20, fill="both", expand=True)

    # Create Treeview with Scrollbars
    user_table = ttk.Treeview(
        table_frame,
        columns=("user_id", "name", "role", "email", "security_question"),
        show="headings",
        height=10
    )
    user_table.column("user_id", anchor="center", width=100)
    user_table.column("name", anchor="w", width=200)
    user_table.column("role", anchor="center", width=100)
    user_table.column("email", anchor="center", width=200)
    user_table.column("security_question", anchor="w", width=300)

    user_table.heading("user_id", text="User ID")
    user_table.heading("name", text="Name")
    user_table.heading("role", text="Role")
    user_table.heading("email", text="Email")
    user_table.heading("security_question", text="Security Question")

    # Add scrollbars
    y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=user_table.yview)
    x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=user_table.xview)
    user_table.configure(yscroll=y_scroll.set, xscroll=x_scroll.set)
    y_scroll.pack(side="right", fill="y")
    x_scroll.pack(side="bottom", fill="x")
    user_table.pack(fill="both", expand=True, padx=10, pady=10)

    # Load users from the database
    def load_users():
        for item in user_table.get_children():
            user_table.delete(item)
        try:
            conn = connect_to_database()
            cursor = conn.cursor()
            query = """
                SELECT user_id, CONCAT(first_name, ' ', last_name), role, email, security_question
                FROM users
            """
            cursor.execute(query)
            users = cursor.fetchall()
            for user in users:
                user_table.insert("", "end", values=user)
            conn.close()
        except Exception as e:
            print(f"Error fetching user data: {e}")

    load_users()  # Initial load of data

    # Function to insert a new user
    def insert_user():
        user_form_window(title="Add User", save_callback=save_user, data=None)

    # Function to update a selected user
    def update_user():
        selected_item = user_table.selection()
        if not selected_item:
            CTkMessagebox(title="Error", message="No user selected for update.", icon="cancel")
            return

        selected_data = user_table.item(selected_item, "values")
        user_id = selected_data[0]
        user_data = {
            "user_id": user_id,
            "name": selected_data[1],
            "role": selected_data[2],
            "email": selected_data[3],
            "security_question": selected_data[4],
        }
        user_form_window(title="Update User", save_callback=save_updated_user, data=user_data)

    # Function to display the user form
    def user_form_window(title, save_callback, data=None):
        form_window = ctk.CTkToplevel()
        form_window.title(title)
        form_window.geometry("400x600")

        ctk.CTkLabel(form_window, text="First Name:", font=SUBHEADING_FONT).pack(pady=(10, 5))
        first_name_entry = ctk.CTkEntry(form_window, width=300)
        first_name_entry.pack(pady=5)

        ctk.CTkLabel(form_window, text="Last Name:", font=SUBHEADING_FONT).pack(pady=(10, 5))
        last_name_entry = ctk.CTkEntry(form_window, width=300)
        last_name_entry.pack(pady=5)

        ctk.CTkLabel(form_window, text="Role:", font=SUBHEADING_FONT).pack(pady=(10, 5))
        role_var = ctk.StringVar(value="student")
        role_dropdown = ctk.CTkOptionMenu(form_window, variable=role_var, values=["student", "mentor"], width=300)
        role_dropdown.pack(pady=5)

        ctk.CTkLabel(form_window, text="Email:", font=SUBHEADING_FONT).pack(pady=(10, 5))
        email_entry = ctk.CTkEntry(form_window, width=300)
        email_entry.pack(pady=5)

        ctk.CTkLabel(form_window, text="Security Question:", font=SUBHEADING_FONT).pack(pady=(10, 5))
        security_question_var = ctk.StringVar(value="What is your mother's maiden name?")
        security_question_dropdown = ctk.CTkOptionMenu(
            form_window,
            variable=security_question_var,
            values=[
                "What is your mother's maiden name?",
                "What is your favourite food?",
                "What is the name of your first pet?"
            ],
            width=300
        )
        security_question_dropdown.pack(pady=5)

        ctk.CTkLabel(form_window, text="Security Answer:", font=SUBHEADING_FONT).pack(pady=(10, 5))
        security_answer_entry = ctk.CTkEntry(form_window, width=300)
        security_answer_entry.pack(pady=5)

        if data:
            first_name, last_name = data["name"].split()
            first_name_entry.insert(0, first_name)
            last_name_entry.insert(0, last_name)
            role_var.set(data["role"])
            email_entry.insert(0, data["email"])
            security_question_var.set(data["security_question"])

        def save_form():
            first_name = first_name_entry.get().strip()
            last_name = last_name_entry.get().strip()
            role = role_var.get()
            email = email_entry.get().strip()
            security_question = security_question_var.get()
            security_answer = security_answer_entry.get().strip()

            if not all([first_name, last_name, role, email, security_question, security_answer]):
                CTkMessagebox(title="Error", message="All fields are required.", icon="cancel")
                return

            save_callback(data["user_id"] if data else None, first_name, last_name, role, email, security_question, security_answer)
            form_window.destroy()

        ctk.CTkButton(form_window, text="Save", font=BUTTON_FONT, fg_color="green", command=save_form).pack(pady=20)

    # Save new user
    def save_user(_, first_name, last_name, role, email, security_question, security_answer):
        try:
            conn = connect_to_database()
            cursor = conn.cursor()
            query = """
                INSERT INTO users (first_name, last_name, role, email, security_question, security_answer)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (first_name, last_name, role, email, security_question, security_answer))
            conn.commit()
            conn.close()
            CTkMessagebox(title="Success", message="User added successfully.", icon="check")
            load_users()
        except Exception as e:
            print(f"Error adding user: {e}")
            CTkMessagebox(title="Error", message="Failed to add user.", icon="cancel")

    # Save updated user
    def save_updated_user(user_id, first_name, last_name, role, email, security_question, security_answer):
        try:
            conn = connect_to_database()
            cursor = conn.cursor()
            query = """
                UPDATE users
                SET first_name = %s, last_name = %s, role = %s, email = %s, security_question = %s, security_answer = %s
                WHERE user_id = %s
            """
            cursor.execute(query, (first_name, last_name, role, email, security_question, security_answer, user_id))
            conn.commit()
            conn.close()
            CTkMessagebox(title="Success", message="User updated successfully.", icon="check")
            load_users()
        except Exception as e:
            print(f"Error updating user: {e}")
            CTkMessagebox(title="Error", message="Failed to update user.", icon="cancel")

    # Button frame for actions
    button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    button_frame.pack(pady=10, fill="x", expand=False)

    insert_button = ctk.CTkButton(
        button_frame, text="Add User", font=BUTTON_FONT,
        fg_color="green", text_color="white", width=120, height=40,
        command=insert_user
    )
    update_button = ctk.CTkButton(
        button_frame, text="Update User", font=BUTTON_FONT,
        fg_color="blue", text_color="white", width=120, height=40,
        command=update_user
    )

    insert_button.pack(side="left", padx=10)
    update_button.pack(side="left", padx=10)

    return frame


# Frame for Session Management
def session_management_frame():
    frame = ctk.CTkFrame(right_section, fg_color='transparent')
    ctk.CTkLabel(frame, text="Session Management", font=HEADING_FONT, text_color=PRIMARY_COLOR).pack(pady=20)

    # Main container frame
    content_frame = ctk.CTkFrame(frame, fg_color="white", width=1000, height=600)
    content_frame.pack_propagate(False)
    content_frame.pack(pady=10, padx=20)

    # Table frame
    table_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    table_frame.pack(pady=10, padx=20, fill="both", expand=True)

    # Create Treeview with Scrollbars
    session_table = ttk.Treeview(
        table_frame,
        columns=("session_id", "student_name", "mentor_name", "status"),
        show="headings",
        height=10
    )
    session_table.column("session_id", anchor="center", width=100)
    session_table.column("student_name", anchor="w", width=200)
    session_table.column("mentor_name", anchor="w", width=200)
    session_table.column("status", anchor="center", width=120)

    session_table.heading("session_id", text="Session ID")
    session_table.heading("student_name", text="Student Name")
    session_table.heading("mentor_name", text="Mentor Name")
    session_table.heading("status", text="Status")

    # Add scrollbars
    y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=session_table.yview)
    x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=session_table.xview)
    session_table.configure(yscroll=y_scroll.set, xscroll=x_scroll.set)
    y_scroll.pack(side="right", fill="y")
    x_scroll.pack(side="bottom", fill="x")
    session_table.pack(fill="both", expand=True, padx=10, pady=10)

    # Styling for the Treeview
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("San Francisco", 12, "bold"), foreground=PRIMARY_COLOR)
    style.configure("Treeview", font=("San Francisco", 10), background="white", foreground="black", rowheight=25)
    style.map("Treeview", background=[("selected", PRIMARY_COLOR)], foreground=[("selected", "white")])

    # Load sessions from the database
    def load_sessions():
        for item in session_table.get_children():
            session_table.delete(item)
        try:
            conn = connect_to_database()
            cursor = conn.cursor()
            query = """
                SELECT session_id, 
                       (SELECT CONCAT(first_name, ' ', last_name) FROM users WHERE user_id = student_id) AS student_name,
                       (SELECT CONCAT(first_name, ' ', last_name) FROM users WHERE user_id = mentor_id) AS mentor_name,
                       goal_status
                FROM sessions
            """
            cursor.execute(query)
            sessions = cursor.fetchall()
            for session in sessions:
                session_table.insert("", "end", values=session)
            conn.close()
        except Exception as e:
            print(f"Error fetching session data: {e}")

    load_sessions()  # Initial load of sessions

    # Button frame for actions
    button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    button_frame.pack(pady=10, fill="x", expand=False)

    # Function to update session status
    def update_session_status(new_status):
        selected_item = session_table.selection()
        if not selected_item:
            CTkMessagebox(title="Error", message="No session selected.", icon="cancel")
            return

        selected_data = session_table.item(selected_item, "values")
        session_id = selected_data[0]

        try:
            conn = connect_to_database()
            cursor = conn.cursor()
            query = "UPDATE sessions SET goal_status = %s WHERE session_id = %s"
            cursor.execute(query, (new_status, session_id))
            conn.commit()
            conn.close()
            CTkMessagebox(title="Success", message=f"Session updated to '{new_status}'.", icon="check")
            load_sessions()  # Refresh the table
        except Exception as e:
            print(f"Error updating session status: {e}")
            CTkMessagebox(title="Error", message="Failed to update session status.", icon="cancel")

    # Buttons for actions
    complete_button = ctk.CTkButton(
        button_frame, text="Mark as Completed", font=BUTTON_FONT,
        fg_color="blue", text_color="white", width=200, height=40,
        command=lambda: update_session_status("completed")
    )
    in_progress_button = ctk.CTkButton(
        button_frame, text="Mark as In Progress", font=BUTTON_FONT,
        fg_color="orange", text_color="white", width=200, height=40,
        command=lambda: update_session_status("in_progress")
    )

    complete_button.pack(side="left", padx=10)
    in_progress_button.pack(side="left", padx=10)

    return frame


def reports_frame():
    frame = ctk.CTkFrame(right_section, fg_color="transparent")
    ctk.CTkLabel(frame, text="Reports", font=HEADING_FONT, text_color=PRIMARY_COLOR).pack(pady=20)

    # Main container frame
    content_frame = ctk.CTkFrame(frame, fg_color="white", width=1000, height=600)
    content_frame.pack_propagate(False)
    content_frame.pack(pady=10, padx=20)

    # Table frame
    table_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    table_frame.pack(pady=10, padx=20, fill="both", expand=True)

    # Create Treeview with Scrollbars
    report_table = ttk.Treeview(
        table_frame,
        columns=(
            "session_id", "student_name", "student_id", 
            "mentor_name", "mentor_id", "session_status", 
            "date_time", "feedback"
        ),
        show="headings",
        height=10
    )
    report_table.column("session_id", anchor="center", width=100)
    report_table.column("student_name", anchor="w", width=150)
    report_table.column("student_id", anchor="center", width=100)
    report_table.column("mentor_name", anchor="w", width=150)
    report_table.column("mentor_id", anchor="center", width=100)
    report_table.column("session_status", anchor="center", width=120)
    report_table.column("date_time", anchor="center", width=150)
    report_table.column("feedback", anchor="w", width=200)

    report_table.heading("session_id", text="Session ID")
    report_table.heading("student_name", text="Student Name")
    report_table.heading("student_id", text="Student ID")
    report_table.heading("mentor_name", text="Mentor Name")
    report_table.heading("mentor_id", text="Mentor ID")
    report_table.heading("session_status", text="Status")
    report_table.heading("date_time", text="Date/Time")
    report_table.heading("feedback", text="Feedback")

    # Add scrollbars
    y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=report_table.yview)
    x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=report_table.xview)
    report_table.configure(yscroll=y_scroll.set, xscroll=x_scroll.set)
    y_scroll.pack(side="right", fill="y")
    x_scroll.pack(side="bottom", fill="x")
    report_table.pack(fill="both", expand=True, padx=10, pady=10)

    # Styling for the Treeview
    style = ttk.Style()
    style.configure("Treeview", rowheight=25)
    style.configure("Treeview.Heading", font=("San Francisco", 12, "bold"), foreground=PRIMARY_COLOR)
    style.configure("Treeview", font=("San Francisco", 10), background="white", foreground="black")
    style.map("Treeview", background=[("selected", PRIMARY_COLOR)], foreground=[("selected", "white")])

    # Dropdown for session status filter using CustomTkinter
    session_status_var = tk.StringVar(value="All")
    filter_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    filter_frame.pack(pady=5, fill="x")
    ctk.CTkLabel(filter_frame, text="Filter by Session Status:", font=BUTTON_FONT).pack(side="left", padx=10)
    
    session_status_dropdown = ctk.CTkComboBox(
        filter_frame,
        values=['All', 'not_started', 'in_progress', 'completed'],
        variable=session_status_var,
        font=BUTTON_FONT,
        dropdown_font=BUTTON_FONT
    )
    session_status_dropdown.pack(side="left", padx=10)

    # Load reports from the database
    def load_reports():
        for item in report_table.get_children():
            report_table.delete(item)
        try:
            conn = connect_to_database()
            cursor = conn.cursor()
            query = """
                SELECT 
                    s.session_id,
                    CONCAT(st.first_name, ' ', st.last_name) AS student_name,
                    st.user_id AS student_id,
                    CONCAT(m.first_name, ' ', m.last_name) AS mentor_name,
                    m.user_id AS mentor_id,
                    s.goal_status AS session_status,
                    s.date_time,
                    COALESCE(s.feedback, 'No Feedback') AS feedback
                FROM sessions s
                INNER JOIN users st ON s.student_id = st.user_id
                INNER JOIN users m ON s.mentor_id = m.user_id
            """
            cursor.execute(query)
            sessions = cursor.fetchall()
            for session in sessions:
                report_table.insert("", "end", values=session)
            conn.close()
        except Exception as e:
            print(f"Error fetching session data: {e}")

    load_reports()

    # Button frame for actions
    button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    button_frame.pack(pady=10, fill="x", expand=False)

    # Generate report with filter and save as PDF
    def generate_report():
        try:
            session_status = session_status_var.get()
            conn = connect_to_database()
            cursor = conn.cursor()

            # Dynamic query based on session status
            query = """
                SELECT 
                    s.session_id,
                    CONCAT(st.first_name, ' ', st.last_name) AS student_name,
                    st.user_id AS student_id,
                    CONCAT(m.first_name, ' ', m.last_name) AS mentor_name,
                    m.user_id AS mentor_id,
                    s.goal_status AS session_status,
                    s.date_time,
                    COALESCE(s.feedback, 'No Feedback') AS feedback
                FROM sessions s
                INNER JOIN users st ON s.student_id = st.user_id
                INNER JOIN users m ON s.mentor_id = m.user_id
            """
            if session_status != "All":
                query += f" WHERE s.goal_status = '{session_status}'"
            query += " ORDER BY s.session_id"

            cursor.execute(query)
            data = cursor.fetchall()

            # Column names
            columns = [
                "Session ID", "Student Name", "Student ID", 
                "Mentor Name", "Mentor ID", "Status", 
                "Date/Time", "Feedback"
            ]

            # Create a PDF
            reports_folder = "reports"
            os.makedirs(reports_folder, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_name = f"Report_status_{session_status}_{timestamp}.pdf"
            report_path = os.path.join(reports_folder, report_name)
            # Create the PDF document
            pdf = SimpleDocTemplate(report_path, pagesize=landscape(letter))
            table_data = [columns] + data

            # Adjust column widths, making the last column (Feedback) wider
            col_widths = [50, 80, 50, 80, 50, 80, 120, 280]
            table = Table(table_data, colWidths=col_widths)

            # Styles for text wrapping
            styles = getSampleStyleSheet()
            style_normal = styles["Normal"]
            style_normal.alignment = enums.TA_LEFT
            # Define the heading style
            heading_style = styles["Heading1"]
            heading_style.alignment = enums.TA_CENTER

            # Create the heading
            heading_text = f"Status of Session: {session_status}"  # Use the variable for the status
            heading = Paragraph(heading_text, heading_style)

            # Spacer for some space between the heading and the table
            spacer = Spacer(1, 20)

            # Wrap feedback text and create table data
            table_data = [columns]
            for row in data:
                wrapped_row = list(row[:-1])  # Add all columns except Feedback
                feedback_paragraph = Paragraph(row[-1], style_normal)  # Wrap Feedback text
                wrapped_row.append(feedback_paragraph)
                table_data.append(wrapped_row)

            # Style the table
            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('VALIGN', (0, 1), (-1, -1), 'TOP'),  # Top-align cells for Feedback
            ])

            # Alternate row coloring
            for i in range(1, len(table_data)):
                bg_color = colors.lightgrey if i % 2 == 0 else colors.whitesmoke
                style.add('BACKGROUND', (0, i), (-1, i), bg_color)

            table.setStyle(style)

            # Build the PDF with heading and table
            pdf.build([heading, spacer, table])

            conn.close()
            CTkMessagebox(title="Success", message=f"Report generated successfully:\n{report_path}", icon="check")
            load_reports()
        except Exception as e:
            print(f"Error generating report: {e}")
            CTkMessagebox(title="Error", message="Failed to generate report.", icon="cancel")

    # Button to generate new reports
    generate_button = ctk.CTkButton(
        button_frame,
        text="Generate Report",
        font=BUTTON_FONT,
        fg_color="blue",
        text_color="white",
        command=generate_report
    )
    generate_button.pack(side="left", padx=10, pady=10)

    # Refresh reports button
    def refresh_reports():
        load_reports()

    refresh_button = ctk.CTkButton(
        button_frame,
        text="Refresh",
        font=BUTTON_FONT,
        fg_color="green",
        text_color="white",
        command=refresh_reports
    )
    refresh_button.pack(side="right", padx=10, pady=10)

    return frame




# Start with "User Management" as the default frame
switch_frame(user_management_frame)

# Run the dashboard window loop
dashboard_window.mainloop()
