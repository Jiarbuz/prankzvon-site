from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import json, os

app = Flask(__name__)
app.secret_key = 'super-secret-key'

ADMIN_USERNAME = "Bes689"
ADMIN_PASSWORD_HASH = generate_password_hash("Feea2209G")
DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

@app.route("/")
def index():
    return render_template("index.html", channels=load_data())

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form["username"] == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, request.form["password"]):
            session["logged_in"] = True
            return redirect(url_for("admin"))
        error = "Неверный логин или пароль"
    return render_template("login.html", error=error)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    channels = load_data()
    if request.method == "POST":
        channels.append({
            "title": request.form["title"],
            "link": request.form["link"],
            "desc": request.form["desc"],
            "avatar": request.form["avatar"]
        })
        save_data(channels)
        return redirect(url_for("admin"))
    return render_template("admin.html", channels=channels)

@app.route("/delete/<int:index>")
def delete(index):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    channels = load_data()
    if 0 <= index < len(channels):
        del channels[index]
        save_data(channels)
    return redirect(url_for("admin"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)