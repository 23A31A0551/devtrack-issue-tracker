from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "devtrack-demo-key"
DB = Path(__file__).with_name("devtrack.db")

def connect():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    with connect() as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT DEFAULT '',
            project TEXT DEFAULT 'General',
            assignee TEXT DEFAULT '',
            priority TEXT NOT NULL DEFAULT 'Medium',
            status TEXT NOT NULL DEFAULT 'To Do',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
        count = con.execute("SELECT COUNT(*) FROM issues").fetchone()[0]
        if count == 0:
            con.executemany("""INSERT INTO issues(title,description,project,assignee,priority,status)
            VALUES(?,?,?,?,?,?)""", [
                ("Login page validation", "Show a clear message for invalid credentials.", "Web Portal", "Asha", "High", "In Progress"),
                ("Add task search", "Allow users to search by title and assignee.", "DevTrack", "Rahul", "Medium", "To Do"),
                ("Fix dashboard layout", "Ensure cards fit on mobile screens.", "DevTrack", "Maya", "Low", "Done")
            ])

@app.route("/")
def index():
    status = request.args.get("status", "")
    q = request.args.get("q", "").strip()
    sql = "SELECT * FROM issues WHERE 1=1"
    args = []
    if status:
        sql += " AND status=?"; args.append(status)
    if q:
        sql += " AND (title LIKE ? OR project LIKE ? OR assignee LIKE ?)"
        args.extend([f"%{q}%"]*3)
    sql += " ORDER BY created_at DESC, id DESC"
    with connect() as con:
        issues = con.execute(sql, args).fetchall()
        totals = {s: con.execute("SELECT COUNT(*) FROM issues WHERE status=?", (s,)).fetchone()[0]
                  for s in ["To Do", "In Progress", "Done"]}
    return render_template("index.html", issues=issues, totals=totals, status=status, q=q)

@app.route("/new", methods=["GET", "POST"])
def new_issue():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        if not title:
            flash("Title is required.", "error")
            return redirect(url_for("new_issue"))
        with connect() as con:
            con.execute("""INSERT INTO issues(title,description,project,assignee,priority,status)
            VALUES(?,?,?,?,?,?)""", (
                title, request.form.get("description","").strip(),
                request.form.get("project","General").strip() or "General",
                request.form.get("assignee","").strip(),
                request.form.get("priority","Medium"),
                request.form.get("status","To Do")))
        flash("Issue created.", "success")
        return redirect(url_for("index"))
    return render_template("form.html", issue=None)

@app.route("/edit/<int:issue_id>", methods=["GET", "POST"])
def edit_issue(issue_id):
    with connect() as con:
        issue = con.execute("SELECT * FROM issues WHERE id=?", (issue_id,)).fetchone()
        if not issue:
            flash("Issue not found.", "error")
            return redirect(url_for("index"))
        if request.method == "POST":
            title = request.form.get("title", "").strip()
            if not title:
                flash("Title is required.", "error")
                return redirect(url_for("edit_issue", issue_id=issue_id))
            con.execute("""UPDATE issues SET title=?,description=?,project=?,assignee=?,priority=?,status=?
            WHERE id=?""", (
                title, request.form.get("description","").strip(),
                request.form.get("project","General").strip() or "General",
                request.form.get("assignee","").strip(),
                request.form.get("priority","Medium"),
                request.form.get("status","To Do"), issue_id))
            flash("Issue updated.", "success")
            return redirect(url_for("index"))
    return render_template("form.html", issue=issue)

@app.route("/delete/<int:issue_id>", methods=["POST"])
def delete_issue(issue_id):
    with connect() as con:
        con.execute("DELETE FROM issues WHERE id=?", (issue_id,))
    flash("Issue deleted.", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
