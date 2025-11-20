from flask import Flask, request, session, render_template_string, redirect
import secrets
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'xss-lab-key'
DB_PATH = "lab_data.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                endpoint TEXT,
                method TEXT,
                author TEXT,
                comment TEXT,
                token TEXT,
                payload TEXT,
                status TEXT,
                ip TEXT,
                user_agent TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

init_db()

def log_submission(endpoint, method, author=None, comment=None, token=None, payload=None, status="OK"):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO submissions (endpoint, method, author, comment, token, payload, status, ip, user_agent)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            endpoint, method, author, comment, token, payload, status,
            request.remote_addr, request.headers.get('User-Agent')
        ))
        conn.commit()

@app.route('/')
def index():
    return render_template_string("""
    <html>
    <head>
      <title>🧪 XSS + CSRF Lab</title>
      <style>
        body { background: #111; color: #eee; font-family: sans-serif; padding: 2rem; }
        a { display: block; margin: 0.5rem 0; color: #ff77aa; text-decoration: none; }
        table { background: #222; border-collapse: collapse; margin-top: 1rem; }
        th, td { border: 1px solid #444; padding: 0.5rem; font-size: 0.85rem; }
        th { background: #333; }
        h1, h2, h3 { color: #fff; }
        #live-data { margin-top: 2rem; }
      </style>
    </head>
    <body>
      <h1>⚔ WebSpear Testing Lab</h1>
      <p>Choose a test case:</p>
      <nav>
        <a href="/?name=test">1. Reflected XSS via Query Param (DOM)</a>
        <a href="/form">2. Reflected XSS via Form Submission (POST)</a>
        <a href="/get-form">3. GET-based Form with Hidden Field</a>
        <a href="/js-form">4. JavaScript-only Form Submission (Fetch)</a>
        <a href="/login">5. Login (for CSRF test)</a>
        <a href="/secure-form">6. CSRF-Protected Form (requires login)</a>
      </nav>

      <div id="live-data">
        <h3>🌊 Total Requests Logged: <span id="total-count">0</span></h3>

        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Endpoint</th>
              <th>Method</th>
              <th>Payload</th>
              <th>Status</th>
              <th>IP</th>
              <th>Time</th>
            </tr>
          </thead>
          <tbody id="submission-table">
            <!-- Populated via JS -->
          </tbody>
        </table>
      </div>

      <script>
        async function fetchCount() {
          const res = await fetch('/count-submissions');
          const data = await res.json();
          document.getElementById('total-count').innerText = data.total || 0;
        }

        async function fetchSubmissions() {
          const res = await fetch('/recent-submissions');
          const html = await res.text();
          document.getElementById('submission-table').innerHTML = html;
        }

        setInterval(() => {
          fetchCount();
          fetchSubmissions();
        }, 1000);
      </script>
    </body>
    </html>
    """)

@app.route('/count-submissions')
def count_submissions():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM submissions")
        total = cur.fetchone()[0]
    return {"total": total}

@app.route('/recent-submissions')
def recent_submissions():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, endpoint, method, payload, status, ip, timestamp
            FROM submissions
            ORDER BY timestamp DESC
            LIMIT 20
        """)
        rows = cur.fetchall()

    html_rows = ""
    for row in rows:
        html_rows += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td><td>{row[5]}</td><td>{row[6]}</td></tr>"
    return html_rows

@app.route('/form', methods=['GET', 'POST'])
def form():
    output = ""
    if request.method == 'POST':
        author = request.form.get("author", "")
        comment = request.form.get("comment", "")
        output = f"<p><strong>{author}</strong>: {comment}</p>"
        log_submission("/form", "POST", author=author, comment=comment)
    return render_template_string(f"""
    <html><body>
      <h2>📝 Comment Form</h2>
      <form method="POST">
        <input name="author" placeholder="Your name">
        <textarea name="comment" placeholder="Say something"></textarea>
        <button type="submit">Submit</button>
      </form>
      <hr>
      {output}
    </body></html>
    """)

@app.route('/get-form', methods=['GET'])
def get_form():
    name = request.args.get("name", "")
    token = request.args.get("token", "")
    if name or token:
        log_submission("/get-form", "GET", author=name, token=token)
    return render_template_string(f"""
    <html><body>
      <h2>🔎 GET Form with hidden input</h2>
      <form method="GET">
        <input name="name" placeholder="Name">
        <input type="hidden" name="token" value="123abc">
        <button type="submit">Submit</button>
      </form>
      <hr>
      <p>Name: {name}</p>
      <p>Token: {token}</p>
    </body></html>
    """)

@app.route('/js-form', methods=['GET'])
def js_form():
    return render_template_string("""
    <html><body>
      <h2>🧪 JavaScript Submit Form</h2>
      <form id="jsform">
        <input name="payload" id="payload">
        <button type="button" onclick="sendData()">Send via JS</button>
      </form>
      <script>
        function sendData() {
          const val = document.getElementById('payload').value;
          fetch('/js-receiver?val=' + encodeURIComponent(val))
            .then(res => res.text()).then(alert);
        }
      </script>
    </body></html>
    """)

@app.route('/js-receiver')
def js_receiver():
    val = request.args.get("val", "")
    if val:
        log_submission("/js-receiver", "GET", payload=val)
    return f"Received: {val}"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user'] = 'admin'
        return redirect('/secure-form')
    return '''
    <form method="POST">
        <input name="username" value="admin">
        <input name="password" value="admin">
        <button type="submit">Login</button>
    </form>
    '''

@app.route('/secure-form', methods=['GET', 'POST'])
def secure_form():
    if 'user' not in session:
        return redirect('/login')

    csrf_token = session.get('csrf_token') or secrets.token_hex(16)
    session['csrf_token'] = csrf_token

    message = ''
    if request.method == 'POST':
        token = request.form.get('csrf_token')
        data = request.form.get('update')
        if token != session['csrf_token']:
            message = "<p style='color:red;'>CSRF validation failed!</p>"
            log_submission("/secure-form", "POST", payload=data, token=token, status="CSRF Failed")
        else:
            message = f"<p style='color:green;'>Updated value: {data}</p>"
            log_submission("/secure-form", "POST", payload=data, token=token, status="CSRF Passed")

    return render_template_string(f"""
    <h2>🔒 Secure Profile Update</h2>
    <form method="POST">
        <input name="update" placeholder="New data">
        <input type="hidden" name="csrf_token" value="{csrf_token}">
        <button type="submit">Update</button>
    </form>
    <hr>
    {message}
    """)

if __name__ == '__main__':
    print("[+] Web lab running at http://localhost:5000")
    app.run(debug=True, port=5010)
