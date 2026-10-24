from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "edulearn_secret_key"

def get_db():
    conn = sqlite3.connect("edulearn.db")
    conn.row_factory = sqlite3.Row
    return conn
@app.route("/")
def home():
    return redirect("/admin")

def create_table():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            quiz_score INTEGER DEFAULT 0,
            python_progress INTEGER DEFAULT 0,
            web_progress INTEGER DEFAULT 0,
            data_progress INTEGER DEFAULT 0
        )
    """)

    columns = [row["name"] for row in conn.execute("PRAGMA table_info(students)")]

    if "python_progress" not in columns:
        conn.execute("ALTER TABLE students ADD COLUMN python_progress INTEGER DEFAULT 0")

    if "web_progress" not in columns:
        conn.execute("ALTER TABLE students ADD COLUMN web_progress INTEGER DEFAULT 0")

    if "data_progress" not in columns:
        conn.execute("ALTER TABLE students ADD COLUMN data_progress INTEGER DEFAULT 0")

    conn.commit()
    conn.close()
    
create_table()
@app.route("/quiz", methods=["GET", "POST"])
def quiz():

    if "student_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        score = request.form["score"]

        conn = get_db()

        conn.execute(
            "UPDATE students SET quiz_score = ? WHERE id = ?",
            (score, session["student_id"])
        )

        conn.commit()
        conn.close()

        return redirect("/progress")

    return render_template("quiz.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()

        student = conn.execute(
            "SELECT * FROM students WHERE email = ? AND password = ?",
            (email, password)
        ).fetchone()

        conn.close()

        if student:
            session["student_id"] = student["id"]
            session["student_name"] = student["name"]
            session["student_email"] = student["email"]

            return redirect("/dashboard")

        return "Invalid Email or Password"

    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()

        conn.execute(
            "INSERT INTO students (name, email, password) VALUES (?, ?, ?)",
            (name, email, password)
        )

        conn.commit()
        conn.close()

        return "Signup successful!"

    return render_template("signup.html")

@app.route("/dashboard")
def dashboard():

    if "student_id" not in session:
        return redirect("/login")

    conn = get_db()

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (session["student_id"],)
    ).fetchone()

    conn.close()

    return render_template("dashboard.html", student=student)
@app.route("/admin")
def admin():

    conn = get_db()

    students = conn.execute(
        "SELECT id, name, email, python_progress, web_progress, data_progress, quiz_score FROM students"
    ).fetchall()

    conn.close()

    return render_template("admin.html", students=students)
@app.route("/admin/register", methods=["GET", "POST"])
def admin_register():

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()

        conn.execute(
            "INSERT INTO students (name, email, password) VALUES (?, ?, ?)",
            (name, email, password)
        )

        conn.commit()
        conn.close()

        return redirect("/admin")

    return render_template("admin_register.html")

@app.route("/python")
def python():
    return render_template("python.html")

@app.route("/python-introduction")
def python_introduction():
    return render_template("python-introduction.html")


@app.route("/complete-python/<int:progress>")
def complete_python(progress):

    if "student_id" not in session:
        return redirect("/login")

    conn = get_db()

    conn.execute(
        "UPDATE students SET python_progress = ? WHERE id = ?",
        (progress, session["student_id"])
    )

    conn.commit()
    conn.close()

    return redirect("/progress")

@app.route("/python-variables")
def python_variables():
    return render_template("python-variables.html")

@app.route("/python-operators")
def python_operators():
    return render_template("python-operators.html")

@app.route("/python-conditions")
def python_conditions():
    return render_template("python-conditions.html")

@app.route("/python-loops")
def python_loops():
    return render_template("python-loops.html")

@app.route("/python-functions")
def python_functions():
    return render_template("python-function.html")

@app.route("/python-list")
def python_list():
    return render_template("python-list.html")

@app.route("/python-tuples")
def python_tuples():
    return render_template("python-tuples.html")

@app.route("/python-dictionaries")
def python_dictionaries():
    return render_template("python-dictionaries.html")

@app.route("/python-classes")
def python_classes():
    return render_template("python-classes.html")

@app.route("/python-inheritance")
def python_inheritance():
    return render_template("python-inheritance.html")

@app.route("/web")
def web():
    return render_template("web.html")
@app.route("/complete-web/<int:progress>")
def complete_web(progress):

    if "student_id" not in session:
        return redirect("/login")

    conn = get_db()

    conn.execute(
        "UPDATE students SET web_progress = ? WHERE id = ?",
        (progress, session["student_id"])
    )

    conn.commit()
    conn.close()

    return redirect("/progress")

@app.route("/data-analytics")
def data_analytics():
    return render_template("data-analytics.html")
@app.route("/complete-data/<int:progress>")
def complete_data(progress):

    if "student_id" not in session:
        return redirect("/login")

    conn = get_db()

    conn.execute(
        "UPDATE students SET data_progress = ? WHERE id = ?",
        (progress, session["student_id"])
    )

    conn.commit()
    conn.close()

    return redirect("/progress")

@app.route("/progress")
def progress():

    if "student_id" not in session:
        return redirect("/login")

    conn = get_db()

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (session["student_id"],)
    ).fetchone()

    conn.close()

    return render_template("progress.html", student=student)

@app.route("/profile")
def profile():
    if "student_id" not in session:
        return redirect("/login")

    conn = get_db()

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (session["student_id"],)
    ).fetchone()

    conn.close()

    return render_template("profile.html", student=student)



@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/admin/dashboard")
def admin_dashboard():
    return render_template("admin_dashboard.html")


@app.route("/admin/students")
def admin_students():
    conn = get_db()
    students = conn.execute("""
    SELECT id, name, email, quiz_score,
           python_progress, web_progress, data_progress
    FROM students
""").fetchall()
    conn.close()

    return render_template("admin_student.html", students=students)
@app.route("/admin/delete/<int:student_id>")
def delete_student(student_id):
    conn = get_db()

    conn.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/admin/students")
@app.route("/admin/edit/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):

    conn = get_db()

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        quiz_score = request.form["quiz_score"]

        conn.execute("""
            UPDATE students
            SET name = ?, email = ?, password = ?, quiz_score = ?
            WHERE id = ?
        """, (name, email, password, quiz_score, student_id))

        conn.commit()
        conn.close()

        return redirect("/admin/students")

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    ).fetchone()

    conn.close()

    return render_template("edit_student.html", student=student)


if __name__ == "__main__":
    app.run(debug=True)