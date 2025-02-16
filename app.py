from flask import Flask, redirect, url_for, session, request, render_template
import msal
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Azure AD Credentials
CLIENT_ID = "your_client_id"
TENANT_ID = "your_tenant_id"
CLIENT_SECRET = "your_client_secret"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
REDIRECT_URI = "http://localhost:5000/getToken" # Update this with your Redirect URI if you do not deploy locally
SCOPES = ["User.Read"]

# MSAL Config
msal_app = msal.ConfidentialClientApplication(CLIENT_ID, CLIENT_SECRET, AUTHORITY)

# Simple In-Memory DB (SQLite)
DB_FILE = "tasks.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, user TEXT, task TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    if "user" in session:
        return render_template("home.html", name=session["user"]["name"])
    return "<a href='/login'>Login with Azure AD</a>"

@app.route("/login")
def login():
    auth_url = msal_app.get_authorization_request_url(SCOPES, redirect_uri=REDIRECT_URI)
    return redirect(auth_url)

@app.route("/getToken")
def get_token():
    code = request.args.get("code")
    if not code:
        return "No authorization code received!"
    
    token_response = msal_app.acquire_token_by_authorization_code(code, SCOPES, redirect_uri=REDIRECT_URI)
    if "id_token_claims" in token_response:
        session["user"] = {
            "name": token_response["id_token_claims"]["name"],
            "email": token_response["id_token_claims"]["preferred_username"],
        }
        return redirect(url_for("tasks"))
    
    return "Login failed!"

@app.route("/tasks")
def tasks():
    if "user" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # If user is Admin (Hardcoded check for now)
    admin_users = ["admin@example.com"]  # Replace with actual Admins
    if session["user"]["email"] in admin_users:
        c.execute("SELECT * FROM tasks")
    else:
        c.execute("SELECT * FROM tasks WHERE user = ?", (session["user"]["email"],))
    
    user_tasks = c.fetchall()
    conn.close()

    return render_template("tasks.html", tasks=user_tasks, user=session["user"])

@app.route("/add", methods=["POST"])
def add_task():
    if "user" not in session:
        return redirect(url_for("login"))

    task = request.form["task"]
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO tasks (user, task) VALUES (?, ?)", (session["user"]["email"], task))
    conn.commit()
    conn.close()

    return redirect(url_for("tasks"))

@app.route("/delete/<int:id>")
def delete_task(id):
    if "user" not in session:
        return redirect(url_for("login"))

    admin_users = ["admin@example.com"]  # Replace with actual Admins
    if session["user"]["email"] not in admin_users:
        return "Unauthorized", 403

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for("tasks"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)

