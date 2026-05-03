# 🔐 SecureX – Cyber Security Toolkit

## 🚀 Project Overview

SecureX is a web-based **Cyber Security Toolkit** built using Python and Streamlit.
It helps users detect common digital threats such as weak passwords, phishing messages, and unsafe URLs.
The system also provides encryption and decryption of sensitive data along with activity logging and report generation.

---

## 🎯 Key Features

### 🔑 Authentication System

* Secure login and signup functionality
* Passwords stored using hashing
* Session-based user management

---

### 🛡️ Password Strength Checker

* Evaluates password strength (0–5 score)
* Checks:

  * Uppercase letters
  * Lowercase letters
  * Numbers
  * Special characters
  * Minimum length

---

### 🌐 URL Safety Checker

* Detects suspicious or unsafe URLs
* Flags:

  * Non-HTTPS links
  * IP-based URLs
  * Long or abnormal URLs
  * Phishing patterns

---

### 🎣 Phishing Detection

* Analyzes messages/emails for phishing attempts
* Detects:

  * Urgent or threatening language
  * Fake bank/security alerts
  * Suspicious keywords
  * Scam patterns

---

### 🔐 Encryption & Decryption

* Secure note encryption using Fernet cryptography
* Allows users to encrypt and decrypt sensitive data safely

---

### 💾 Database Logging

* Uses SQLite database
* Stores:

  * User actions
  * Results
  * Timestamps

---

### 📊 Report Generation

* Displays activity logs in dashboard
* Allows users to download reports in CSV format

---

## 🖥️ Tech Stack

* Python 🐍
* Streamlit 🌐
* SQLite 💾
* Cryptography (Fernet) 🔐
* Pandas 📊
* Regex 🧾

---

## 📸 Screenshots

### 🔑 Password Checker

![Password Checker](screenshots/password.png)

### 🌐 URL Checker

![URL Checker](screenshots/url.png)

### 🎣 Phishing Detector

![Phishing Detector](screenshots/phishing.png)

### 🔐 Encryption & Decryption

![Encryption](screenshots/encrypt.png)

### 📊 Report System

![Report](screenshots/report.png)

---

## 🌐 Live Demo

👉 Add your deployed Streamlit link here

---

## 🧠 Project Architecture

User → Streamlit UI → Security Modules → Database → Report System

---

## 📦 Installation & Setup

```bash
git clone https://github.com/chithrasagadevan2008-lgtm/securex-toolkit.git
cd securex-toolkit
pip install -r requirements.txt
python -m streamlit run app.py
```

---

## 📄 requirements.txt

```
streamlit
cryptography
pandas
```

---

## 🔮 Future Enhancements

* AI-based phishing detection
* Real-time risk scoring system
* User-specific dashboards
* Cloud database integration
* Advanced UI improvements

---

## ⚠️ Disclaimer

This project is intended for educational purposes only and does not provide production-level security.
# securex-toolkit
🛡️ SecureX is a premium cyber security toolkit that analyzes password strength, detects phishing URLs, and verifies file integrity using SHA-256 hashing.
