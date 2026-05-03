import streamlit as st
import re
import hashlib
import sqlite3
import pandas as pd
from cryptography.fernet import Fernet
from datetime import datetime
from urllib.parse import urlparse

# ---------------- DATABASE ----------------
conn = sqlite3.connect("securex.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    username TEXT,
    action TEXT,
    result TEXT,
    time TEXT
)
""")
conn.commit()

# ---------------- ENCRYPTION KEY ----------------
if "key" not in st.session_state:
    st.session_state.key = Fernet.generate_key()
    st.session_state.cipher = Fernet(st.session_state.key)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="SecureX Ultimate", layout="wide")

# ---------------- CSS ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: white;
}
.title {
    font-size: 34px;
    text-align: center;
    color: #38bdf8;
    font-weight: bold;
}
.card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 12px;
    margin-top: 10px;
}
.stButton>button {
    background-color: #38bdf8;
    color: black;
    font-weight: bold;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HELPERS ----------------
def log(user, action, result):
    cursor.execute(
        "INSERT INTO logs VALUES (?, ?, ?, ?)",
        (user, action, result, str(datetime.now()))
    )
    conn.commit()

# ---------------- PASSWORD CHECKER ----------------
def check_password_strength(password):
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Min 8 chars")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add uppercase")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add lowercase")

    if re.search(r"[0-9]", password):
        score += 1
    else:
        feedback.append("Add number")

    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("Add special char")

    return score, feedback

# ---------------- URL CHECK ----------------
def url_check(url):
    issues = []
    parsed = urlparse(url)

    if parsed.scheme != "https":
        issues.append("Not HTTPS")

    if "@" in url:
        issues.append("Contains @ trick")

    if re.search(r"\d+\.\d+\.\d+\.\d+", url):
        issues.append("IP based URL")

    if len(url) > 75:
        issues.append("Too long URL")

    return issues

# ---------------- PHISHING ----------------
def phishing_check(text):
    keywords = ["urgent", "password", "verify", "bank", "login", "click"]
    flags = []

    for k in keywords:
        if k in text.lower():
            flags.append(k)

    return flags

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- LOGIN PAGE ----------------
if not st.session_state.logged_in:

    st.markdown('<div class="title">🔐 SecureX Login</div>', unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        hashed = hashlib.sha256(password.encode()).hexdigest()

        cursor.execute("SELECT * FROM users WHERE username=? AND password=?",
                       (username, hashed))
        user = cursor.fetchone()

        if user:
            st.session_state.logged_in = True
            st.session_state.user = username
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid login")

    if st.button("Create Account"):
        hashed = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute("INSERT INTO users VALUES (?,?)", (username, hashed))
        conn.commit()
        st.success("Account created")

# ---------------- DASHBOARD ----------------
else:

    st.sidebar.title("SecureX Menu")
    menu = st.sidebar.radio("Navigate", [
        "Dashboard",
        "Password Checker",
        "URL Checker",
        "Phishing Detector",
        "Secure Notes",
        "Reports",
        "Logout"
    ])

    # ---------------- DASHBOARD ----------------
    if menu == "Dashboard":
        st.markdown('<div class="title">Cyber Security Dashboard 🛡️</div>', unsafe_allow_html=True)

        st.write(f"Welcome **{st.session_state.user}**")

    # ---------------- PASSWORD ----------------
    elif menu == "Password Checker":
        pwd = st.text_input("Enter Password", type="password")

        if st.button("Check"):
            score, fb = check_password_strength(pwd)

            st.write("Score:", score, "/5")

            log(st.session_state.user, "Password Check", str(score))

            for f in fb:
                st.write("•", f)

    # ---------------- URL ----------------
    elif menu == "URL Checker":
        url = st.text_input("Enter URL")

        if st.button("Check URL"):
            res = url_check(url)

            if res:
                st.error("Suspicious URL")
                for r in res:
                    st.write("•", r)
            else:
                st.success("Safe URL")

            log(st.session_state.user, "URL Check", str(res))

    # ---------------- PHISHING ----------------
    elif menu == "Phishing Detector":
        text = st.text_area("Paste email/message")

        if st.button("Analyze"):
            res = phishing_check(text)

            if res:
                st.warning("Possible phishing detected")
                st.write(res)
            else:
                st.success("No phishing detected")

            log(st.session_state.user, "Phishing Check", str(res))

    # ---------------- ENCRYPTION ----------------
    elif menu == "Secure Notes":

        note = st.text_area("Enter Note")

        if st.button("Encrypt"):
            enc = st.session_state.cipher.encrypt(note.encode())
            st.session_state.enc = enc
            st.code(enc.decode())
            log(st.session_state.user, "Encrypt", "done")

        if st.button("Decrypt"):
            if "enc" in st.session_state:
                dec = st.session_state.cipher.decrypt(st.session_state.enc).decode()
                st.success(dec)
                log(st.session_state.user, "Decrypt", "done")

    # ---------------- REPORT ----------------
    elif menu == "Reports":

        cursor.execute("SELECT * FROM logs")
        data = cursor.fetchall()

        df = pd.DataFrame(data, columns=["User", "Action", "Result", "Time"])

        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download Report",
            csv,
            "securex_report.csv",
            "text/csv"
        )

    # ---------------- LOGOUT ----------------
    elif menu == "Logout":
        st.session_state.logged_in = False
        st.success("Logged out")
        st.rerun()