import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from utils import authenticate_user, get_security_question, validate_security_answer, reset_password
from PIL import Image, ImageTk
import subprocess
from tkinter import messagebox
import re  # For regex-based email validation

# Configure appearance for the application
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")
# Function to center the application window on the screen
def centre_window(root_window, width=800, height=600):
    """Centers the window on the screen."""
    root_window.geometry(f"{width}x{height}")
    screen_width = root_window.winfo_screenwidth()
    screen_height = root_window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root_window.geometry(f"{width}x{height}+{x}+{y}")


# Initialize the sign-in window
signin_window = ctk.CTk()
signin_window.title("Sign In - Student Mentorship Platform")
centre_window(signin_window, width=800, height=600)
signin_window.resizable(False, False)


# Define colors and fonts
PRIMARY_COLOR = "#4A90E2"
BUTTON_COLOR = "#6A0032"
TEXT_COLOR = "#FFFFFF"
HEADING_FONT = ("San Francisco", 24, "bold")
BUTTON_FONT = ("San Francisco", 14, "bold")
ERROR_COLOR = "#FF6666"  # Dim red for error messages
SUCCESS_COLOR = "#28A745"

# Background image setup
bg_image = Image.open('images/background_image.jpeg').resize((800, 600))
bg_photo = ImageTk.PhotoImage(bg_image)

background_label = ctk.CTkLabel(signin_window, image=bg_photo, text="")
background_label.place(relwidth=1, relheight=1)
background_label.image = bg_photo

# Wrapper frame
wrapper = ctk.CTkFrame(signin_window, fg_color="white")
wrapper.pack(fill="both", expand=True, padx=50, pady=50)
# Forgot Password Functionality
def on_forgot_password():
    # Clear the wrapper for forgot password functionality
    for widget in wrapper.winfo_children():
        widget.destroy()

    # Title
    title_label = ctk.CTkLabel(wrapper, text="Forgot Password", font=HEADING_FONT, text_color=PRIMARY_COLOR)
    title_label.pack(pady=20)

    # Forgot password form frame
    forgot_frame = ctk.CTkFrame(wrapper, fg_color="white")
    forgot_frame.pack(pady=20)

    # Email and Load Question Row
    email_label = ctk.CTkLabel(forgot_frame, text="Email:", font=("San Francisco", 14), text_color="black")
    email_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    email_entry = ctk.CTkEntry(forgot_frame, width=200, placeholder_text="Enter your email")
    email_entry.grid(row=0, column=1, padx=10, pady=10)
    load_button = ctk.CTkButton(forgot_frame, text="Load Question", fg_color=PRIMARY_COLOR, command=lambda: load_security_question())
    load_button.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    question_label = ctk.CTkLabel(forgot_frame, text="", font=("San Francisco", 14), text_color="black")
    question_label.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    def load_security_question():
        email = email_entry.get().strip()
        security_question = get_security_question(email)
        if security_question:
            question_label.configure(text=security_question)
        else:
            question_label.configure(text="* Email not found", text_color=ERROR_COLOR)

    # Answer Entry
    answer_label = ctk.CTkLabel(forgot_frame, text="Security Answer:", font=("San Francisco", 14), text_color="black")
    answer_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    answer_entry = ctk.CTkEntry(forgot_frame, width=200, placeholder_text="Enter your answer")
    answer_entry.grid(row=2, column=1, padx=10, pady=10)

    # New Password and Confirm Password Row
    new_password_label = ctk.CTkLabel(forgot_frame, text="New Password:", font=("San Francisco", 14), text_color="black")
    new_password_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
    new_password_entry = ctk.CTkEntry(forgot_frame, width=200, show="*", placeholder_text="Enter new password")
    new_password_entry.grid(row=3, column=1, padx=10, pady=10)

    confirm_password_label = ctk.CTkLabel(forgot_frame, text="Confirm Password:", font=("San Francisco", 14), text_color="black")
    confirm_password_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
    confirm_password_entry = ctk.CTkEntry(forgot_frame, width=200, show="*", placeholder_text="Confirm new password")
    confirm_password_entry.grid(row=4, column=1, padx=10, pady=10)

    # Reset Password Action
    def reset_password_action():
        email = email_entry.get().strip()
        answer = answer_entry.get().strip()
        new_password = new_password_entry.get().strip()
        confirm_password = confirm_password_entry.get().strip()

        if validate_security_answer(email, answer) and reset_password(email, new_password):
            if (
                len(new_password) < 8 or 
                not re.search(r"[A-Za-z]", new_password) or 
                not re.search(r"\d", new_password) or 
                not re.search(r"[!@#$%^&*(),.?\":{}|<>]", new_password)
            ):
                new_password_entry.delete(0, "end")
                confirm_password_entry.delete(0, "end")
                new_password_entry.configure(
                    placeholder_text="*Weak Password ", placeholder_text_color=ERROR_COLOR
                )
                reset_button.focus_set()
                return
            elif new_password != confirm_password:
                confirm_password_entry.delete(0, "end")
                confirm_password_entry.configure(
                    placeholder_text="* Passwords do not match", placeholder_text_color=ERROR_COLOR
                )
                reset_button.focus_set()
                return
            else:
                messagebox.showinfo("Success", "Password reset successful!")
                load_signin_screen()
        elif not validate_security_answer(email, answer):
            answer_entry.delete(0, "end")
            new_password_entry.delete(0, "end")
            confirm_password_entry.delete(0, "end")
            answer_entry.configure(
                placeholder_text="* Incorrect security answer", placeholder_text_color=ERROR_COLOR
            )
            reset_button.focus_set()
            return
        elif new_password != confirm_password:
            confirm_password_entry.delete(0, "end")
            confirm_password_entry.configure(
                placeholder_text="* Passwords do not match", placeholder_text_color=ERROR_COLOR
            )
            reset_button.focus_set()
            return

        
        
        

    reset_button = ctk.CTkButton(wrapper, text="Reset Password", font=BUTTON_FONT, fg_color=BUTTON_COLOR,
                                 text_color=TEXT_COLOR, command=reset_password_action)
    reset_button.pack(pady=20)

    back_button = ctk.CTkButton(wrapper, text="Back", font=BUTTON_FONT, fg_color=PRIMARY_COLOR,
                                text_color=TEXT_COLOR, command=load_signin_screen)
    back_button.pack(pady=10)


def load_signin_screen():
    """Clears the wrapper and loads the sign-in screen."""
    for widget in wrapper.winfo_children():
        widget.destroy()

    # Title section
    title_label = ctk.CTkLabel(wrapper, text="Sign In to Your Account", font=HEADING_FONT, text_color=PRIMARY_COLOR)
    title_label.pack(pady=20)

    # Login form section
    form_frame = ctk.CTkFrame(wrapper, fg_color="white")
    form_frame.pack(pady=20)

    # Email Entry
    email_label = ctk.CTkLabel(form_frame, text="Email:", font=("San Francisco", 14), text_color="black")
    email_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    email_entry = ctk.CTkEntry(form_frame, width=300, placeholder_text="Enter your email")
    email_entry.grid(row=0, column=1, padx=10, pady=10)

    # Password Entry
    password_label = ctk.CTkLabel(form_frame, text="Password:", font=("San Francisco", 14), text_color="black")
    password_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    password_entry = ctk.CTkEntry(form_frame, width=300, show="*", placeholder_text="Enter your password")
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    # Show Password and Forgot Password aligned side by side
    # toggle_frame = ctk.CTkFrame(form_frame, fg_color="white")
    # toggle_frame.grid(row=2, column=1, sticky="w", pady=10)

    # Show Password Checkbox
    show_password_var = ctk.BooleanVar()
    show_password_checkbox = ctk.CTkCheckBox(
        form_frame, text="Show Password", variable=show_password_var,
        command=lambda: password_entry.configure(show="" if show_password_var.get() else "*"),
        text_color="#C0C0C0"
    )
    show_password_checkbox.grid(row=2, column=0, padx=(0, 20))

    # Forgot Password Feature
    forgot_password_label = ctk.CTkLabel(
        form_frame, text="Forgot Password?", font=("San Francisco", 12, "underline"),
        text_color=PRIMARY_COLOR, cursor="hand2"
    )
    forgot_password_label.grid(row=2, column=1, sticky="w")
    forgot_password_label.bind("<Button-1>", lambda e: on_forgot_password())

    def on_signin():
        email = email_entry.get().strip()
        password = password_entry.get().strip()

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            email_entry.delete(0, "end")
            password_entry.delete(0, "end")
            email_entry.configure(placeholder_text="* Invalid email format", placeholder_text_color=ERROR_COLOR)
            signin_button.focus_set() 
            return

        user_id, actual_role, error_text = authenticate_user(email, password)

        if user_id:
            # Show a success messagebox before opening the dashboard
            messagebox.showinfo("Sign In Success", f"Welcome back, {email}!")
            subprocess.Popen(["python", f"{actual_role}_dashboard.py", str(user_id)])
            signin_window.destroy()
        else:
            if error_text == "Email not found":
                email_entry.delete(0, "end")
                password_entry.delete(0, "end")
                email_entry.configure(placeholder_text="* Email not found", placeholder_text_color=ERROR_COLOR)
                password_entry.configure(placeholder_text="Enter your password")

            else:
                password_entry.delete(0, "end")
                password_entry.configure(placeholder_text="* Incorrect password", placeholder_text_color=ERROR_COLOR)
            signin_button.focus_set()


    signin_button = ctk.CTkButton(wrapper, text="Sign In", font=BUTTON_FONT, fg_color=BUTTON_COLOR,
                                  text_color=TEXT_COLOR, width=200, height=40, command=on_signin)
    signin_button.pack(pady=20)

    # Back Button to go to home page
    def on_back_click():
        subprocess.Popen(["python", "home.py"])
        signin_window.destroy()

    back_button = ctk.CTkButton(wrapper, text="Back", font=BUTTON_FONT, fg_color=PRIMARY_COLOR,
                                text_color=TEXT_COLOR, width=100, height=40, command=on_back_click)
    back_button.pack(pady=10)

    def on_signup_click():
        subprocess.Popen(["python", "signup.py"])
        signin_window.destroy()
    
    signup_redirect = ctk.CTkLabel(wrapper, text="Don't have an account? Sign up here", font=("San Francisco", 12, "underline"),
                               text_color=PRIMARY_COLOR, cursor="hand2")
    signup_redirect.pack(pady=10)
    signup_redirect.bind("<Button-1>", lambda e: on_signup_click())

    signin_window.mainloop()

load_signin_screen()



# Run the sign-in window loop
signin_window.mainloop()
