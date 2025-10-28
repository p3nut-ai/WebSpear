# web.py
from flask import Flask, redirect, render_template, request, url_for
import sqlite3
import os
import json

# make sure these are correct relative imports in your project layout
from exploit_modules.exploits import Exploits
from database.db_init import init_db

base_dir = os.path.dirname(__file__)
main_db_path =  os.path.join(base_dir, "..", "webspear.db")

app = Flask(__name__)

# ensure DB/tables exist when web app starts
init_db(main_db_path)

@app.route('/', methods=['GET'])
def index():
    targets = get_all_targets()
    selected_id = request.args.get("target")

    selected_target = None
    if selected_id:
        selected_target = next((t for t in targets if str(t["id"]) == selected_id), None)
    elif targets:
        selected_target = targets[0]  # newest first due to ORDER BY in get_all_targets()

    return render_template(
        "index.html",
        targets=targets,
        selected_target=selected_target,
        results=selected_target or {}
    )

@app.route('/scan', methods=['POST'])
def scan():
    """
    POST endpoint receives a form field 'scan_url' and runs the Exploits scanner.
    The scanner is executed synchronously here and writes results to the DB.
    After completion we redirect back to index (latest scan will be auto-selected).
    """
    scan_url = request.form.get("scan_url", "").strip()
    if not scan_url:
        # no input provided -> redirect back
        return redirect(url_for('index'))

    # create and run Exploits scanner
    try:
        exploits = Exploits(scan_url)
        exploits.start_hunting()   # scanner already saves results into DB
    except Exception as e:
        # log error (could be more sophisticated)
        print(f"[!] Scan error for {scan_url}: {e}")

    # redirect to dashboard (newest entry should be selected)
    return redirect(url_for('index'))

def run_flask_server(host="0.0.0.0", port=5000):
    print("[+] Starting Web UI")
    app.run(debug=True, host=host, port=port)

def get_all_targets(db_path=main_db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Order newest first (use timestamp or id depending on your schema)
    cursor.execute("SELECT * FROM targets ORDER BY timestamp DESC, id DESC")

    columns = [desc[0] for desc in cursor.description]
    results = []

    for row in cursor.fetchall():
        record = dict(zip(columns, row))

        # Parse JSON array fields safely
        for field in [
            "final_internal_links",
            "endpoints_with_query",
            "form_endpoints",
            "js_endpoints",
            "wp_vulnerability",
            "bs_vulnerability"
        ]:
            try:
                record[field] = json.loads(record[field]) if record.get(field) else []
            except Exception:
                record[field] = []

        # Normalize names for the template
        record["wp_version"] = record.get("wp_version", "") or ""
        record["bs_version"] = record.get("bs_version", "") or ""
        record["wp_cves"] = record.get("wp_vulnerability", []) or []
        record["bootstrap_cves"] = record.get("bs_vulnerability", []) or []
        record["findings"] = record.get("findings", []) or []
        record["log"] = record.get("log", "") or ""

        results.append(record)

    conn.close()
    return results

# allow running as a script for dev convenience
if __name__ == "__main__":
    run_flask_server()
