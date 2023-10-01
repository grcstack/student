# Import necessary modules
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import date

# Create a Flask app
app = Flask(__name__)
app.secret_key = "your_secret_key"

# Sample user data (you should implement a proper user authentication system)
users = {
    "admin": "password"
}

# Class to represent a student
class Student:
    def __init__(self, roll_no, name):
        self.roll_no = roll_no
        self.name = name
        self.attendance = []

    def mark_attendance(self):
        today = date.today()
        self.attendance.append(today.strftime("%Y-%m-%d"))

    def view_attendance(self):
        return self.attendance

students = {}

# Define routes and views
@app.route("/")
def home():
    if 'username' in session:
        return render_template("index.html", username=session['username'])
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for("home"))
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html", error=None)

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for("home"))

@app.route("/add_student", methods=["GET", "POST"])
def add_student():
    if 'username' not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        roll_no = request.form["roll_no"]
        name = request.form["name"]
        student = Student(roll_no, name)
        students[roll_no] = student
        return redirect(url_for("home"))
    return render_template("add_student.html")

@app.route("/mark_attendance", methods=["GET", "POST"])
def mark_attendance():
    if 'username' not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        roll_no = request.form["roll_no"]
        if roll_no in students:
            student = students[roll_no]
            student.mark_attendance()
            return redirect(url_for("home"))
        else:
            return render_template("mark_attendance.html", error="Invalid Roll No.")
    return render_template("mark_attendance.html", error=None)

@app.route("/view_attendance", methods=["GET", "POST"])
def view_attendance():
    if 'username' not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        roll_no = request.form["roll_no"]
        if roll_no in students:
            student = students[roll_no]
            attendance = student.view_attendance()
            return render_template("view_attendance.html", student=student, attendance=attendance)
        else:
            return render_template("view_attendance.html", error="Invalid Roll No.")
    return render_template("view_attendance.html", error=None)

if __name__ == "__main__":
    app.run(debug=True)
