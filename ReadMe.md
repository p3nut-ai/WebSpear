
# ⚔️ WebSpear – Automated Web Vulnerability Framework

**WebSpear** is an offensive security framework built in Python, designed for ethical web application penetration testing and vulnerability research.  
It focuses on **automation**, **realism**, and **offensive depth**, supporting modules from **XSS** to **DoS simulation**, **JS endpoint analysis**, and **credential brute-forcing**.

---

## 🧩 Key Features

### 🕸️ Recon & Crawler
- Intelligent web crawler capable of identifying:
  - Internal and external links  
  - Query-based endpoints  
  - JavaScript endpoints  
  - Form submission points (`<form>`, `fetch`, etc.)
- Extracts all assets needed for post-recon exploitation.

---

## 💀 Exploitation Modules

### 🧨 Cross-Site Scripting (XSS)

#### 🔹 DOM-Based XSS
- Parses all URLs with query parameters.
- Injects unique tracking payloads (UUID-based).
- Checks reflection in:
  - HTML text
  - `<script>` blocks
  - Inline event handlers
- Identifies vulnerable parameters and context.

#### 🔹 Reflected & Stored XSS via Forms
- Auto-detects form endpoints and injection points.
- Submits payloads via both `GET` and `POST` methods.
- Tests multiple payload encodings:
  - `<script>alert(1)</script>`
  - Encoded forms (`&lt;script&gt;`, `&#x3C;script&#x3E;`)
  - HTML and image-based payloads
- Detects reflection and persistence in response content.

#### 🧠 Payload Intelligence
- HTML context awareness (avoids breaking forms).  
- Supports `<textarea>` and hidden fields.  
- Form action fallback detection (submits even if JS handles form logic).  
- Phase 1 (DOM reflection) → Phase 2 (Payload execution).

---

### 🌊 Denial of Service (DoS) Simulation
- Simulates **form-spam DoS attacks** to identify rate-limit and captcha bypass issues.
- Features:
  - Multi-threaded flood (`ThreadPoolExecutor`)
  - Header rotation (`User-Agent`, `X-Forwarded-For`)
  - Optional proxy pool support
  - CSRF token discovery and reuse
  - Adaptive behavior:  
    - Phase 1 → 20 probe requests  
    - Phase 2 → Full flood if target is responsive

---

### ⚙️ JavaScript Endpoint Analysis
- Scans internal & external JS files for:
  - API keys, tokens, AWS credentials  
  - Hardcoded passwords or secrets  
  - Sensitive endpoints (`fetch`, `axios`, `XMLHttpRequest`)  
  - DOM-based sinks (`document.write`, `innerHTML`)
- Extracts **fetch target domains** for deeper exploitation.
- Maps relationships between JS files and backend APIs.

---

### 🔐 Login Form Detection & Brute Force
- Automatically detects login forms by analyzing:
  - Form structure (`<input type="password">`)
  - Button text (`login`, `sign in`)
  - Hidden CSRF tokens
- Brute-forces login using wordlists (`usernames.txt`, `passwords.txt`).
- Supports fallback **Playwright automation** for:
  - JS-based logins
  - Event-driven form submissions
- Extracts cookies & session data upon successful login.

---

## 🧪 Local WebSpear Lab
To safely test WebSpear’s modules, a **Flask-based local lab** is included.

### Features:
- Endpoints for:
  - GET & POST forms  
  - DOM-based XSS reflection  
  - JS-based form submission  
  - CSRF-protected form  
- Real-time request counter & request log display (via SQLite)
- WebSocket-like live refresh for showcasing DoS and brute-force simulations

---

## 📊 Dashboard UI
- Built using **TailwindCSS**
- Features:
  - Live vulnerability tracking  
  - Realtime DoS visualization (active request counter)  
  - Target summary: URLs, IPs, tech stack  
  - Vulnerability breakdown per endpoint  
  - CVE mapping (WordPress / Bootstrap versions)
- Data persistence via SQLite for lightweight storage.

---

## 🧠 Architecture Overview

```
WebSpear/
├── exploit_modules/
│   ├── exploits.py           # Core engine: XSS, DoS, Login brute-force, JS analyzer
│   ├── utils.py              # Helper functions (regex, DB, payload generation)
│   └── wp_db/                # Local CVE database for tech detection
├── dashboards/
│   └── index.py            # Tailwind dashboard for visualizing results
├── testing_ground/
│   └── index.py                # Flask-based XSS/CSRF/DoS simulation lab
├── webspear.db               # SQLite main database
├── usernames.txt             # Brute-force usernames
├── passwords.txt             # Brute-force passwords
└── README.md
```

---

## 🚀 How to Run

### Install dependencies:
```bash
pip install -r requirements.txt
```

### Run the local lab:
```bash
python testing_ground/index.py
```

### Run WebSpear exploit engine:
```bash
python exploit_modules/exploits.py --scan https://target.site
```

### Optional CLI arguments:
| Flag | Description |
|------|--------------|
| `--url` | Target URL |
| `--d` | Launch dashboard UI |
| `--headless` | Run scans without UI |
| `--fast` | Quick scan mode |

---

## 📋 Features Completed
- ✅ Crawler / Link Enumerator  
- ✅ DOM XSS  
- ✅ Form XSS  
- ✅ DoS (form flood)  
- ✅ JS Analyzer (Fetch, secrets, tokens)  
- ✅ Login Finder  
- ✅ Brute-force Engine  
- ✅ Playwright Auto-Login  
- ✅ Realtime Dashboard + Lab  

---

## 🧱 Upcoming Modules
| Feature | Status | Description |
|----------|----------|-------------|
| SQL Injection Detection | 🧩 Planned | Fuzz params and forms for SQL-based injection |
| LFI/RFI / Path Traversal | 🧩 Planned | Identify file inclusion and traversal vulnerabilities |
| Authenticated Scanning | 🧩 Planned | Use saved cookies from login for deeper scan |
| Screenshot Capture | 🧩 Planned | Visual confirmation of vulnerabilities via Playwright |
| CVE Matching Expansion | 🧩 Planned | Add more frameworks (React, Angular, etc.) |

---

## ⚠️ Legal Disclaimer
> WebSpear is designed for **ethical security testing, education, and research** only.  
> Do not use this tool against systems you do not own or have explicit permission to test.

---

## 🧑‍💻 Author
**WebSpear**  
Developed by **0slo** — building offensive automation for next-gen cybersecurity research.
