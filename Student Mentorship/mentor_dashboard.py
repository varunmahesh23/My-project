import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkinter import ttk, messagebox
from utils import connect_to_database
import sys
import subprocess

# Get the user_id from the command-line argument
mentor_id = int(sys.argv[1]) if len(sys.argv) > 1 else 3

# Ensure mentor_id is provided
if mentor_id is None:
    print("Mentor ID not provided. Exiting application.")
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
dashboard_window.title("Mentor Dashboard - Student Mentorship Platform")
centre_window(dashboard_window, width=1200, height=700)
dashboard_window.resizable(False, False)


# Define colors and fonts
PRIMARY_COLOR = "#4A90E2"
SECONDARY_COLOR = "#FFFFFF"
BUTTON_COLOR = "#6A0032"
TEXT_COLOR = "#FFFFFF"
ERROR_COLOR = "#FF4C4C"  # Bright red for error messages
SUCCESS_COLOR = "#4CAF50"  # Green for success messages
HEADING_FONT = ("San Francisco", 24, "bold")
SUBHEADING_FONT = ("San Francisco", 16)
BUTTON_FONT = ("San Francisco", 14, "bold")

# Fetch mentor details from the database
def get_mentor_details(mentor_id):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        query = "SELECT first_name, last_name, role FROM users WHERE user_id = %s"
        cursor.execute(query, (mentor_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            first_name, last_name, role = result
            return f"{first_name} {last_name}", role
    except Exception as e:
        print(f"Error fetching mentor details: {e}")
    return "Mentor", "mentor"

# Get mentor's name and role
mentor_name, mentor_role = get_mentor_details(mentor_id)

# Wrapper frame for layout
wrapper = ctk.CTkFrame(dashboard_window, fg_color='transparent')
wrapper.pack(fill='both', expand=True)

# Left navigation panel
left_nav = ctk.CTkFrame(wrapper, width=200, fg_color='transparent')
left_nav.pack(fill='y', side="left", padx=10)

# Right section for the main content
right_section = ctk.CTkFrame(wrapper, fg_color='transparent')
right_section.pack(fill='both', side="right", expand=True, padx=20)

# Title section with mentor info and sign-out button
title_frame = ctk.CTkFrame(right_section, fg_color='transparent')
title_frame.pack(fill="x", pady=20)

# Greeting and role labels
greeting_label = ctk.CTkLabel(title_frame, text=f"Welcome, {mentor_name}", font=HEADING_FONT, text_color=PRIMARY_COLOR)
greeting_label.pack(side="left", padx=20)

role_label = ctk.CTkLabel(title_frame, text=f"Role: {mentor_role.capitalize()}", font=SUBHEADING_FONT, text_color=PRIMARY_COLOR)
role_label.pack(side="left", padx=20)

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
create_nav_button(left_nav, "Student Requests", lambda: switch_frame(student_requests_frame), 0)
create_nav_button(left_nav, "Scheduled Sessions", lambda: switch_frame(sessions_management_frame), 1)
create_nav_button(left_nav, "Feedback & Reports", lambda: switch_frame(feedback_reports_frame), 2)

# Sign Out Button at the bottom of the left navigation
def sign_out():
    dashboard_window.destroy()
    subprocess.Popen(["python", "home.py"])  # Redirect to home.py

# Use grid for sign-out button to avoid conflict with pack
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

# Frame for Student Requests
def student_requests_frame():
    frame = ctk.CTkFrame(right_section, fg_color='transparent')
    ctk.CTkLabel(frame, text="Student Requests", font=HEADING_FONT, text_color=PRIMARY_COLOR).pack(pady=20)

    # Main container frame
    content_frame = ctk.CTkFrame(frame, fg_color="white", width=1000, height=600)
    content_frame.pack_propagate(False)
    content_frame.pack(pady=10, padx=20)

    # Table frame
    table_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    table_frame.pack(pady=10, padx=20, fill="both", expand=True)

    # Create Treeview with Scrollbars
    requests_table = ttk.Treeview(
        table_frame,
        columns=("request_id", "student_name", "requested_date", "status"),
        show="headings",
        height=10
    )
    requests_table.column("request_id", anchor="center", width=80)
    requests_table.column("student_name", anchor="w", width=200)
    requests_table.column("requested_date", anchor="center", width=200)
    requests_table.column("status", anchor="center", width=150)

    requests_table.heading("request_id", text="Request ID")
    requests_table.heading("student_name", text="Student Name")
    requests_table.heading("requested_date", text="Requested Date & Time")
    requests_table.heading("status", text="Status")

    # Add scrollbars
    y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=requests_table.yview)
    x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=requests_table.xview)
    requests_table.configure(yscroll=y_scroll.set, xscroll=x_scroll.set)
    y_scroll.pack(side="right", fill="y")
    x_scroll.pack(side="bottom", fill="x")
    requests_table.pack(fill="both", expand=True, padx=10, pady=10)

    # Load requests from the database
    def load_requests():
        for item in requests_table.get_children():
            requests_table.delete(item)
        try:
            conn = connect_to_database()
            cursor = conn.cursor()
            query = """
                SELECT request_id,
                       CONCAT(users.first_name, ' ', users.last_name) AS student_name,
                       request_date,
                       status
                FROM requests
                JOIN users ON requests.student_id = users.user_id
                WHERE mentor_id = %s
            """
            cursor.execute(query, (mentor_id,))
            requests = cursor.fetchall()
            for request in requests:
                request_id, student_name, requested_date, status = request
                # Add request to the table
                requests_table.insert("", "end", values=(request_id, student_name, requested_date, status))
            conn.close()
        except Exception as e:
            print(f"Error fetching student requests: {e}")

    load_requests()  # Initial load of requests

    # Approve and Decline functions
    def approve_request():
        selected_item = requests_table.selection()
        if selected_item:
            request_id = requests_table.item(selected_item)["values"][0]
            create_session_from_request(request_id)

    def decline_request():
        selected_item = requests_table.selection()
        if selected_item:
            status = requests_table.item(selected_item)["values"][3]
            if status == "Approved":
                CTkMessagebox(
                    title="Action Restricted",
                    message="Approved requests cannot be rejected.",
                    icon="info"
                )
            else:
                request_id = requests_table.item(selected_item)["values"][0]
                update_request_status(request_id, "Rejected")

    # Function to update request status in the database
    def update_request_status(request_id, new_status):
        try:
            conn = connect_to_database()
            cursor = conn.cursor()
            cursor.execute("UPDATE requests SET status = %s WHERE request_id = %s", (new_status, request_id))
            conn.commit()
            conn.close()
            CTkMessagebox(message=f"Success, Request {new_status} successfully.", icon="check", option_1="Thanks")
            load_requests()  # Refresh the table to show updated requests
        except Exception as e:
            print(f"Error updating request status: {e}")
            CTkMessagebox(title="Error", message="Failed to update request status.", icon="cancel")

    # Function to create a session from an approved request
    def create_session_from_request(request_id):
        try:
            conn = connect_to_database()
            cursor = conn.cursor()

            # Get the request details
            cursor.execute("""
                SELECT student_id, mentor_id, request_date
                FROM requests
                WHERE request_id = %s
            """, (request_id,))
            result = cursor.fetchone()

            if result:
                student_id, mentor_id, request_date = result

                # Check if the session already exists
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM sessions
                    WHERE student_id = %s AND mentor_id = %s AND date_time = %s
                """, (student_id, mentor_id, request_date))
                session_exists = cursor.fetchone()[0]

                if session_exists > 0:
                    CTkMessagebox(title="Info", message="Session already exists.", icon="info")
                else:
                    # Create a session with status 'not_started'
                    cursor.execute("""
                        INSERT INTO sessions (student_id, mentor_id, date_time, goal_status)
                        VALUES (%s, %s, %s, 'not_started')
                    """, (student_id, mentor_id, request_date))

                    # Update the request status to 'Approved'
                    update_request_status(request_id, "Approved")

                    conn.commit()
                    # CTkMessagebox(message="Session created successfully!", icon="check", option_1="Thanks")
            else:
                CTkMessagebox(title="Error", message="Request not found.", icon="cancel")

            conn.close()
            load_requests()  # Refresh the table to show updated requests
        except Exception as e:
            print(f"Error creating session: {e}")
            CTkMessagebox(title="Error", message="Failed to create session.", icon="cancel")

    # Button frame for actions
    button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    button_frame.pack(pady=10, fill="x", expand=False)

    approve_button = ctk.CTkButton(
        button_frame, text="Approve", font=BUTTON_FONT,
        fg_color="green", text_color="white", width=120, height=40,
        command=approve_request
    )
    decline_button = ctk.CTkButton(
        button_frame, text="Decline", font=BUTTON_FONT,
        fg_color="red", text_color="white", width=120, height=40,
        command=decline_request
    )
    approve_button.pack(side="left", padx=10)
    decline_button.pack(side="right", padx=10)

    # Apply a tag to disabled rows
    style = ttk.Style()
    style.configure("Treeview", rowheight=25)
    requests_table.tag_configure("disabled", background="#f0f0f0", foreground="gray")

    return frame


# Frame for Managing Sessions
def sessions_management_frame():
    frame = ctk.CTkFrame(right_section, fg_color='transparent')
    ctk.CTkLabel(frame, text="Sessions Management", font=HEADING_FONT, text_color=PRIMARY_COLOR).pack(pady=20)

    # Main container frame
    content_frame = ctk.CTkFrame(frame, fg_color="white", width=1000, height=600)
    content_frame.pack_propagate(False)
    content_frame.pack(pady=10, padx=20)

    # Table frame
    table_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    table_frame.pack(pady=10, padx=20, fill="both", expand=True)

    # Create Treeview with Scrollbars
    sessions_table = ttk.Treeview(
        table_frame,
        columns=("session_id", "student_name", "date_time", "status"),
        show="headings",
        height=10
    )
    sessions_table.column("session_id", anchor="center", width=80)
    sessions_table.column("student_name", anchor="w", width=200)
    sessions_table.column("date_time", anchor="center", width=200)
    sessions_table.column("status", anchor="center", width=150)

    sessions_table.heading("session_id", text="Session ID")
    sessions_table.heading("student_name", text="Student Name")
    sessions_table.heading("date_time", text="Date & Time")
    sessions_table.heading("status", text="Status")

    # Add scrollbars
    y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=sessions_table.yview)
    x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=sessions_table.xview)
    sessions_table.configure(yscroll=y_scroll.set, xscroll=x_scroll.set)
    y_scroll.pack(side="right", fill="y")
    x_scroll.pack(side="bottom", fill="x")
    sessions_table.pack(fill="both", expand=True, padx=10, pady=10)

    # Load session data from the database
    def load_sessions_data():
        for item in sessions_table.get_children():
            sessions_table.delete(item)
        try:
            conn = connect_to_database()
            cursor = conn.cursor()
            query = """
                SELECT sessions.session_id,
                       CONCAT(users.first_name, ' ', users.last_name) AS student_name,
                       sessions.date_time,
                       sessions.goal_status AS status
                FROM sessions
                JOIN users ON sessions.student_id = users.user_id
                WHERE mentor_id = %s
                ORDER BY sessions.date_time DESC
            """
            cursor.execute(query, (mentor_id,))
            records = cursor.fetchall()
            for record in records:
                sessions_table.insert("", "end", values=record)
            conn.close()
        except Exception as e:
            print(f"Error fetching sessions: {e}")

    load_sessions_data()  # Initial load of data

    # Action function for updating session statuses
    def update_status(session_id, new_status):
        try:
            conn = connect_to_database()
            cursor = conn.cursor()
            cursor.execute("UPDATE sessions SET goal_status = %s WHERE session_id = %s", (new_status, session_id))
            conn.commit()
            conn.close()
            CTkMessagebox(
                title="Success",
                message=f"Session status updated to {new_status}.",
                icon="check"
            )
            load_sessions_data()  # Refresh the table
        except Exception as e:
            print(f"Error updating status: {e}")
            CTkMessagebox(
                title="Error",
                message="Failed to update session status.",
                icon="cancel"
            )

    # Action function for completing sessions
    def complete_selected():
        selected_item = sessions_table.selection()
        if selected_item:
            session_id, _, _, status = sessions_table.item(selected_item)["values"]
            if status in ["in_progress", "not_started"]:
                update_status(session_id, "completed")

    # Action function for marking sessions as in progress
    def mark_in_progress():
        selected_item = sessions_table.selection()
        if selected_item:
            session_id, _, _, status = sessions_table.item(selected_item)["values"]
            if status == "not_started":
                update_status(session_id, "in_progress")

    # Button frame for actions
    button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    button_frame.pack(pady=10, fill="x", expand=False)

    # Complete button
    complete_button = ctk.CTkButton(
        button_frame, text="Complete", font=BUTTON_FONT,
        fg_color="blue", text_color="white", width=120, height=40,
        command=complete_selected
    )
    complete_button.pack(side="left", padx=10)

    # In Progress button
    in_progress_button = ctk.CTkButton(
        button_frame, text="In Progress", font=BUTTON_FONT,
        fg_color="orange", text_color="white", width=120, height=40,
        command=mark_in_progress
    )
    in_progress_button.pack(side="left", padx=10)

    return frame


# Frame for Feedback & Reports
def feedback_reports_frame():
    frame = ctk.CTkFrame(right_section, fg_color='transparent')
    ctk.CTkLabel(frame, text="Feedback & Reports", font=HEADING_FONT, text_color=PRIMARY_COLOR).pack(pady=20)

    # Main container frame
    content_frame = ctk.CTkFrame(frame, fg_color="white", width=1000, height=600)
    content_frame.pack_propagate(False)
    content_frame.pack(pady=10, padx=20)

    # Table frame
    table_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    table_frame.pack(pady=10, padx=20, fill="both", expand=True)

    # Create Treeview with Scrollbars
    feedback_table = ttk.Treeview(
        table_frame,
        columns=("session_id", "student_name", "feedback", "date", "status"),
        show="headings",
        height=10
    )
    feedback_table.column("session_id", anchor="center", width=100)
    feedback_table.column("student_name", anchor="w", width=200)
    feedback_table.column("feedback", anchor="center", width=300)
    feedback_table.column("date", anchor="center", width=150)
    feedback_table.column("status", anchor="center", width=150)

    feedback_table.heading("session_id", text="Session ID")
    feedback_table.heading("student_name", text="Student Name")
    feedback_table.heading("feedback", text="Feedback & Improvement")
    feedback_table.heading("date", text="Date")
    feedback_table.heading("status", text="Status")

    # Add scrollbars
    y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=feedback_table.yview)
    x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=feedback_table.xview)
    feedback_table.configure(yscroll=y_scroll.set, xscroll=x_scroll.set)
    y_scroll.pack(side="right", fill="y")
    x_scroll.pack(side="bottom", fill="x")
    feedback_table.pack(fill="both", expand=True, padx=10, pady=10)

    # Fetch existing feedback and in-progress sessions from the database
    def load_feedback():
        for item in feedback_table.get_children():
            feedback_table.delete(item)
        try:
            conn = connect_to_database()
            cursor = conn.cursor()
            query = """
                SELECT session_id,
                       CONCAT(users.first_name, ' ', users.last_name) AS student_name,
                       IFNULL(feedback, 'No Feedback Yet') AS feedback,
                       date_time,
                       goal_status AS status
                FROM sessions
                JOIN users ON sessions.student_id = users.user_id
                WHERE mentor_id = %s AND goal_status IN ('completed', 'in_progress')
            """
            cursor.execute(query, (mentor_id,))
            feedback_data = cursor.fetchall()
            for fb in feedback_data:
                feedback_table.insert("", "end", values=fb)
            conn.close()
        except Exception as e:
            print(f"Error fetching feedback and reports: {e}")

    load_feedback()  # Initial load of feedback data

    # Feedback Form
    form_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    form_frame.pack(pady=10, fill="x", expand=False)

    # Session selection
    session_label = ctk.CTkLabel(form_frame, text="Select Session:", font=SUBHEADING_FONT, text_color=PRIMARY_COLOR)
    session_label.grid(row=0, column=0, padx=(15, 5), pady=(5, 10), sticky="e")

    session_var = ctk.StringVar()
    session_dropdown = ctk.CTkOptionMenu(form_frame, variable=session_var, values=[], width=300)
    session_dropdown.grid(row=0, column=1, padx=10, pady=(5, 10), sticky="w")

    # Fetch sessions eligible for feedback
    def load_sessions():
        try:
            conn = connect_to_database()
            cursor = conn.cursor()
            query = """
                SELECT session_id, CONCAT(users.first_name, ' ', users.last_name), date_time
                FROM sessions
                JOIN users ON sessions.student_id = users.user_id
                WHERE mentor_id = %s AND goal_status IN ('completed', 'in_progress') AND feedback IS NULL
            """
            cursor.execute(query, (mentor_id,))
            sessions = cursor.fetchall()
            session_dropdown.configure(values=[f"{session[0]} - {session[1]} ({session[2]})" for session in sessions])
            conn.close()
        except Exception as e:
            print(f"Error fetching sessions: {e}")

    load_sessions()  # Load sessions eligible for feedback

    # Feedback entry
    feedback_label = ctk.CTkLabel(form_frame, text="Feedback & Improvement:", font=SUBHEADING_FONT, text_color=PRIMARY_COLOR)
    feedback_label.grid(row=1, column=0, padx=(15, 5), pady=(5, 10), sticky="e")

    feedback_entry = ctk.CTkTextbox(form_frame, height=100, width=500)
    feedback_entry.grid(row=1, column=1, padx=10, pady=(5, 10), sticky="w")

    # Submit feedback function
    def submit_feedback():
        selected_session = session_var.get()
        feedback_text = feedback_entry.get("1.0", "end-1c").strip()

        if not selected_session or not feedback_text:
            CTkMessagebox(
                title="Error",
                message="Please select a session and enter feedback.",
                icon="cancel"
            )
            return

        # Extract session_id from the selected session
        session_id = int(selected_session.split(" - ")[0])

        try:
            conn = connect_to_database()
            cursor = conn.cursor()
            query = """
                UPDATE sessions
                SET feedback = %s, goal_status = 'completed'
                WHERE session_id = %s
            """
            cursor.execute(query, (feedback_text, session_id))
            conn.commit()
            conn.close()

            CTkMessagebox(
                title="Success",
                message="Feedback submitted successfully.",
                icon="check"
            )
            load_feedback()  # Reload feedback data
            load_sessions()  # Reload sessions dropdown
            feedback_entry.delete("1.0", "end")  # Clear feedback field
        except Exception as e:
            print(f"Error submitting feedback: {e}")
            CTkMessagebox(
                title="Error",
                message="Failed to submit feedback.",
                icon="cancel"
            )

    # Submit button
    submit_button = ctk.CTkButton(
        form_frame, text="Submit Feedback", font=BUTTON_FONT,
        fg_color="green", text_color="white", command=submit_feedback
    )
    submit_button.grid(row=2, column=1, padx=15, pady=(20, 5), sticky="e")

    return frame




# Start with "Student Requests" as the default frame
switch_frame(student_requests_frame)

# Run the dashboard window loop
dashboard_window.mainloop()
