import customtkinter as ctk
from PIL import Image, ImageTk
import subprocess

# Function to center the application window on the screen
def centre_window(root_window, width=800, height=600):
    """Centers the window on the screen."""
    root_window.geometry(f"{width}x{height}")
    screen_width = root_window.winfo_screenwidth()
    screen_height = root_window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root_window.geometry(f"{width}x{height}+{x}+{y}")


class HomeWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Mentorship Platform")
        self.root.geometry("1200x800")
        self.root.resizable(False, False)

        # Configure theme and color scheme (Light theme)
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("breeze.json")

        # Colors and fonts
        self.PRIMARY_COLOR = "#2F80ED"  # Soft blue
        self.BUTTON_COLOR = "#56CCF2"  # Sky blue
        self.TEXT_COLOR = "#333333"  # Dark text for readability
        self.HEADING_FONT = ("Arial", 28, "bold")
        self.SUBHEADING_FONT = ("Arial", 16, "italic")
        self.BUTTON_FONT = ("Arial", 14, "bold")
        self.NORMAL_FONT = ("Arial", 12)

        # Wrapper Frame (Transparent background for content)
        self.wrapper = ctk.CTkFrame(self.root, fg_color='transparent', corner_radius=20)
        self.wrapper.place(relwidth=1, relheight=1)

        # Set up background image with opacity
        bg_image = Image.open('images/background_image.jpeg').resize((1200, 800))
        bg_image = bg_image.convert("RGBA")
        alpha = bg_image.split()[3]
        alpha = alpha.point(lambda p: p * 0.8)
        bg_image.putalpha(alpha)
        bg_photo = ImageTk.PhotoImage(bg_image)

        self.background_label = ctk.CTkLabel(self.wrapper, image=bg_photo, text="")
        self.background_label.place(relwidth=1, relheight=1)
        self.background_label.image = bg_photo

        # Initialize layout components
        self.setup_title_section()
        self.setup_action_buttons()
        self.setup_features_section()
        self.setup_cta_section()
        self.setup_footer()

    def setup_title_section(self):
        title_frame = ctk.CTkFrame(self.wrapper, fg_color='white', bg_color='#299EC1', corner_radius=20)
        title_frame.pack(fill="x", padx=20, pady=5)

        title_label = ctk.CTkLabel(
            title_frame,
            text="Welcome to the Student Mentorship Platform",
            font=self.HEADING_FONT,
            text_color=self.PRIMARY_COLOR,
            fg_color='transparent'
        )
        title_label.pack()

        subheading_label = ctk.CTkLabel(
            title_frame,
            text="Connecting Students with Mentors for Academic and Career Success",
            font=self.SUBHEADING_FONT,
            text_color=self.PRIMARY_COLOR,
            fg_color='transparent'
        )
        subheading_label.pack(pady=10)

    def setup_action_buttons(self):
        action_frame = ctk.CTkFrame(self.wrapper, fg_color='white', bg_color= '#58C9D1', corner_radius=15)
        action_frame.pack(pady=60)

        # Sub-frame to hold buttons with text
        signin_frame = ctk.CTkFrame(action_frame, fg_color='transparent', corner_radius=15)
        signin_frame.grid(row=0, column=0, padx=30, pady=10)

        signin_label = ctk.CTkLabel(
            signin_frame,
            text="Already a member?",
            font=self.NORMAL_FONT,
            text_color=self.PRIMARY_COLOR,
            fg_color='transparent'
        )
        signin_label.pack()

        signin_button = ctk.CTkButton(
            signin_frame,
            text="Sign In",
            font=self.BUTTON_FONT,
            fg_color=self.BUTTON_COLOR,
            text_color=self.TEXT_COLOR,
            hover_color="#3498DB",
            width=180,
            height=50,
            corner_radius=12,
            command=self.open_signin
        )
        signin_button.pack(pady=5)

        # Sub-frame to hold buttons with text
        signup_frame = ctk.CTkFrame(action_frame, fg_color='transparent', corner_radius=15)
        signup_frame.grid(row=0, column=1, padx=30, pady=10)

        signup_label = ctk.CTkLabel(
            signup_frame,
            text="New here?",
            font=self.NORMAL_FONT,
            text_color=self.PRIMARY_COLOR,
            fg_color='transparent'
        )
        signup_label.pack()

        signup_button = ctk.CTkButton(
            signup_frame,
            text="Sign Up",
            font=self.BUTTON_FONT,
            fg_color=self.BUTTON_COLOR,
            text_color=self.TEXT_COLOR,
            hover_color="#3498DB",
            width=180,
            height=50,
            corner_radius=12,
            command=self.open_signup
        )
        signup_button.pack(pady=5)

    def setup_features_section(self):
        features_frame = ctk.CTkFrame(self.wrapper, fg_color='white',bg_color= '#6DCED5', corner_radius=15)
        features_frame.pack(pady=60, padx=260, fill='both',expand = True)

        feature_title = ctk.CTkLabel(
            features_frame,
            text="Key Features of the Platform",
            font=self.HEADING_FONT,
            text_color=self.PRIMARY_COLOR,
            fg_color='transparent'
        )
        feature_title.pack()

        feature_description = ctk.CTkLabel(
            features_frame,
            text="Designed to make your mentorship experience seamless and effective",
            font=self.SUBHEADING_FONT,
            text_color=self.PRIMARY_COLOR,
            fg_color='transparent'
        )
        feature_description.pack(pady=10)

        icons_frame = ctk.CTkFrame(features_frame, fg_color='transparent', corner_radius=15)
        icons_frame.pack(pady=20)

        # Adding icons with descriptions
        self.create_feature_icon(icons_frame, "images/mentor.png", "Mentor Matching", 0, 0)
        self.create_feature_icon(icons_frame, "images/session.png", "Book Sessions", 0, 1)
        self.create_feature_icon(icons_frame, "images/report.png", "Track Progress", 0, 2)
        self.create_feature_icon(icons_frame, "images/career.png", "Career Guidance", 1, 0)
        self.create_feature_icon(icons_frame, "images/project.png", "Project Assistance", 1, 1)
        self.create_feature_icon(icons_frame, "images/community.png", "Join Communities", 1, 2)

    def create_feature_icon(self, frame, image_path, text, row, column):
        icon_image = Image.open(image_path).resize((60, 60))
        icon_photo = ImageTk.PhotoImage(icon_image)

        icon_frame = ctk.CTkFrame(frame, fg_color='transparent', corner_radius=15)
        icon_frame.grid(row=row * 2, column=column, padx=30, pady=20)

        icon_label = ctk.CTkLabel(icon_frame, image=icon_photo, text="", fg_color='transparent')
        icon_label.image = icon_photo  # Keep reference to avoid garbage collection
        icon_label.pack()

        text_label = ctk.CTkLabel(
            icon_frame, 
            text=text, 
            font=self.NORMAL_FONT, 
            fg_color='transparent', 
            text_color=self.PRIMARY_COLOR,
            justify="center"
        )
        text_label.pack()

    def setup_cta_section(self):
        cta_frame = ctk.CTkFrame(self.wrapper, fg_color='transparent', corner_radius=20)
        cta_frame.pack(pady=50)

        cta_label = ctk.CTkLabel(
            cta_frame,
            text="Ready to take the next step in your academic journey?",
            font=("Arial", 24, "bold"),
            text_color=self.BUTTON_COLOR,
            fg_color='transparent'
        )
        cta_label.pack()

        cta_description = ctk.CTkLabel(
            cta_frame,
            text="Join now and connect with mentors who can guide you to success!",
            font=self.NORMAL_FONT,
            text_color=self.PRIMARY_COLOR,
            fg_color='transparent'
        )
        cta_description.pack(pady=10)

        cta_buttons_frame = ctk.CTkFrame(cta_frame, fg_color='transparent', corner_radius=15)
        cta_buttons_frame.pack(pady=20)

        cta_signin_button = ctk.CTkButton(
            cta_buttons_frame,
            text="Sign In",
            font=self.BUTTON_FONT,
            fg_color=self.BUTTON_COLOR,
            text_color=self.TEXT_COLOR,
            hover_color="#3498DB",
            width=180,
            height=50,
            corner_radius=12,
            command=self.open_signin
        )
        cta_signin_button.grid(row=0, column=0, padx=30)

        cta_signup_button = ctk.CTkButton(
            cta_buttons_frame,
            text="Sign Up",
            font=self.BUTTON_FONT,
            fg_color=self.BUTTON_COLOR,
            text_color=self.TEXT_COLOR,
            hover_color="#3498DB",
            width=180,
            height=50,
            corner_radius=12,
            command=self.open_signup
        )
        cta_signup_button.grid(row=0, column=1, padx=30)

    def setup_footer(self):
        footer_frame = ctk.CTkFrame(self.wrapper, fg_color='transparent', corner_radius=15)
        footer_frame.pack(fill='x', side='bottom')

        footer_label = ctk.CTkLabel(
            footer_frame,
            text="Student Mentorship Platform © 2024 - Empowering Students, Connecting Mentors",
            font=("Arial", 10),
            text_color=self.TEXT_COLOR,
            fg_color='transparent'
        )
        footer_label.pack(pady=10)

    # Functions to open Sign-in and Sign-up windows
    def open_signin(self):
        subprocess.Popen(["python", "signin.py"])
        self.root.destroy()

    def open_signup(self):
        subprocess.Popen(["python", "signup.py"])
        self.root.destroy()

# Main execution
if __name__ == "__main__":
    root = ctk.CTk()
    centre_window(root, width=1200, height=800)
    app = HomeWindow(root)
    root.mainloop()
