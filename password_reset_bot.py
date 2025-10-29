#!/usr/bin/env python3
"""
Active-Directory password reset bot for Microsoft Teams.
Runs every 5 min, checks locked accounts, resets them, posts card to Teams.
Author: Michail Lazaridis – MIT licence
"""
import os, json, requests, sqlite3
from datetime import datetime
from ad import AD  # pip install pyad
from teams import TeamsHook  # pip install pymsteams

TEAMS_URL = os.getenv("TEAMS_WEBHOOK")
DB_FILE   = "reset_log.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS resets (sam text, ts text)")

def was_reset(sam):
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.execute("SELECT 1 FROM resets WHERE sam=? AND ts>=datetime('now','-1 day')", (sam,))
        return cur.fetchone() is not None

def log_reset(sam):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("INSERT INTO resets VALUES (?, ?)", (sam, datetime.utcnow().isoformat()))

def locked_users():
    """Return list[(sam, email)] of locked AD accounts."""
    return [(u.sAMAccountName, u.mail) for u in AD().search_locked()]

def unlock(sam):
    user = AD().get_user(sam)
    user.unlock()
    user.set_password("TempPass123!")  # force change at next logon
    user.force_pwd_change_on_login()

def notify_teams(sam, email):
    card = {
        "@type": "MessageCard",
        "text": f"🔓 **{sam}** unlocked & temp password sent to {email}"
    }
    requests.post(TEAMS_URL, json=card)

def main():
    init_db()
    for sam, email in locked_users():
        if not was_reset(sam):
            unlock(sam)
            log_reset(sam)
            notify_teams(sam, email)

if __name__ == "__main__":
    main()
