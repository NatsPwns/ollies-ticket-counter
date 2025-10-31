# 🐾 Ollie’s Ticket Counter

[![GitHub Repo](https://img.shields.io/badge/GitHub-natspwns%2Follies--ticket--counter-181717?logo=github)](https://github.com/natspwns/ollies-ticket-counter)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Install from GitHub](https://img.shields.io/badge/pip%20install-git%2Bhttps%3A%2F%2Fgithub.com%2Fnatspwns%2Follies--ticket--counter.git-brightgreen)](https://github.com/natspwns/ollies-ticket-counter)

**Ollie’s Ticket Counter** is a lightweight, local CLI tool to track daily support activity, messages sent, tickets handled, and weekly progress!
All saved privately on your machine.  
Built with love, coffee ☕, and the occasional "click clack" from Ollie 🐶💻

---

## ✨ Features

- 🧮 Track messages and ticket links for each day  
- 📊 View your daily and weekly stats  
- 📁 Export weekly reports to CSV  
- 💾 Saves progress locally in `support_tracker.json`  
- 🐾 Runs entirely offline (no cloud dependencies)

---

## ⚙️ Installation

To install directly from GitHub:


pip install git+https://github.com/natspwns/ollies-ticket-counter.git

## 🚀 Usage

Run from any terminal once installed:
```bash
ollies-ticket-counter menu          # Interactive menu featuring Ollie 🐶
ollies-ticket-counter add           # Log a new ticket (interactive)
ollies-ticket-counter msg           # Count 1 message
ollies-ticket-counter msg --count 3 # Count 3 messages
ollies-ticket-counter today         # View today’s stats
ollies-ticket-counter week          # Weekly report
ollies-ticket-counter export        # Export CSV (with optional cache clear)
```

## 🧩 Example Output
```bash
  / __ \| | (_)    ( )     | | (_)    | |      | |                         | |           
 | |  | | | |_  ___|/ ___  | |_ _  ___| | _____| |_    ___ ___  _   _ _ __ | |_ ___ _ __ 
 | |  | | | | |/ _ \ / __| | __| |/ __| |/ / _ \ __|  / __/ _ \| | | | '_ \| __/ _ \ '__|
 | |__| | | | |  __/ \__ \ | |_| | (__|   <  __/ |_  | (_| (_) | |_| | | | | ||  __/ |   
  \____/|_|_|_|\___| |___/  \__|_|\___|_|\_\___|\__|  \___\___/ \__,_|_| |_|\__\___|_|   

            __
 (___()'`;\
 /,    /`   💻  click clack...
 \\"--\\
Targets: 15 messages/day  ·  8 new convos/day
```

## Development 

Clone locally for testing or improvements:
```bash
git clone https://github.com/natspwns/ollies-ticket-counter.git
cd ollies-ticket-counter
pip install -e .
```
Then run:
```bash
ollies-ticket-counter menu
```
