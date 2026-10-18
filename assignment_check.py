"""
ASSIGNMENT SUBMISSION PORTAL
Diploma Python GUI Micro Project
Technology: Python, Tkinter, JSON, File Handling

Default demonstration teacher password: 1234
Change TEACHER_PASSWORD before using the project beyond classroom demonstration.
"""

import json
import shutil
import uuid
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from datetime import datetime

# -------------------- CONFIGURATION --------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "assignments.json"
UPLOAD_DIR = BASE_DIR / "uploads"
TEACHER_PASSWORD = "1234"
MAX_MARKS = 100

UPLOAD_DIR.mkdir(exist_ok=True)


# -------------------- DATA HANDLING --------------------

def load_data():
    """Read assignment records from the JSON file."""
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        messagebox.showerror(
            "Data Error",
            "The assignment database could not be read. "
            "Check assignments.json."
        )
        return []


def save_data(records):
    """Save assignment records to the JSON file."""
    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(records, file, indent=4, ensure_ascii=False)
        return True
    except OSError as error:
        messagebox.showerror("Save Error", f"Could not save records:\n{error}")
        return False


# -------------------- MAIN APPLICATION --------------------

class AssignmentPortal:
    def __init__(self, root):
        self.root = root
        self.root.title("Assignment Submission Portal")
        self.root.geometry("900x650")
        self.root.minsize(760, 560)

        self.selected_file = ""
        self.teacher_authenticated = False

        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        self.style.configure("Title.TLabel", font=("Arial", 19, "bold"))
        self.style.configure("Subtitle.TLabel", font=("Arial", 10))
        self.style.configure("Treeview", rowheight=27)

        self.create_interface()
        self.refresh_teacher_table()

    def create_interface(self):
        header = ttk.Frame(self.root, padding=(18, 14))
        header.pack(fill="x")

        ttk.Label(
            header, text="ASSIGNMENT SUBMISSION PORTAL",
            style="Title.TLabel"
        ).pack(anchor="center")

        ttk.Label(
            header,
            text="A Python GUI system for student submissions and teacher grading",
            style="Subtitle.TLabel"
        ).pack(anchor="center", pady=(5, 0))

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=16, pady=10)

        self.student_tab = ttk.Frame(self.notebook, padding=20)
        self.teacher_tab = ttk.Frame(self.notebook, padding=15)
        self.result_tab = ttk.Frame(self.notebook, padding=20)

        self.notebook.add(self.student_tab, text="Student Submission")
        self.notebook.add(self.teacher_tab, text="Teacher Dashboard")
        self.notebook.add(self.result_tab, text="Check Result")

        self.create_student_tab()
        self.create_teacher_tab()
        self.create_result_tab()

        footer = ttk.Label(
            self.root,
            text="Python Micro Project | Local demonstration version",
            anchor="center"
        )
        footer.pack(fill="x", pady=(0, 8))

    # -------------------- STUDENT TAB --------------------

    def create_student_tab(self):
        ttk.Label(
            self.student_tab, text="Submit Your Assignment",
            font=("Arial", 15, "bold")
        ).pack(anchor="w", pady=(0, 15))

        form = ttk.Frame(self.student_tab)
        form.pack(fill="x")

        self.student_name = tk.StringVar()
        self.roll_number = tk.StringVar()
        self.subject_name = tk.StringVar()
        self.file_label = tk.StringVar(value="No file selected")

        fields = [
            ("Student Name:", self.student_name),
            ("Roll Number:", self.roll_number),
            ("Subject Name:", self.subject_name),
        ]

        for row, (label_text, variable) in enumerate(fields):
            ttk.Label(form, text=label_text).grid(
                row=row, column=0, sticky="w", padx=(0, 12), pady=9
            )
            ttk.Entry(form, textvariable=variable, width=48).grid(
                row=row, column=1, sticky="ew", pady=9
            )

        form.columnconfigure(1, weight=1)

        ttk.Label(form, text="Assignment File:").grid(
            row=3, column=0, sticky="w", padx=(0, 12), pady=9
        )
        file_frame = ttk.Frame(form)
        file_frame.grid(row=3, column=1, sticky="ew", pady=9)

        ttk.Button(
            file_frame, text="Choose File", command=self.choose_file
        ).pack(side="left")
        ttk.Label(
            file_frame, textvariable=self.file_label, wraplength=420
        ).pack(side="left", padx=10)

        ttk.Button(
            self.student_tab, text="Submit Assignment",
            command=self.submit_assignment
        ).pack(anchor="w", pady=20)

        note = (
            "Instructions:\n"
            "1. Enter your name, roll number and subject.\n"
            "2. Select the assignment file from your device.\n"
            "3. Click Submit Assignment.\n"
            "4. Keep the generated Submission ID for reference."
        )
        ttk.Label(
            self.student_tab, text=note, justify="left"
        ).pack(anchor="w", pady=8)

    def choose_file(self):
        path = filedialog.askopenfilename(
            title="Select Assignment",
            filetypes=[
                ("Documents", "*.pdf *.doc *.docx *.txt *.ppt *.pptx"),
                ("All files", "*.*")
            ]
        )
        if path:
            self.selected_file = path
            self.file_label.set(Path(path).name)

    def submit_assignment(self):
        name = self.student_name.get().strip()
        roll = self.roll_number.get().strip()
        subject = self.subject_name.get().strip()

        if not name or not roll or not subject:
            messagebox.showwarning(
                "Missing Information",
                "Please enter student name, roll number and subject."
            )
            return

        if not self.selected_file or not Path(self.selected_file).is_file():
            messagebox.showwarning(
                "File Required", "Please choose a valid assignment file."
            )
            return

        submission_id = str(uuid.uuid4())[:8].upper()
        original_name = Path(self.selected_file).name
        safe_name = f"{submission_id}_{original_name}"
        destination = UPLOAD_DIR / safe_name

        try:
            shutil.copy2(self.selected_file, destination)
        except OSError as error:
            messagebox.showerror(
                "Upload Error", f"Could not copy the selected file:\n{error}"
            )
            return

        records = load_data()
        record = {
            "id": submission_id,
            "name": name,
            "roll": roll,
            "subject": subject,
            "file": str(destination),
            "original_file": original_name,
            "submitted_on": datetime.now().strftime("%d-%m-%Y %H:%M"),
            "marks": None,
            "feedback": "Not graded"
        }
        records.append(record)

        if save_data(records):
            messagebox.showinfo(
                "Submission Successful",
                f"Your assignment has been submitted.\n"
                f"Submission ID: {submission_id}"
            )
            self.student_name.set("")
            self.roll_number.set("")
            self.subject_name.set("")
            self.selected_file = ""
            self.file_label.set("No file selected")
            self.refresh_teacher_table()

    # -------------------- TEACHER TAB --------------------

    def create_teacher_tab(self):
        top = ttk.Frame(self.teacher_tab)
        top.pack(fill="x", pady=(0, 10))

        ttk.Label(
            top, text="Teacher Dashboard",
            font=("Arial", 15, "bold")
        ).pack(side="left")

        self.login_button = ttk.Button(
            top, text="Teacher Login", command=self.teacher_login
        )
        self.login_button.pack(side="right")

        columns = ("id", "name", "roll", "subject", "date", "marks")
        self.assignment_table = ttk.Treeview(
            self.teacher_tab, columns=columns, show="headings", height=10
        )

        headings = {
            "id": "Submission ID",
            "name": "Student",
            "roll": "Roll No.",
            "subject": "Subject",
            "date": "Submitted On",
            "marks": "Marks"
        }
        widths = {
            "id": 105, "name": 130, "roll": 80,
            "subject": 120, "date": 135, "marks": 70
        }

        for column in columns:
            self.assignment_table.heading(column, text=headings[column])
            self.assignment_table.column(
                column, width=widths[column], anchor="center"
            )

        self.assignment_table.pack(fill="both", expand=True, pady=8)
        self.assignment_table.bind(
            "<<TreeviewSelect>>", self.show_selected_assignment
        )

        grading = ttk.LabelFrame(
            self.teacher_tab, text="Grade Selected Assignment", padding=12
        )
        grading.pack(fill="x", pady=8)

        ttk.Label(grading, text="Marks (0-100):").grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )
        self.marks_entry = ttk.Entry(grading, width=12)
        self.marks_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(grading, text="Feedback:").grid(
            row=1, column=0, sticky="w", padx=5, pady=5
        )
        self.feedback_entry = ttk.Entry(grading, width=55)
        self.feedback_entry.grid(
            row=1, column=1, sticky="ew", padx=5, pady=5
        )
        grading.columnconfigure(1, weight=1)

        buttons = ttk.Frame(grading)
        buttons.grid(row=2, column=0, columnspan=2, sticky="w", pady=8)

        ttk.Button(
            buttons, text="Save Grade", command=self.grade_assignment
        ).pack(side="left", padx=(0, 8))
        ttk.Button(
            buttons, text="Open Selected File", command=self.open_selected_file
        ).pack(side="left", padx=8)
        ttk.Button(
            buttons, text="Refresh", command=self.refresh_teacher_table
        ).pack(side="left", padx=8)

        ttk.Label(
            self.teacher_tab,
            text="Teacher login is required before grading. "
                 "Select a row to view and grade a submission.",
            foreground="gray"
        ).pack(anchor="w", pady=(5, 0))

    def teacher_login(self):
        from tkinter import simpledialog

        password = simpledialog.askstring(
            "Teacher Login", "Enter teacher password:", show="*",
            parent=self.root
        )
        if password is None:
            return

        if password == TEACHER_PASSWORD:
            self.teacher_authenticated = True
            self.login_button.configure(text="Logged In")
            messagebox.showinfo("Login Successful", "Teacher access enabled.")
        else:
            messagebox.showerror("Login Failed", "Incorrect teacher password.")

    def refresh_teacher_table(self):
        if not hasattr(self, "assignment_table"):
            return

        for item in self.assignment_table.get_children():
            self.assignment_table.delete(item)

        for record in load_data():
            marks = record.get("marks")
            marks_text = "Pending" if marks is None else str(marks)
            self.assignment_table.insert(
                "", "end",
                values=(
                    record.get("id", ""),
                    record.get("name", ""),
                    record.get("roll", ""),
                    record.get("subject", ""),
                    record.get("submitted_on", ""),
                    marks_text
                )
            )

    def get_selected_record(self):
        selected = self.assignment_table.selection()
        if not selected:
            messagebox.showwarning(
                "Select Assignment", "Please select an assignment from the table."
            )
            return None

        submission_id = self.assignment_table.item(
            selected[0], "values"
        )[0]

        for record in load_data():
            if record.get("id") == submission_id:
                return record
        return None

    def show_selected_assignment(self, _event=None):
        record = self.get_selected_record()
        if not record:
            return

        self.marks_entry.delete(0, tk.END)
        self.feedback_entry.delete(0, tk.END)

        if record.get("marks") is not None:
            self.marks_entry.insert(0, str(record["marks"]))

        self.feedback_entry.insert(
            0, record.get("feedback", "")
        )

    def grade_assignment(self):
        if not self.teacher_authenticated:
            messagebox.showwarning(
                "Login Required", "Please log in as a teacher before grading."
            )
            return

        record = self.get_selected_record()
        if not record:
            return

        try:
            marks = float(self.marks_entry.get().strip())
        except ValueError:
            messagebox.showerror(
                "Invalid Marks", "Enter marks as a number between 0 and 100."
            )
            return

        if not 0 <= marks <= MAX_MARKS:
            messagebox.showerror(
                "Invalid Marks", "Marks must be between 0 and 100."
            )
            return

        feedback = self.feedback_entry.get().strip()
        records = load_data()

        for item in records:
            if item.get("id") == record.get("id"):
                item["marks"] = marks
                item["feedback"] = feedback or "No feedback provided"
                item["graded_on"] = datetime.now().strftime("%d-%m-%Y %H:%M")
                break

        if save_data(records):
            messagebox.showinfo(
                "Grade Saved", "Marks and feedback have been saved successfully."
            )
            self.refresh_teacher_table()

    def open_selected_file(self):
        record = self.get_selected_record()
        if not record:
            return

        file_path = Path(record.get("file", ""))
        if not file_path.is_file():
            messagebox.showerror(
                "File Not Found", "The uploaded assignment file is unavailable."
            )
            return

        try:
            import os
            import sys
            import subprocess

            if sys.platform.startswith("win"):
                os.startfile(str(file_path))
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(file_path)])
            else:
                subprocess.Popen(["xdg-open", str(file_path)])
        except Exception as error:
            messagebox.showerror(
                "Open File Error",
                f"Could not open the file automatically:\n{error}\n\n"
                f"File location: {file_path}"
            )

    # -------------------- RESULT TAB --------------------

    def create_result_tab(self):
        ttk.Label(
            self.result_tab, text="Check Assignment Result",
            font=("Arial", 15, "bold")
        ).pack(anchor="w", pady=(0, 15))

        search_frame = ttk.Frame(self.result_tab)
        search_frame.pack(anchor="w", fill="x")

        ttk.Label(search_frame, text="Enter Roll Number:").pack(side="left")
        self.result_roll = tk.StringVar()
        ttk.Entry(
            search_frame, textvariable=self.result_roll, width=25
        ).pack(side="left", padx=10)

        ttk.Button(
            search_frame, text="Check Result", command=self.check_result
        ).pack(side="left")

        self.result_display = tk.Text(
            self.result_tab, height=14, width=75, wrap="word",
            state="disabled"
        )
        self.result_display.pack(fill="both", expand=True, pady=18)

    def check_result(self):
        roll = self.result_roll.get().strip()
        if not roll:
            messagebox.showwarning(
                "Roll Number Required", "Please enter your roll number."
            )
            return

        matches = [
            record for record in load_data()
            if record.get("roll", "").lower() == roll.lower()
        ]

        self.result_display.configure(state="normal")
        self.result_display.delete("1.0", tk.END)

        if not matches:
            self.result_display.insert(
                tk.END, "No assignment records found for this roll number."
            )
        else:
            for record in matches:
                marks = record.get("marks")
                marks_text = "Pending" if marks is None else str(marks)

                result_text = (
                    f"Student Name : {record.get('name', '')}\n"
                    f"Roll Number  : {record.get('roll', '')}\n"
                    f"Subject      : {record.get('subject', '')}\n"
                    f"Submission ID: {record.get('id', '')}\n"
                    f"Submitted On : {record.get('submitted_on', '')}\n"
                    f"Marks        : {marks_text}\n"
                    f"Feedback     : {record.get('feedback', '')}\n"
                    f"{'-' * 48}\n"
                )
                self.result_display.insert(tk.END, result_text)

        self.result_display.configure(state="disabled")


# -------------------- PROGRAM ENTRY POINT --------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = AssignmentPortal(root)
    root.mainloop()