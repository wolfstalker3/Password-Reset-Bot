# 🔐 AD Password-Reset Bot for MS Teams

Auto-unlocks Active-Directory accounts and notifies the help-desk channel.

## Demo
30-sec Loom: https://loom.com/share/YOUR_SHARE  
Live run screenshot:  
![run](https://raw.githubusercontent.com/wolfstalker3/Password-Reset-Bot/main/demo.png)

## Impact at ACT AE
- 25 locked-account tickets/week → **0 manual resets** after deployment  
- Mean resolution time: **3 h → 45 min**  
- Ran uninterrupted since 2024-06

## Quick start
1. Clone & `pip install -r requirements.txt`
2. Create Teams incoming webhook → export `TEAMS_WEBHOOK=&lt;url&gt;`
3. `python password_reset_bot.py` (or schedule via Task Scheduler / cron)

## Stack
Python 3 | pyad | pymsteams | SQLite

## Licence
MIT – feel free to use at your company.
