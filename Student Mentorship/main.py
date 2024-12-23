import subprocess
import customtkinter as ctk
from utils import connect_to_database
from home import HomeWindow

# Set up the appearance and color theme for the whole app
ctk.set_appearance_mode("Dark")  # Options are "Dark" and "Light"
ctk.set_default_color_theme("blue")  # Options include "blue", "green", "dark-blue"

# Function to create required tables with new security question columns
def create_tables():
    create_users_table_query = """CREATE TABLE IF NOT EXISTS users (
        user_id INT NOT NULL AUTO_INCREMENT,
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        role ENUM('student', 'mentor', 'admin') NOT NULL,
        security_question ENUM("What is your mother's maiden name?", "What is your favourite food?", "What is the name of your first pet?") NOT NULL,
        security_answer VARCHAR(255) NOT NULL,
        date_registered TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (user_id)
    );"""

    create_sessions_table_query = """CREATE TABLE IF NOT EXISTS sessions (
        session_id INT NOT NULL AUTO_INCREMENT,
        student_id INT NOT NULL,
        mentor_id INT NOT NULL,
        date_time DATETIME NOT NULL,
        feedback TEXT,
        goal_status ENUM('not_started', 'in_progress', 'completed') DEFAULT 'not_started',
        PRIMARY KEY (session_id),
        FOREIGN KEY (student_id) REFERENCES users(user_id),
        FOREIGN KEY (mentor_id) REFERENCES users(user_id)
    );"""

    create_reports_table_query = """CREATE TABLE IF NOT EXISTS reports (
        report_id INT NOT NULL AUTO_INCREMENT,
        report_name VARCHAR(100),
        generated_by INT NOT NULL,
        date_generated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (report_id),
        FOREIGN KEY (generated_by) REFERENCES users(user_id)
    );"""

    create_requests_table_query = """CREATE TABLE IF NOT EXISTS requests (
        request_id INT NOT NULL AUTO_INCREMENT,
        student_id INT NOT NULL,
        mentor_id INT NOT NULL,
        request_date DATETIME NOT NULL,
        status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
        PRIMARY KEY (request_id),
        FOREIGN KEY (student_id) REFERENCES users(user_id),
        FOREIGN KEY (mentor_id) REFERENCES users(user_id)
    );"""

    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute(create_users_table_query)
        cursor.execute(create_sessions_table_query)
        cursor.execute(create_reports_table_query)
        cursor.execute(create_requests_table_query)
        conn.commit()
        print("Database tables created successfully.")
    except Exception as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

# Function to center the application window on the screen
def centre_window(root_window, width=1200, height=800):
    """Centers the window on the screen."""
    root_window.geometry(f"{width}x{height}")
    screen_width = root_window.winfo_screenwidth()
    screen_height = root_window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root_window.geometry(f"{width}x{height}+{x}+{y}")

# Main function
def main():
    # Initialize database tables
    create_tables()
    
    # Start the main application window
    app = ctk.CTk()  # Initialize main application as customtkinter window
    centre_window(app, width=1200, height=800)
    app.title("Student Mentorship Platform")
    # centre_window(app)
    # Launch the Home Window
    HomeWindow(app)
    
    # Run the Tkinter main loop
    app.mainloop()

# Entry point for the application
if __name__ == "__main__":
    main()
