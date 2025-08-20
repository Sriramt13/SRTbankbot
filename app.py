from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "srt_bank_secret_key"

# --- Dummy Data ---
users = {"teja": "srt123", "sri": "bank123"}

account_profile = {
    "name": "Teja",
    "number": "XXXX-XXXX-4050",
    "type": "Savings",
    "balance": 25000.75,
    "currency": "INR"
}

transactions = [
    {"date": "2025-08-01", "desc": "UPI - Grocery", "amount": -1450.00, "balance": 26300.75},
    {"date": "2025-07-29", "desc": "Salary Credit", "amount": 35000.00, "balance": 27750.75},
    {"date": "2025-07-25", "desc": "ATM Withdrawal", "amount": -5000.00, "balance": -1},  # -1 means missing
]

loans_catalog = [
    {"type": "Personal Loan", "rate": "11.25% p.a.", "max": "₹10 Lakh", "tenure": "12–60 months"},
    {"type": "Home Loan", "rate": "8.50% p.a.", "max": "₹1 Crore", "tenure": "5–30 years"},
    {"type": "Education Loan", "rate": "9.90% p.a.", "max": "₹30 Lakh", "tenure": "12–84 months"},
    {"type": "Auto Loan", "rate": "9.25% p.a.", "max": "₹25 Lakh", "tenure": "12–84 months"},
]

cards_info = {
    "debit": {"status": "Active", "limit": "₹50,000/day", "last4": "4321"},
    "credit": {"status": "Active", "limit": "₹1,50,000", "last4": "9988"},
}

branches = [
    {"city": "Hyderabad", "name": "SRT Bank - HiTech City", "address": "Plot 21, Cyber Towers", "ifsc": "SRTB0000123"},
    {"city": "Bengaluru", "name": "SRT Bank - Indiranagar", "address": "100ft Rd, HAL 2nd Stage", "ifsc": "SRTB0000456"},
    {"city": "Mumbai", "name": "SRT Bank - BKC", "address": "G Block, Bandra Kurla Complex", "ifsc": "SRTB0000789"},
]

# --- Helpers ---
def logged_in():
    return "user" in session

# --- Routes ---
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form.get("username", "").strip()
        p = request.form.get("password", "").strip()
        if u in users and users[u] == p:
            session["user"] = u
            flash("Login successful. Welcome to SRT Bank!", "success")
            return redirect(url_for("dashboard"))
        flash("Invalid credentials. Try again.", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))

@app.route("/dashboard")
def dashboard():
    if not logged_in():
        return redirect(url_for("login"))
    return render_template("dashboard.html", profile=account_profile, cards=cards_info)

@app.route("/balance")
def balance():
    if not logged_in():
        return redirect(url_for("login"))
    return render_template("balance.html", profile=account_profile)

@app.route("/transactions")
def transactions_page():
    if not logged_in():
        return redirect(url_for("login"))
    
    running = account_profile["balance"]
    txns = []
    for t in transactions:
        txn = t.copy()
        if txn["balance"] == -1:
            running = round(running + txn["amount"], 2)
            txn["balance"] = running
        txns.append(txn)

    return render_template("transactions.html", txns=txns)

@app.route("/loans")
def loans():
    if not logged_in():
        return redirect(url_for("login"))
    return render_template("loans.html", loans=loans_catalog)

@app.route("/cards")
def cards():
    if not logged_in():
        return redirect(url_for("login"))
    return render_template("cards.html", cards=cards_info)

@app.route("/branches")
def branches_list():
    if not logged_in():
        return redirect(url_for("login"))
    return render_template("branches.html", branches=branches)

@app.route("/chatbot")
def chatbot():
    if not logged_in():
        return redirect(url_for("login"))
    return render_template("chatbot.html", now=datetime.now().strftime("%d %b %Y, %I:%M %p"))

# --- API for Chatbot ---
@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json() or {}
    message = (data.get("message") or "").strip().lower()
    
    if "balance" in message:
        return {"reply": f"Your {account_profile['type']} balance is ₹{account_profile['balance']:.2f}."}
    if "block" in message and "card" in message:
        return {"reply": "To block your card instantly, call 1800-123-4567 or visit the Cards page."}
    if "loan" in message:
        return {"reply": "We offer Personal, Home, Education, and Auto loans. Visit Loans for rates & tenure."}
    if "atm" in message or "branch" in message:
        return {"reply": "Use Branches in the menu to find your nearest SRT Bank branch or ATM."}
    
    return {"reply": "I'm SRT Assistant. Ask me about balance, loans, card blocking, or branch locator."}

if __name__ == "__main__":
    app.run(debug=True)
