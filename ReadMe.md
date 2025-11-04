# ⚔️ WebSpear: Automated Web Recon and Exploitation Framework

**WebSpear** is a modern, modular web reconnaissance and vulnerability scanner.  
It crawls, analyzes, and attacks web applications — including authenticated ones — using a mix of passive recon and active exploitation modules.

---

## 🚀 Features

- 🌐 URL Crawler & Endpoint Finder
- 🧩 JavaScript Scraper & Sensitive Data Detector
- 📄 Form Detection (POST/GET)
- 🎯 WordPress & Bootstrap Version Detection + CVE Matching
- 🔐 Login Bruteforce via Playwright
- 🔍 Exploit Modules:
  - Reflected **XSS**
  - Error-based & Time-based **SQL Injection**
  - **LFI / RFI / Path Traversal**
  - **JS Endpoint Analysis**
  - Basic **DoS / DDoS** via parameter spam
- 📦 Result Storage via SQLite
- 📊 Web Dashboard (Flask + Tailwind CSS)
- ☁️ Session Cookie Persistence

---

## 📁 Project Structure

```
webspear/
├── exploit_modules/
│   ├── exploits.py                 # Main engine
│   ├── xss.py                      # XSS detection
│   ├── sqli.py                     # SQL injection
│   ├── lfi_rfi.py                  # Path traversal
│   ├── js_scraper.py               # JS endpoint scraping
│   ├── dos_fuzzer.py               # DoS module
│   ├── playwright_login.py         # Playwright-based login
│
├── database/
│   ├── db_init.py                  # SQLite schema
│   ├── session_cookie_utils.py     # Cookie saving/loading
│
├── static/
│   └── splash.gif                  # Dashboard splash
│
├── templates/
│   └── index.html                  # Tailwind-powered UI
│
├── web.py                          # Flask dashboard
├── main.py                         # CLI runner
├── webspear.db                     # Auto-generated DB
└── README.md
```

---

## 🧠 How It Works

1. 🕷️ Crawl the target — discover links, forms, JS, etc.
2. 📑 Analyze page for CMS/libraries (e.g., WordPress, Bootstrap)
3. 💥 Run enabled exploits (XSS, SQLi, LFI, DoS, etc.)
4. 💾 Store results in SQLite
5. 🌐 View output via dashboard or CLI

---

## 🖥️ CLI Usage

### 🔹 Basic Scan

```bash
python main.py -s https://target.com --cli --all
```

### 🔹 Targeted Modules

```bash
python main.py -s https://target.com --cli --xss --sqli --js
```

### 🔹 Start Dashboard UI

```bash
python main.py -s https://target.com --dashboard
```

---

## 🧪 CLI Flags

| Flag         | Description                                 |
|--------------|---------------------------------------------|
| `-s URL`     | Target to scan                              |
| `--cli`      | Run in terminal-only mode                   |
| `--dashboard`| Start Flask-based web UI                    |
| `--all`      | Run all exploit modules                     |
| `--xss`      | Enable XSS module                           |
| `--sqli`     | Enable SQL Injection module                 |
| `--lfi`      | Enable LFI/RFI/Path Traversal detection     |
| `--js`       | Enable JS endpoint inspection               |
| `--ddos`     | Enable basic DoS check                      |
| `--brute`    | Enable login bruteforce via Playwright      |

---

## 📊 Web Dashboard (Flask)

- 🔍 Start and track scans
- 📂 Explore discovered endpoints
- 🛠️ View all vulnerabilities
- 🛡️ Matched CVEs from WordPress/Bootstrap versions
- 📜 Review scan logs
- 🎨 Fully responsive dark-mode UI (TailwindCSS)

> Start with:
```bash
python main.py -s https://target.com --dashboard
```

---

## 🔐 Authentication Support

If login is required:
- You can log in manually via the browser
- `session_cookies.json` will be saved
- Reused on all future scans

Or:
- Run `--brute` to automate login attempts with provided wordlists

---

## 🧾 Database

All findings are stored in:
```
webspear.db
```

Including:
- Discovered endpoints
- All types of vulns (XSS, SQLi, etc.)
- Detected CVEs
- Timestamps and full logs

---

## 📦 Install Requirements

```bash
pip install -r requirements.txt
playwright install
```

> Required for headless login automation and JS interaction

---

## 📌 CVE Data

Located in JSON files:
- `wp_vulns.json`
- `bootstrap_vulns.json`

Used for offline matching — no network request needed.

---

## 🧷 Disclaimer

This tool is for **educational and authorized penetration testing only**.  
Do **not** scan or attack any system without proper permission.

---

## ✍️ Author

Made with 🖤 by **0slo**  


---

## 🧩 TODO

- [ ] Severity scoring per CVE
- [ ] PDF/HTML report generator
- [ ] Better Playwright login detection
- [ ] Sitemap export
- [ ] Scanner speed modes (fast/deep)

---


