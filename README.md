![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

# Student-Teacher Coding Platform

A web-based platform where teachers can create and manage coding problems, and students can solve, run, and submit their code for evaluation. The platform supports user authentication, email verification, and enforces exam integrity by restricting copy-paste, drag-and-drop, and split-screen during coding tests. Try by these two links https://coding-platform-2-ygg0.onrender.com/ <br>
https://coding-platform-2-ijg4.onrender.com/

---

## Features

- **User Roles:** Separate access for Teachers and Students
- **Authentication:** Signup with email verification via activation code
- **Problem Management:** Teachers can add, edit, and delete coding problems
- **Code Editor:** Students can write, run, and submit code solutions
- **Integrity Controls:** Disabled copy-paste, drag-and-drop, and split-screen to prevent cheating
- **Dashboard:** Role-based dashboards showing problem lists, submissions, and results
- **Email Notifications:** Activation codes sent to user emails during signup
- **Responsive UI:** Clean and user-friendly interface accessible on multiple devices

---

## Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **Database:** MySql
- **Email Service:** Flask-Mail (SMTP for sending activation codes)

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/student-teacher-coding-platform.git
   cd student-teacher-coding-platform
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Setup environment variables in a .env file:
   ```bash
    FLASK_APP=app.py
    FLASK_ENV=development
    SECRET_KEY=your_secret_key
    MAIL_SERVER=smtp.gmail.com
    MAIL_PORT=587
    MAIL_USERNAME=your_email@gmail.com
    MAIL_PASSWORD=your_email_password_or_app_password
   ```
5. Initialize the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```
6. Run the application:
   ```bash
   flask run
   ```
___
## Usage
Teachers can register, create coding problems, and manage them.

Students can register, verify accounts via email, and solve coding problems.

Code editor disables copy-paste, drag-and-drop, and split-screen for exam integrity.

Results and submissions are visible on personalized dashboards.

Folder Structure
```cshape
├── app.py              # Main application
├── models.py           # Database models
├── routes.py           # Routes and views
├── templates/          # HTML templates
├── static/             # CSS, JS, images
├── utils/              # Helper functions (email, code execution, etc.)
├── migrations/         # Database migration files
├── requirements.txt    # Python dependencies
└── README.md           # This file
```
___
Contributing
Contributions are welcome! Please:

## License

This project is licensed under the [MIT License](LICENSE).  
Feel free to use and adapt it as needed.
