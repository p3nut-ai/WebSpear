# sqli_app.py
import os, sqlite3
from flask import Flask, request, render_template_string

DB_PATH = "lab.db"
app = Flask(__name__)

def init_db():
    fresh = not os.path.exists(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if fresh:
        c.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, password TEXT)")
        c.execute("INSERT INTO users (name, password) VALUES ('admin','admin123')")
        c.execute("INSERT INTO users (name, password) VALUES ('alice','alicepass')")
        c.execute("INSERT INTO users (name, password) VALUES ('bob','bobpass')")
        c.execute("CREATE TABLE products (id INTEGER PRIMARY KEY, title TEXT, price REAL)")
        c.executemany("INSERT INTO products (title, price) VALUES (?,?)",
                      [("Hoodie",49.99), ("Sticker Pack",4.99), ("USB Trinket",19.99)])
        conn.commit()
    conn.close()

HOME = """
<!doctype html>
<title>SQLi Demo</title>
<h1>SQL Injection Playground (SQLite)</h1>

<h2>Search by name (vulnerable)</h2>
<form method="get" action="/user">
  <input name="name" placeholder="e.g., alice">
  <button type="submit">Search</button>
</form>

<h2>Login (vulnerable)</h2>
<form method="post" action="/login">
  <input name="name" placeholder="e.g., admin">
  <input name="password" placeholder="e.g., admin123">
  <button type="submit">Login</button>
</form>

<h2>Product by id (vulnerable)</h2>
<form method="get" action="/product">
  <input name="id" placeholder="1">
  <button type="submit">View</button>
</form>
"""

@app.get("/")
def index():
    return HOME

@app.get("/user")
def user_search():
    name = request.args.get("name", "")
    # VULNERABLE: unsafely concatenated string into SQL
    q = f"SELECT id, name FROM users WHERE name = '{name}'"
    rows = query(q)
    items = "<br>".join([f"id={r[0]} name={r[1]}" for r in rows]) or "(no rows)"
    return f"<h1>Query:</h1><pre>{q}</pre><h2>Result</h2><p>{items}</p><p><a href='/'>Home</a></p>"

@app.post("/login")
def login():
    name = request.form.get("name", "")
    password = request.form.get("password", "")
    # VULNERABLE: classic login bypass
    q = f"SELECT id, name FROM users WHERE name = '{name}' AND password = '{password}'"
    rows = query(q)
    if rows:
        return f"<h1>Welcome, {rows[0][1]}!</h1><p>(Query was:<br><pre>{q}</pre>)<br><a href='/'>Home</a></p>"
    else:
        return f"<h1>Login failed</h1><p>(Query:<br><pre>{q}</pre>)<br><a href='/'>Home</a></p>"

@app.get("/product")
def product():
    pid = request.args.get("id", "1")
    # VULNERABLE: unsanitized numeric parameter
    q = f"SELECT id, title, price FROM products WHERE id = {pid}"
    rows = query(q)
    if rows:
        r = rows[0]
        return f"<h1>Product</h1><p>id={r[0]} title={r[1]} price={r[2]}</p><pre>{q}</pre><p><a href='/'>Home</a></p>"
    else:
        return f"<h1>Not Found</h1><pre>{q}</pre><p><a href='/'>Home</a></p>"

def query(q):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute(q)  # intentionally unsafe for demo
        rows = c.fetchall()
    except Exception as e:
        rows = []
        # Show DB error to aid the lesson
        return [(None, f"DB-ERROR: {e}")]
    finally:
        conn.commit()
        conn.close()
    return rows

if __name__ == "__main__":
    init_db()
    app.run(port=5003, debug=True)
