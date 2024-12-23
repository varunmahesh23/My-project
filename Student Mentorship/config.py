class Config:
    # Database Configuration
    db_host = '141.209.241.57'  # Change this to your database host
    db_user = 'yarra2v'       # Your MySQL username
    db_password = 'mypass'  # Your MySQL password
    db_name = 'BIS698M_GRP7'  # The name of your database
    
    # Application Settings (global constants)
    secret_key = 'supersecretkey'  # Secret key for session management or encryption
    session_duration_minutes = 60  # Default session duration in minutes
    max_file_upload_size = 16 * 1024 * 1024  # Max upload size for documents (16MB)
    
    # SMTP Configuration (for email notifications)
    smtp_server = 'smtp.yourprovider.com'
    smtp_port = 587
    smtp_user = 'your_email@example.com'
    smtp_password = 'email_password'
    
    # Debug Mode
    debug = True  # Set to False in production

    @staticmethod
    def get_database_uri():
        """Returns a formatted database URI for use with an ORM or for testing."""
        return f"mysql://{Config.db_user}:{Config.db_password}@{Config.db_host}/{Config.db_name}"

    @staticmethod
    def get_smtp_settings():
        """Returns SMTP settings for email notifications."""
        return {
            'server': Config.smtp_server,
            'port': Config.smtp_port,
            'user': Config.smtp_user,
            'password': Config.smtp_password
        }
