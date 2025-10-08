from flask import Flask, render_template, request, redirect, url_for, session, flash
from ai_utils import granite_generate_response, analyze_sentiment
import sqlite3, os 

app = Flask(__name__)
app.secret_key = "supersecret"

# ---------------- DATABASE ----------------
def init_db():
    if not os.path.exists("users.db"):
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute('''CREATE TABLE users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        reg_id TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL
                    )''')
        conn.commit()
        conn.close()

# ---------------- IN-MEMORY STORAGE ----------------
chat_history = []
feedback_data = []
citizen_issues = []

# ---------------- ROUTES ----------------
@app.route("/")
def base():
    return render_template("base.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/services")
def services():
    return render_template("services.html")

# ---- Chat (Protected) ----
@app.route("/chat")
def chat():
    if "user" not in session:
        flash("Please login first to access the chat.", "warning")
        return redirect(url_for("login"))
    return render_template("chat.html", history=chat_history)

# ---- AI Assistant (Ask Question) ----
@app.route("/ask", methods=["POST"])
def ask_question():
    if "user" not in session:
        flash("You must login first.", "warning")
        return redirect(url_for("login"))

    question = request.form.get("user_input", "").strip()
    if not question:
        return render_template("chat.html", history=chat_history, error="Question cannot be empty.")

    try:
        response = granite_generate_response(question)
    except Exception as e:
        response = f"Error generating response: {e}"

    chat_history.append({"question": question, "answer": response})

    try:
        sentiment = analyze_sentiment(response)
    except Exception:
        sentiment = "neutral"

    feedback_data.append({"feedback": response, "sentiment": sentiment})
    citizen_issues.append(f"Q: {question} → AI: {response} ({sentiment})")

    return render_template("chat.html", history=chat_history, question=question, response=response, sentiment=sentiment)

# ---- Feedback (Protected) ----
@app.route("/feedback", methods=["POST"])
def submit_feedback():
    if "user" not in session:
        flash("You must login first.", "warning")
        return redirect(url_for("login"))

    feedback_text = request.form.get("feedback", "").strip()
    if not feedback_text:
        return render_template("chat.html", history=chat_history, error="Feedback cannot be empty.")

    try:
        sentiment = analyze_sentiment(feedback_text)
    except Exception:
        sentiment = "neutral"

    feedback_data.append({"feedback": feedback_text, "sentiment": sentiment})
    citizen_issues.append(f"Feedback: {feedback_text} ({sentiment})")

    return render_template("chat.html", history=chat_history, feedback=feedback_text, sentiment=sentiment)

# ---- Concern Reporting (Protected) ----
@app.route("/concern", methods=["POST"])
def concern():
    if "user" not in session:
        flash("You must login first.", "warning")
        return redirect(url_for("login"))

    concern_text = request.form.get("concern", "").strip()
    if not concern_text:
        return render_template("chat.html", history=chat_history, error="Concern cannot be empty.")

    citizen_issues.append(f"Concern: {concern_text}")

    return render_template("chat.html", history=chat_history, concern=concern_text, concern_response="Your concern has been recorded successfully.")

# ---- Dashboard (Protected) ----
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        flash("Please login to view the dashboard.", "warning")
        return redirect(url_for("login"))

    pos = sum(1 for f in feedback_data if "positive" in f["sentiment"].lower())
    neg = sum(1 for f in feedback_data if "negative" in f["sentiment"].lower())
    neu = sum(1 for f in feedback_data if "neutral" in f["sentiment"].lower())

    sentiment_counts = {"positive": pos, "negative": neg, "neutral": neu}
    recent_issues = list(reversed(citizen_issues[-10:]))

    return render_template("dashboard.html", sentiment_counts=sentiment_counts, recent_issues=recent_issues)

# ---- Register ----
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        reg_id = request.form["reg_id"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (name, email, reg_id, password) VALUES (?, ?, ?, ?)", (name, email, reg_id, password))
            conn.commit()
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Registration ID already exists. Please choose another.", "danger")
        conn.close()
    return render_template("register.html")

# ---- Login ----
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        reg_id = request.form["reg_id"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE reg_id = ? AND password = ?", (reg_id, password))
        user = c.fetchone()
        conn.close()

        if user:
            session["user"] = user[1]  # Save name in session
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid Login! Please try again.", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")

# ---- Logout ----
@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("base"))

# ---------------- MAIN ----------------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
