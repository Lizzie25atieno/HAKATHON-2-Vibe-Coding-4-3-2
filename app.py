from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import config  # your config.py with SECRET_KEY and DB credentials

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

# DB Connection 
def get_db_connection():
    return mysql.connector.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME
    )

# Home / Index 
@app.route("/")
def index():
    if session.get("user_id"):
        return redirect(url_for("dashboard"))
    return render_template("index.html")

# Register 
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s,%s,%s)",
                           (username, email, password))
            conn.commit()
            flash("Account created successfully!", "success")
            return redirect(url_for("login"))
        except mysql.connector.IntegrityError:
            flash("Username or email already exists.", "danger")
        finally:
            cursor.close()
            conn.close()
    return render_template("register.html")

# Login 
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            # Check premium (if you add premium field later)
            session["is_premium"] = False
            flash("Logged in successfully.", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials.", "danger")
    return render_template("login.html")

# Logout 
@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))

# Dashboard
@app.route("/dashboard")
def dashboard():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students WHERE user_id=%s", (session["user_id"],))
    profile = cursor.fetchone()
    profile_exists = bool(profile)
    cursor.close()
    conn.close()
    return render_template("dashboard.html", username=session["username"], profile_exists=profile_exists)

# Profile
@app.route("/profile", methods=["GET", "POST"])
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == "POST":
        course = request.form["course"]
        skills = request.form.get("skills", "")
        university = request.form.get("university", "")
        cursor.execute("SELECT * FROM students WHERE user_id=%s", (session["user_id"],))
        existing = cursor.fetchone()
        if existing:
            cursor.execute(
                "UPDATE students SET course=%s, skills=%s, university=%s WHERE user_id=%s",
                (course, skills, university, session["user_id"])
            )
            flash("Profile updated.", "success")
        else:
            cursor.execute(
                "INSERT INTO students (user_id, course, skills, university) VALUES (%s,%s,%s,%s)",
                (session["user_id"], course, skills, university)
            )
            flash("Profile created.", "success")
        conn.commit()
    cursor.execute("SELECT * FROM students WHERE user_id=%s", (session["user_id"],))
    profile = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template("profile.html", profile=profile)

# Find Buddy
@app.route("/match", methods=["GET", "POST"])
def match():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students WHERE user_id=%s", (session["user_id"],))
    me = cursor.fetchone()
    filter_by = request.form.get("filter") if request.method == "POST" else "course"

    if filter_by == "course":
        cursor.execute("SELECT s.*, u.username, u.id FROM students s JOIN users u ON s.user_id=u.id WHERE s.course=%s AND s.user_id!=%s",
                       (me["course"], session["user_id"]))
    elif filter_by == "university":
        cursor.execute("SELECT s.*, u.username, u.id FROM students s JOIN users u ON s.user_id=u.id WHERE s.university=%s AND s.user_id!=%s",
                       (me["university"], session["user_id"]))
    elif filter_by == "skills":
        cursor.execute("SELECT s.*, u.username, u.id FROM students s JOIN users u ON s.user_id=u.id WHERE s.skills LIKE %s AND s.user_id!=%s",
                       (f"%{me['skills']}%", session["user_id"]))
    matches = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("match.html", matches=matches)

# Send Buddy Request 
@app.route("/send_request", methods=["POST"])
def send_request():
    if not session.get("user_id"):
        return redirect(url_for("login"))
    receiver_id = request.form["receiver_id"]
    conn = get_db_connection()
    cursor = conn.cursor()
    # Check existing request
    cursor.execute("SELECT * FROM buddy_requests WHERE sender_id=%s AND receiver_id=%s", (session["user_id"], receiver_id))
    if cursor.fetchone():
        flash("You already sent a request.", "warning")
    else:
        cursor.execute("INSERT INTO buddy_requests (sender_id, receiver_id) VALUES (%s,%s)", (session["user_id"], receiver_id))
        conn.commit()
        flash("Buddy request sent!", "success")
    cursor.close()
    conn.close()
    return redirect(url_for("match"))

# Buddy Requests Page 
@app.route("/requests", methods=["GET"])
def requests_page():
    if not session.get("user_id"):
        return redirect(url_for("login"))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT br.id, u.username AS sender_name, br.status
        FROM buddy_requests br
        JOIN users u ON br.sender_id = u.id
        WHERE br.receiver_id=%s
    """, (session["user_id"],))
    received = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("requests.html", received=received)

# Respond to Buddy Request 
@app.route("/respond_request", methods=["POST"])
def respond_request():
    if not session.get("user_id"):
        return redirect(url_for("login"))
    request_id = request.form["request_id"]
    action = request.form["action"]
    conn = get_db_connection()
    cursor = conn.cursor()
    if action == "accept":
        cursor.execute("UPDATE buddy_requests SET status='accepted' WHERE id=%s", (request_id,))
        flash("Buddy request accepted.", "success")
    elif action == "decline":
        cursor.execute("UPDATE buddy_requests SET status='declined' WHERE id=%s", (request_id,))
        flash("Buddy request declined.", "info")
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("requests_page"))

# My Buddies 
@app.route("/messages")
def messages():
    if not session.get("user_id"):
        return redirect(url_for("login"))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT u.id, u.username
        FROM users u
        JOIN buddy_requests br ON
        (br.sender_id=u.id AND br.receiver_id=%s AND br.status='accepted')
        OR (br.receiver_id=u.id AND br.sender_id=%s AND br.status='accepted')
    """, (session["user_id"], session["user_id"]))
    buddies = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("buddies.html", buddies=buddies)

# Chat 
@app.route("/chat/<int:buddy_id>", methods=["GET", "POST"])
def chat(buddy_id):
    if not session.get("user_id"):
        return redirect(url_for("login"))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        content = request.form["content"]
        cursor.execute("INSERT INTO messages (sender_id, receiver_id, content) VALUES (%s,%s,%s)",
                       (session["user_id"], buddy_id, content))
        conn.commit()

    cursor.execute("SELECT username FROM users WHERE id=%s", (buddy_id,))
    buddy = cursor.fetchone()

    cursor.execute("""
        SELECT m.*, u.username AS sender
        FROM messages m
        JOIN users u ON m.sender_id = u.id
        WHERE (m.sender_id=%s AND m.receiver_id=%s) OR (m.sender_id=%s AND m.receiver_id=%s)
        ORDER BY m.created_at ASC
    """, (session["user_id"], buddy_id, buddy_id, session["user_id"]))
    chat_history = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("chat.html", buddy=buddy, chat_history=chat_history)

# Lecturers 
@app.route("/lecturers")
def lecturers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM lecturers")
    lecturers = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("lecturers.html", lecturers=lecturers, premium=session.get("is_premium", False))

# Exercises 
@app.route("/exercises")
def exercises():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM exercises")
    exercises = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("exercises.html", exercises=exercises, premium=session.get("is_premium", False))

# Companies / Internships 
@app.route("/companies")
def companies():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM companies")
    companies = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("companies.html", companies=companies, premium=session.get("is_premium", False))

# Tools 
@app.route("/tools")
def tools():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tools")  
    resources = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("tools.html", resources=resources)

# Premium Upgrade Placeholder
@app.route("/upgrade")
def upgrade():
    flash("Upgrade feature is not implemented yet.", "info")
    return redirect(url_for("dashboard"))

# Run App
import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
