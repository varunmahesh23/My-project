# Student Mentorship Platform (SMP)

The **Student Mentorship Platform** is a scalable, secure, and user-friendly system designed to formalize and enhance mentorship programs for students. It enables seamless interaction between students and mentors while providing administrators with powerful tools to monitor and optimize mentorship effectiveness.

---

## Features

### For Students:
- **Registration and Login**: Secure onboarding with email validation and password encryption.
- **Mentor Matching**: Find mentors based on academic and professional needs.
- **Session Booking**: Book mentorship sessions with an interactive calendar.
- **Progress Tracking**: Monitor personal progress with visual feedback from mentors.

### For Mentors:
- **Session Management**: Approve, reject, or schedule mentorship sessions.
- **Feedback Tools**: Provide detailed feedback for students.
- **Progress Monitoring**: Track students' development over time.

### For Administrators:
- **User Management**: Manage student and mentor accounts.
- **Reporting**: Generate and export detailed PDF reports on program effectiveness.
- **Session Oversight**: Monitor session statuses and overall platform activity.

---

## Technologies Used
- **Programming Languages**: Python
- **Database**: MySQL
- **Frameworks**: CustomTkinter (GUI), ReportLab (PDF generation)
- **Libraries**: Pandas, TkCalendar, Matplotlib
- **Security**: Role-based access control, password encryption, SQL injection prevention

---

## Installation Guide

### Prerequisites
- **Operating System**: Windows, macOS, or Linux
- **Python Version**: 3.8 or higher
- **Database**: MySQL Server installed and configured
- **Package Manager**: PIP (Python package installer)

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/student-mentorship-platform.git
   ```
2. **Install Dependencies**:
   Navigate to the project directory and run:
   ```bash
   pip install -r requirements.txt
   ```
   
3. **Set Up the Database**:
   - Create a database:
     ```sql
     CREATE DATABASE student_mentorship_platform;
     ```
   - Import the schema:
     ```bash
     mysql -u root -p student_mentorship_platform < schema.sql
     ```
   - Update the `config.py` file with your database credentials.

4. **Run the Application**:
   Execute the following command to start the platform:
   ```bash
   python main.py
   ```

---

## Usage

### **Students**
1. Register and log in to the platform.
2. Search for mentors based on their expertise.
3. Book sessions and track progress via the dashboard.

### **Mentors**
1. Log in to manage your schedule and student requests.
2. Approve or decline session requests.
3. Provide detailed feedback and monitor student growth.

### **Administrators**
1. Log in to oversee all platform activity.
2. Manage user accounts and generate insightful reports.

---

## System Design

- **Relational Database**: Structured to ensure seamless data flow between users, sessions, and reports.
- **Data Security**: Implements role-based access, encrypted communication, and password protection.
- **Scalable Architecture**: Handles increasing user load without compromising performance.

---

## Key Screens

1. **Landing Page**: Overview of platform functionality.
2. **Dashboard**:
   - Students: Track sessions and progress.
   - Mentors: Manage requests and provide feedback.
   - Admins: Monitor activities and generate reports.
3. **Session Management**: Book, approve, or review mentorship sessions.
4. **Reports**: View or export detailed analytics on platform usage.

---

## Future Enhancements
- **Mobile App Integration**: Extend platform functionality to mobile devices.
- **AI-based Mentor Matching**: Use machine learning for better mentor-student pairings.
- **Advanced Analytics**: Provide predictive insights on program effectiveness.

---

## Contributors
- Varun Mahesh Yarraguntla
- Ruthvick Reddy Nagaram
- Naga Sai Raghu Ram Golla
- Revanth Dongala
- Harsha Vardhan Reddy Vippala

---

## License
This project is licensed under the MIT License.

---

## Contact
For any questions or feedback, feel free to reach out:
- Email: varunmahesh2000@gmail.com
- LinkedIn: [Varun Mahesh Yarraguntla](https://linkedin.com/in/varun-mahesh-22l)
- GitHub: [GitHub Profile](https://github.com/varunmahesh23)
