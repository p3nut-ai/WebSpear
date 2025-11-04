# web.py
from flask import Flask, redirect, render_template, request, url_for
import sqlite3
import os
import json
import sys 

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from exploit_modules.exploits import Exploits
from database.db_init import init_db

base_dir = os.path.dirname(__file__)
main_db_path = os.path.join(base_dir, "..", "webspear.db")

app = Flask(__name__)

init_db(main_db_path)

@app.route('/', methods=['GET'])
def index():
    targets = get_all_targets()
    selected_id = request.args.get("target")

    selected_target = None
    if selected_id:
        selected_target = next((t for t in targets if str(t["id"]) == selected_id), None)
    elif targets:
        selected_target = targets[0]

    return render_template(
        "index.html",
        targets=targets,
        selected_target=selected_target,
        results=selected_target or {}
    )

@app.route('/scan', methods=['POST'])
def scan():
    scan_url = request.form.get("scan_url", "").strip()
    if scan_url:
        try:
            exploits = Exploits(scan_url)
            exploits.start_exploit_engine() 
        except Exception as e:
            print(f"[!] Scan error for {scan_url}: {e}")
        return redirect(url_for('index'))
    return redirect(url_for('index'))

def get_all_targets(db_path=main_db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM targets ORDER BY timestamp DESC, id DESC")

    columns = [desc[0] for desc in cursor.description]
    results = []

    for row in cursor.fetchall():
        record = dict(zip(columns, row))

        # Safely decode all JSON-based fields
        json_fields = [
            "final_internal_links",
            "endpoints_with_query",
            "form_endpoints",
            "js_endpoints",
            "wp_vulnerability",
            "bs_vulnerability",
            "vuln_types",
            "xss_findings",
            "sqli_findings",
            "lfi_rfi_findings",
            "ddos_results",
            "js_findings"
        ]

        for field in json_fields:
            try:
                record[field] = json.loads(record.get(field) or "[]")
            except Exception:
                record[field] = []

        record["wp_version"] = record.get("wp_version", "") or ""
        record["bs_version"] = record.get("bs_version", "") or ""

        results.append(record)

    conn.close()
    return results

def run_flask_server(host="0.0.0.0", port=5005):
    print("[+] Starting Web UI")
    app.run(debug=True, host=host, port=port)

