import customtkinter as ctk
from utils import save_user, resize_image
from PIL import Image, ImageTk
import subprocess
from tkinter import messagebox
import re  # For regex-based email validation

# Configure appearance for the application
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


# Function to center the application window on the screen
def centre_window(root_window, width=800, height=750):
    """Centers the window on the screen."""
    root_window.geometry(f"{width}x{height}")
    screen_width = root_window.winfo_screenwidth()
    screen_height = root_window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root_window.geometry(f"{width}x{height}+{x}+{y}")


# Initialize the sign-up window
signup_window = ctk.CTk()
signup_window.title("Sign Up - Student Mentorship Platform")
centre_window(signup_window, width=800, height=750)
signup_window.resizable(False, False)


# Define colors and fonts
PRIMARY_COLOR = "#4A90E2"
BUTTON_COLOR = "#6A0032"
TEXT_COLOR = "#FFFFFF"
HEADING_FONT = ("San Francisco", 24, "bold")
BUTTON_FONT = ("San Francisco", 14, "bold")
ERROR_COLOR = "#FF0000"  # Dim red for error messages
SUCCESS_COLOR = "#28A745"

# Background image setup
bg_image = Image.open('images/background_image.jpeg').resize((800, 750))
bg_photo = ImageTk.PhotoImage(bg_image)

background_label = ctk.CTkLabel(signup_window, image=bg_photo, text="")
background_label.place(relwidth=1, relheight=1)
background_label.image = bg_photo  # Prevent garbage collection

# Wrapper frame
wrapper = ctk.CTkFrame(signup_window, fg_color="white")
wrapper.pack(fill="both", expand=True, padx=50, pady=50)

# Title section
title_label = ctk.CTkLabel(wrapper, text="Create Your Account", font=HEADING_FONT, text_color=PRIMARY_COLOR)
title_label.pack(pady=20)

# Sign-up form section
form_frame = ctk.CTkFrame(wrapper, fg_color="white")
form_frame.pack(pady=20)

# First Name Entry
first_name_label = ctk.CTkLabel(form_frame, text="First Name:", font=("San Francisco", 14), text_color="black")
first_name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
first_name_entry = ctk.CTkEntry(form_frame, width=300, placeholder_text="Enter your first name")
first_name_entry.grid(row=0, column=1, padx=10, pady=10)

# Last Name Entry
last_name_label = ctk.CTkLabel(form_frame, text="Last Name:", font=("San Francisco", 14), text_color="black")
last_name_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
last_name_entry = ctk.CTkEntry(form_frame, width=300, placeholder_text="Enter your last name")
last_name_entry.grid(row=1, column=1, padx=10, pady=10)

# Email Entry
email_label = ctk.CTkLabel(form_frame, text="Email:", font=("San Francisco", 14), text_color="black")
email_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
email_entry = ctk.CTkEntry(form_frame, width=300, placeholder_text="Enter your email")
email_entry.grid(row=2, column=1, padx=10, pady=10)

# Role Dropdown (Student/Mentor)
role_label = ctk.CTkLabel(form_frame, text="Role:", font=("San Francisco", 14), text_color="black")
role_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
role_var = ctk.StringVar(value="student")
role_dropdown = ctk.CTkOptionMenu(form_frame, variable=role_var, values=["student", "mentor"])
role_dropdown.grid(row=3, column=1, padx=10, pady=10)

# Password Entry
password_label = ctk.CTkLabel(form_frame, text="Password:", font=("San Francisco", 14), text_color="black")
password_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
password_entry = ctk.CTkEntry(form_frame, width=300, show="*", placeholder_text="Enter your password")
password_entry.grid(row=4, column=1, padx=10, pady=10)

# Show Password Checkbox
show_password_var = ctk.BooleanVar()
show_password_checkbox = ctk.CTkCheckBox(form_frame, text="Show Password", variable=show_password_var, 
                                         command=lambda: password_entry.configure(show="" if show_password_var.get() else "*"))
show_password_checkbox.grid(row=5, column=1, sticky="w")

# Security Question Dropdown
security_question_label = ctk.CTkLabel(form_frame, text="Security Question:", font=("San Francisco", 14), text_color="black")
security_question_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")
security_question_var = ctk.StringVar(value="Select a question")
security_question_dropdown = ctk.CTkOptionMenu(
    form_frame,
    variable=security_question_var,
    values=["What is your mother's maiden name?", "What is your favourite food?", "What is the name of your first pet?"]
)
security_question_dropdown.grid(row=6, column=1, padx=10, pady=10)

# Security Answer Entry
security_answer_label = ctk.CTkLabel(form_frame, text="Answer:", font=("San Francisco", 14), text_color="black")
security_answer_label.grid(row=7, column=0, padx=10, pady=10, sticky="w")
security_answer_entry = ctk.CTkEntry(form_frame, width=300, placeholder_text="Enter your answer")
security_answer_entry.grid(row=7, column=1, padx=10, pady=10)

# Sign-up Button
def on_signup():
    # Get user input
    first_name = first_name_entry.get().strip()
    last_name = last_name_entry.get().strip()
    email = email_entry.get().strip()
    role = role_var.get()
    password = password_entry.get().strip()
    security_question = security_question_var.get()
    security_answer = security_answer_entry.get().strip()
    
    # Reset placeholders to default
    first_name_entry.configure(placeholder_text="Enter your first name", placeholder_text_color="grey")
    last_name_entry.configure(placeholder_text="Enter your last name", placeholder_text_color="grey")
    email_entry.configure(placeholder_text="Enter your email", placeholder_text_color="grey")
    password_entry.configure(placeholder_text="Enter your password", placeholder_text_color="grey")
    security_answer_entry.configure(placeholder_text="Enter your answer", placeholder_text_color="grey")

    # Check if any field is empty
    if not first_name or not last_name or not email or not password or security_question == "Select a question" or not security_answer:
        first_name_entry.focus_set()
        if not first_name:
            first_name_entry.configure(placeholder_text="* Required", placeholder_text_color=ERROR_COLOR)
        if not last_name:
            last_name_entry.configure(placeholder_text="* Required", placeholder_text_color=ERROR_COLOR)
        if not email:
            email_entry.configure(placeholder_text="* Required", placeholder_text_color=ERROR_COLOR)
        if not password:
            password_entry.configure(placeholder_text="* Required", placeholder_text_color=ERROR_COLOR)
        if security_question == "Select a question":
            security_question_var.set("* Required")
        if not security_answer:
            security_answer_entry.configure(placeholder_text="* Required", placeholder_text_color=ERROR_COLOR)
        return

    # Validate email format
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email) or not email.endswith(".com"):
        email_entry.delete(0, "end")
        email_entry.configure(placeholder_text="* Invalid email format", placeholder_text_color=ERROR_COLOR)
        signup_button.focus_set()
        return

    # Validate password
    if len(password) < 8 or not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password) or not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        password_entry.delete(0, "end")
        password_entry.configure(placeholder_text="* Must have mixedcase,num,special characters", placeholder_text_color=ERROR_COLOR)
        signup_button.focus_set()
        return
    
    # If all validations pass, save user
    if save_user(first_name, last_name, email, role, password, security_question, security_answer):
        messagebox.showinfo("Success", "Account created successfully!")
        subprocess.Popen(["python", "signin.py"])  # Redirect to sign-in
        signup_window.destroy()
    else:
        email_entry.delete(0, "end")
        email_entry.configure(placeholder_text="* Email already exists", placeholder_text_color=ERROR_COLOR)
        signup_button.focus_set()

signup_button = ctk.CTkButton(wrapper, text="Sign Up", font=BUTTON_FONT, fg_color=BUTTON_COLOR, 
                              text_color=TEXT_COLOR, width=200, height=40, command=on_signup)
signup_button.pack(pady=20)

# Sign-in redirect
def on_signin_click():
    subprocess.Popen(["python", "signin.py"])
    signup_window.destroy()

signin_redirect = ctk.CTkLabel(wrapper, text="Already have an account? Sign in here", font=("San Francisco", 12, "underline"),
                               text_color=PRIMARY_COLOR, cursor="hand2")
signin_redirect.pack(pady=10)
signin_redirect.bind("<Button-1>", lambda e: on_signin_click())

# Footer
footer_frame = ctk.CTkFrame(wrapper, fg_color=PRIMARY_COLOR)
footer_frame.pack(fill='x', side='bottom')

footer_label = ctk.CTkLabel(footer_frame, text="Student Mentorship Platform © 2024", font=("Arial", 10), text_color=TEXT_COLOR)
footer_label.pack(pady=10)

# Run the sign-up window loop
signup_window.mainloop()
