import sqlite3

def init_db(db_path="webspear.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS targets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT NOT NULL UNIQUE,
        ip TEXT,
        final_internal_links TEXT,
        endpoints_with_query TEXT,
        form_endpoints TEXT,
        js_endpoints TEXT,
        wp_version TEXT,
        wp_vulnerability TEXT,
        bs_version TEXT,
        bs_vulnerability TEXT,
        vuln_types TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()
