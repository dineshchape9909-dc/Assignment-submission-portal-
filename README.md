### Assignment Submission Portal

A lightweight, local Python desktop application designed as a GUI Micro Project. It serves as a simplified, offline learning management system that bridges student submissions and teacher grading within a single interface. 

### 🚀 Features

### 👨‍🎓 Student Submission Tab

* **Form Inputs:** Collects student Name, Roll Number, and Subject.
* **File Uploads:** Supports document uploads including .pdf, .doc, .docx, .txt, .ppt, and .pptx.
* **Unique Tracking:** Automatically generates a distinct 8-character alphanumeric Submission ID using uuid.

### 👩‍🏫 Teacher Dashboard

* **Secure Access:** Features a password-protected login to prevent unauthorized grading.
* **Centralized Database:** Displays a structured table of all student entries.
* **File Viewer:** Open and review submitted student files natively right from the app dashboard.
* **Interactive Evaluation:** Teachers can input numerical marks (0-100) and custom text feedback.

### 📊 Result Checker Tab

* **Instant Status Updates:** Students can query the system using their Roll Number to see their evaluation status, marks, and feedback.

### 💾 Local Data Handling

* Uses a local JSON file (assignments.json) as a flat-file database to persist submission records and timestamps across application restarts.
* Saves copies of all student work automatically into a dedicated local uploads/ folder.

### 🛠️ Technology Stack

* **Language:** Python
* **GUI Framework:** Tkinter & TTK
* **Data Storage:** JSON
* **File Operations:** Built-in shutil, pathlib, and uuid modules

### 💻 Installation & Setup

### Prerequisites

Make sure you have Python installed on your computer. 

### Step-by-Step Run Guide

1. Download or clone this repository to your local machine.
2. Open your terminal, command prompt, or terminal app.
3. Navigate to the project directory: 


cd Assignment-Submission-Portal

Use code with caution.
4. Run the application: 


python assignment_check.py

Use code with caution.

### 🔒 Security Configuration

* **Default Teacher Password:** 1234
* **Warning:** If you plan to deploy or use this application beyond a local classroom demonstration, open the code file and modify the TEACHER_PASSWORD variable at the top configuration section to a secure string.

### 📝 License

This project is open-source and available under the MIT License. Feel free to use, modify, and distribute it for academic or demonstration purposes.
