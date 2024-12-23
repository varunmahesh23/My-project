import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
# from tktimepicker import AnalogPicker, AnalogThemes
from tkinter import ttk, messagebox, Toplevel
from tkcalendar import Calendar  # Ensure to install tkcalendar (`pip install tkcalendar`)
from utils import connect_to_database
import sys
import subprocess
from datetime import datetime, timedelta
from tkcalendar import DateEntry

# Get the user_id from the command-line argument
user_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

# Ensure user_id is provided
if user_id is None:
    print("User ID not provided. Exiting application.")
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
dashboard_window.title("Student Dashboard - Student Mentorship Platform")
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

# Fetch user details from the database
def get_user_details(user_id):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        query = "SELECT first_name, last_name, role FROM users WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            first_name, last_name, role = result
            return f"{first_name} {last_name}", role
    except Exception as e:
        print(f"Error fetching user details: {e}")
    return "User", "student"

# Fetch the user's name and role
user_name, user_role = get_user_details(user_id)

# Wrapper frame for layout
wrapper = ctk.CTkFrame(dashboard_window, fg_color='transparent')
wrapper.pack(fill='both', expand=True)

# Left navigation panel
left_nav = ctk.CTkFrame(wrapper, width=200, fg_color='transparent')
left_nav.pack(fill='y', side="left", padx=10)

# Right section for the main content
right_section = ctk.CTkFrame(wrapper, fg_color='transparent')
right_section.pack(fill='both', side="right", expand=True, padx=20)

# Title section with user info
title_frame = ctk.CTkFrame(right_section, fg_color='transparent')
title_frame.pack(fill="x", pady=20)

# Greeting and role labels with personalized user info
greeting_label = ctk.CTkLabel(title_frame, text=f"Welcome, {user_name}", font=HEADING_FONT, text_color=PRIMARY_COLOR)
greeting_label.pack(side="left", padx=20)

role_label = ctk.CTkLabel(title_frame, text=f"Role: {user_role.capitalize()}", font=SUBHEADING_FONT, text_color=PRIMARY_COLOR)
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
create_nav_button(left_nav, "My Requests", lambda: switch_frame(my_requests_frame), 0)
create_nav_button(left_nav, "Mentor Requests", lambda: switch_frame(mentor_requests_frame), 1)
create_nav_button(left_nav, "Review Progress", lambda: switch_frame(progress_reports_frame), 2)

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

# Frame for My Requests
def my_requests_frame():
    # Main container frame
    frame = ctk.CTkFrame(right_section, fg_color='transparent')
    ctk.CTkLabel(frame, text="My Requests", font=HEADING_FONT, text_color=PRIMARY_COLOR).pack(pady=20)

    # Subframe for table and buttons
    content_frame = ctk.CTkFrame(frame, fg_color="white", width=1000, height=600)
    content_frame.pack_propagate(False)  # Prevent resizing with content
    content_frame.pack(pady=10, padx=20)

    # Table frame for the request table
    table_frame = ctk.CTkFrame(content_frame, fg_color='transparent')
    table_frame.pack(pady=10, padx=20, fill="both", expand=True)

    # Create Treeview with Scrollbars
    request_table = ttk.Treeview(
        table_frame,
        columns=("request_id", "mentor_name", "requested_date", "status"),
        show="headings",
        height=10,
        style="Custom.Treeview"
    )

    # Configure column widths
    request_table.column("request_id", anchor="center", width=80)
    request_table.column("mentor_name", anchor="w", width=200)
    request_table.column("requested_date", anchor="center", width=200)
    request_table.column("status", anchor="center", width=120)

    # Define headings
    request_table.heading("request_id", text="Request ID", anchor="center")
    request_table.heading("mentor_name", text="Mentor Name", anchor="center")
    request_table.heading("requested_date", text="Requested Date", anchor="center")
    request_table.heading("status", text="Status", anchor="center")

    # Add scrollbars
    y_scroll = ctk.CTkScrollbar(table_frame, orientation="vertical", command=request_table.yview)
    x_scroll = ctk.CTkScrollbar(table_frame, orientation="horizontal", command=request_table.xview)
    request_table.configure(yscroll=y_scroll.set, xscroll=x_scroll.set)
    y_scroll.pack(side="right", fill="y")
    x_scroll.pack(side="bottom", fill="x")
    request_table.pack(fill="both", expand=True, padx=10, pady=10)

    # Styling for the Treeview
    style = ttk.Style()
    style.configure("Custom.Treeview.Heading", font=("San Francisco", 12, "bold"), foreground=PRIMARY_COLOR)
    style.configure("Custom.Treeview", font=("San Francisco", 10), background="white", foreground="black", rowheight=25)
    style.map("Custom.Treeview", background=[("selected", PRIMARY_COLOR)], foreground=[("selected", "white")])

    # Fetch and display requests for the user
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        query = """
            SELECT request_id, 
                   (SELECT CONCAT(first_name, ' ', last_name) FROM users WHERE user_id = mentor_id) AS mentor_name,
                   request_date, 
                   status 
            FROM requests 
            WHERE student_id = %s
            ORDER BY request_date DESC
        """
        cursor.execute(query, (user_id,))
        requests = cursor.fetchall()

        # Insert request data into the table
        for request in requests:
            request_id, mentor_name, requested_date, status = request
            request_table.insert(
                "",
                "end",
                values=(request_id, mentor_name, requested_date, status)
            )
        conn.close()
    except Exception as e:
        print(f"Error fetching requests: {e}")

    # Button frame for actions
    button_frame = ctk.CTkFrame(content_frame, fg_color='transparent')
    button_frame.pack(pady=10, padx=20, fill="x", expand=False)

    # Refresh requests button
    def refresh_requests():
        request_table.delete(*request_table.get_children())
        try:
            conn = connect_to_database()
            cursor = conn.cursor()
            cursor.execute(query, (user_id,))
            requests = cursor.fetchall()
            for request in requests:
                request_id, mentor_name, requested_date, status = request
                request_table.insert(
                    "",
                    "end",
                    values=(request_id, mentor_name, requested_date, status)
                )
            conn.close()
        except Exception as e:
            print(f"Error refreshing requests: {e}")

    refresh_button = ctk.CTkButton(
        button_frame,
        text="Refresh",
        font=BUTTON_FONT,
        fg_color=BUTTON_COLOR,
        command=refresh_requests
    )
    refresh_button.pack(side="left", padx=5, pady=10)

    return frame



# Frame for Mentor Requests
def mentor_requests_frame():
    frame = ctk.CTkFrame(right_section, fg_color='transparent')
    # Add heading outside the frame
    ctk.CTkLabel(
        frame,
        text="Mentor Requests",
        font=HEADING_FONT,
        text_color=PRIMARY_COLOR
    ).pack(pady=20)

    # Main container frame with fixed size
    content_frame = ctk.CTkFrame(frame, fg_color="white", width=1000, height=600)
    content_frame.pack_propagate(False)  # Prevent resizing to fit content
    content_frame.grid_propagate(False)  # Prevent grid resizing
    content_frame.pack(pady=10, padx=20)

    # Configure grid for centering
    content_frame.grid_rowconfigure(0, weight=1)
    content_frame.grid_rowconfigure(1, weight=1)
    content_frame.grid_rowconfigure(2, weight=1)
    content_frame.grid_rowconfigure(3, weight=1)
    content_frame.grid_rowconfigure(4, weight=1)
    content_frame.grid_rowconfigure(5, weight=1)
    content_frame.grid_columnconfigure(0, weight=1)
    content_frame.grid_columnconfigure(1, weight=1)

    # Mentor Dropdown
    mentor_var = ctk.StringVar()
    ctk.CTkLabel(content_frame, text="Select a Mentor:", font=("San Francisco", 14), text_color="black").grid(
        row=0, column=0, padx=10, pady=10, sticky="e"
    )
    mentor_dropdown = ctk.CTkOptionMenu(
        content_frame,
        variable=mentor_var,
        values=[],
        width=300,
        height=35,
        dropdown_font=("Arial", 10)
    )
    mentor_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    # Load mentors from the database
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, CONCAT(first_name, ' ', last_name) FROM users WHERE role = 'mentor'")
        mentors = cursor.fetchall()
        conn.close()
        mentor_dropdown.configure(values=[f"{mentor[1]} (ID: {mentor[0]})" for mentor in mentors])
    except Exception as e:
        print(f"Error fetching mentors: {e}")

    # Date Selection
    date_var = ctk.StringVar()

    ctk.CTkLabel(content_frame, text="Select Date:", font=("San Francisco", 14), text_color="black").grid(
        row=1, column=0, padx=10, pady=10, sticky="e"
    )

    # Frame for the button and entry to align them closely
    date_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    date_frame.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    # Button to open calendar
    def show_calendar():
        """Display the calendar widget below the button."""
        calendar_window = ctk.CTkToplevel()
        calendar_window.title("Select Date")
        centre_window(calendar_window, width=400, height=300)
        calendar_window.grab_set()  # Make the calendar modal

        def set_date():
            """Set the selected date to the entry field."""
            selected_date = cal.get_date()
            date_var.set(selected_date)
            calendar_window.destroy()

        # Create Calendar widget
        cal = Calendar(
            calendar_window,
            selectmode="day",
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day,
            date_pattern="mm/dd/yyyy"
        )
        cal.pack(pady=20)

        # Submit button to confirm date selection
        submit_date_button = ctk.CTkButton(
            calendar_window,
            text="Select",
            command=set_date,
            width=100,
            height=40,
            corner_radius=12,
            fg_color=BUTTON_COLOR,
            text_color=TEXT_COLOR
        )
        submit_date_button.pack(pady=10)

    # Button and entry placed inside the same frame for alignment
    select_date_button = ctk.CTkButton(
        date_frame,
        text="Select Date",
        font=("Arial", 12),
        width=120,
        height=35,
        corner_radius=10,
        command=show_calendar,
        fg_color=BUTTON_COLOR,
        text_color=TEXT_COLOR
    )
    select_date_button.grid(row=0, column=0, padx=(0, 5))  # Minimal spacing between button and entry

    date_entry = ctk.CTkEntry(
        date_frame,
        textvariable=date_var,
        width=150,  # Adjust width as necessary
        state="readonly",
        placeholder_text="Select a date"
    )
    date_entry.grid(row=0, column=1)
    # Time Slot Dropdown
    time_var = ctk.StringVar()
    ctk.CTkLabel(content_frame, text="Select Time Slot:", font=("San Francisco", 14), text_color="black").grid(
        row=3, column=0, padx=10, pady=10, sticky="e"
    )
    time_slots = [(datetime.strptime("09:00", "%H:%M") + timedelta(hours=i)).strftime("%H:%M") for i in range(9)]
    time_dropdown = ctk.CTkOptionMenu(
        content_frame,
        variable=time_var,
        values=time_slots,
        width=300,
        height=35,
        dropdown_font=("Arial", 10)
    )
    time_dropdown.grid(row=3, column=1, padx=10, pady=10, sticky="w")

    # Submit Button
    def submit_request():
        mentor_selection = mentor_var.get()
        selected_date = date_var.get()
        selected_time = time_var.get()

        if not mentor_selection or not selected_date or not selected_time:
            ctk.CTkLabel(content_frame, text="Please select all fields.", font=("Arial", 10), text_color=ERROR_COLOR).grid(
                row=5, column=0, columnspan=2, pady=10, sticky="n"
            )
            return

        try:
            mentor_id = int(mentor_selection.split("ID: ")[1].split(")")[0])
            # Convert selected date to MySQL's DATETIME format
            formatted_date = datetime.strptime(selected_date, "%m/%d/%Y").strftime("%Y-%m-%d")
            session_datetime = f"{formatted_date} {selected_time}:00"

            conn = connect_to_database()
            cursor = conn.cursor()
            query = """
                INSERT INTO requests (student_id, mentor_id, request_date, status)
                VALUES (%s, %s, %s, 'Pending')
            """
            cursor.execute(query, (user_id, mentor_id, session_datetime))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Mentor request submitted successfully!")
            mentor_var.set("")
            date_var.set("")
            time_var.set("")
        except Exception as e:
            print(f"Error submitting mentorship request: {e}")
            messagebox.showerror("Error", "Submission failed. Try again.")

    submit_button = ctk.CTkButton(
        content_frame,
        text="Submit Request",
        font=BUTTON_FONT,
        fg_color=BUTTON_COLOR,
        text_color=TEXT_COLOR,
        width=300,
        height=40,
        corner_radius=20,
        command=submit_request,
    )
    submit_button.grid(row=4, column=0, columnspan=2, pady=20, sticky="n")

    return frame


# Frame for Progress Reports
def progress_reports_frame():
    # Main container frame
    frame = ctk.CTkFrame(right_section, fg_color='transparent')
    ctk.CTkLabel(frame, text="Progress & Feedback", font=HEADING_FONT, text_color=PRIMARY_COLOR).pack(pady=20)

    # Subframe for table and buttons
    content_frame = ctk.CTkFrame(frame, fg_color="white", width=1000, height=600)
    content_frame.pack_propagate(False)  # Prevent resizing with content
    content_frame.pack(pady=10, padx=20)

    # Table frame for the session table
    table_frame = ctk.CTkFrame(content_frame, fg_color='transparent')
    table_frame.pack(pady=10, padx=20, fill="both", expand=True)

    # Create Treeview with Scrollbars
    progress_table = ttk.Treeview(
        table_frame,
        columns=("session_id", "mentor_name", "date", "feedback", "progress"),
        show="headings",
        height=10,
        style="Custom.Treeview"
    )

    # Configure column widths
    progress_table.column("session_id", anchor="center", width=100)
    progress_table.column("mentor_name", anchor="w", width=200)
    progress_table.column("date", anchor="center", width=150)
    progress_table.column("feedback", anchor="w", width=350)
    progress_table.column("progress", anchor="center", width=150)

    # Define headings
    progress_table.heading("session_id", text="Session ID", anchor="center")
    progress_table.heading("mentor_name", text="Mentor Name", anchor="center")
    progress_table.heading("date", text="Date", anchor="center")
    progress_table.heading("feedback", text="Feedback", anchor="center")
    progress_table.heading("progress", text="Goal Progress", anchor="center")

    # Add scrollbars
    y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=progress_table.yview)
    x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=progress_table.xview)
    progress_table.configure(yscroll=y_scroll.set, xscroll=x_scroll.set)
    y_scroll.pack(side="right", fill="y")
    x_scroll.pack(side="bottom", fill="x")
    progress_table.pack(fill="both", expand=True, padx=10, pady=10)

    # Styling for the Treeview
    style = ttk.Style()
    style.configure("Custom.Treeview.Heading", font=("San Francisco", 12, "bold"), foreground=PRIMARY_COLOR)
    style.configure("Custom.Treeview", font=("San Francisco", 10), background="white", foreground="black", rowheight=25)
    style.map("Custom.Treeview", background=[("selected", PRIMARY_COLOR)], foreground=[("selected", "white")])

    # Fetch and display session progress and feedback
    def populate_table():
        # Clear existing data
        for row in progress_table.get_children():
            progress_table.delete(row)
        try:
            conn = connect_to_database()
            cursor = conn.cursor()
            query = """
                SELECT 
                    sessions.session_id,
                    CONCAT(users.first_name, ' ', users.last_name) AS mentor_name,
                    sessions.date_time AS date,
                    IFNULL(sessions.feedback, 'No Feedback Yet') AS feedback,
                    IFNULL(sessions.goal_status, 'Not Started') AS progress
                FROM sessions
                JOIN users ON sessions.mentor_id = users.user_id
                WHERE sessions.student_id = %s
                ORDER BY sessions.date_time DESC
            """
            cursor.execute(query, (user_id,))
            sessions = cursor.fetchall()
            for session in sessions:
                progress_table.insert("", "end", values=session)
            conn.close()
        except Exception as e:
            print(f"Error fetching progress reports: {e}")

    # Initial population of the table
    populate_table()

    # Button frame for actions
    button_frame = ctk.CTkFrame(content_frame, fg_color='transparent')
    button_frame.pack(pady=10, padx=20, fill="x", expand=False)

    # Refresh reports button
    def refresh_reports():
        populate_table()

    refresh_button = ctk.CTkButton(
        button_frame,
        text="Refresh",
        font=BUTTON_FONT,
        fg_color=BUTTON_COLOR,
        command=refresh_reports
    )
    refresh_button.pack(side="left", padx=5, pady=10)

    # View details button
    def view_feedback_details():
        selected_item = progress_table.selection()
        if selected_item:
            session_id = progress_table.item(selected_item, "values")[0]
            feedback = progress_table.item(selected_item, "values")[3]
            progress = progress_table.item(selected_item, "values")[4]
            CTkMessagebox(
                title="Session Feedback & Progress",
                message=f"Session ID: {session_id}\nFeedback: {feedback}\nProgress: {progress}",
                icon="info",
                option_1="Close"
            )
        else:
            CTkMessagebox(title="Error", message="Please select a session to view details.", icon="cancel")

    details_button = ctk.CTkButton(
        button_frame,
        text="View Details",
        font=BUTTON_FONT,
        fg_color=PRIMARY_COLOR,
        command=view_feedback_details
    )
    details_button.pack(side="right", padx=5, pady=10)

    return frame



# Start with "My Sessions" as the default frame
switch_frame(my_requests_frame)

# Run the dashboard window loop
dashboard_window.mainloop()
