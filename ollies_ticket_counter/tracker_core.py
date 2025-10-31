#!/usr/bin/env python3
"""
HOW TO:
Support Activity Tracker V3:

- Menu-driven terminal app
- Log ticket links (each unique link = 1 new conversation)
- Log messages sent (increments total messages for today by 1)
- View today's progress (compares to targets: 15 messages, 8 conversations)
- Weekly report (last 7 days)
- Export to CSV, then optionally clear local cache so you don't end up with old tickets in your export
- Autosaves to support_tracker.json (Local file memory, no cloud here!)

Save as: support_tracker.py
Run: python3 support_tracker.py
"""

import json
import csv
import os
from datetime import datetime, timedelta

DATA_FILE = "support_tracker.json"
CSV_FILE = "support_activity_report.csv"
MESSAGE_GOAL = 15
CONVERSATION_GOAL = 8

# ANSI colors (simple)
RESET = "\033[0m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def today_str():
    return datetime.now().strftime("%Y-%m-%d")


def week_dates_for(date_obj=None):
    # returns list of YYYY-MM-DD strings for the week containing the given date (Mon-Sun)
    if date_obj is None:
        date_obj = datetime.now().date()
    else:
        date_obj = date_obj if isinstance(date_obj, datetime) else date_obj
        date_obj = date_obj.date() if isinstance(date_obj, datetime) else date_obj
    weekday = date_obj.weekday()  # Monday=0
    monday = date_obj - timedelta(days=weekday)
    return [(monday + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]


def ticket_already_logged_in_week(data, link):
    # check all links for current week
    for d in week_dates_for():
        day = data.get(d, {})
        links = day.get("links", [])
        if link in links:
            return True
    return False


def add_new_ticket(data):
    link = input("Enter ticket link: ").strip()
    if not link:
        print(f"{YELLOW}No link entered, returning to menu.{RESET}")
        return data
    if ticket_already_logged_in_week(data, link):
        print(f"Skipping: ticket already logged for this week. {MAGENTA}({link}){RESET}")
        return data
    d = today_str()
    day = data.get(d, {"messages": 0, "links": []})
    day.setdefault("messages", 0)
    links = day.setdefault("links", [])
    links.append(link)
    data[d] = day
    save_data(data)
    print(f"Logged ticket: {CYAN}{link}{RESET}  — total tickets today: {len(data[d]['links'])}")
    # pretties
    print(f"{GREEN}🎟️  Ticket logged!{RESET}")
    return data


def log_message_sent(data):
    d = today_str()
    day = data.get(d, {"messages": 0, "links": []})
    day.setdefault("links", [])
    day["messages"] = day.get("messages", 0) + 1
    data[d] = day
    save_data(data)
    total = day["messages"]
    status = f"{GREEN}✅ Message goal met: {total} / {MESSAGE_GOAL}{RESET}" if total >= MESSAGE_GOAL else f"{YELLOW}Logged 1 message. Total messages today: {total} / {MESSAGE_GOAL}{RESET}"
    print(status)
    # encouragement, cause being in Support is hard.
    print("✉️  " + (f"{GREEN}Nice — keep going!{RESET}" if total >= MESSAGE_GOAL else f"{CYAN}Logged.{RESET}"))
    return data


def view_todays_progress(data):
    d = today_str()
    day = data.get(d, {"messages": 0, "links": []})
    messages = day.get("messages", 0)
    convos = len(day.get("links", []))
    print()
    print(f"{BOLD}Date:{RESET} {d}")
    msg_ok = messages >= MESSAGE_GOAL
    conv_ok = convos >= CONVERSATION_GOAL
    msg_line = f"Messages: {messages} / {MESSAGE_GOAL} {'✅' if msg_ok else '⚠️'}"
    conv_line = f"New Conversations: {convos} / {CONVERSATION_GOAL} {'✅' if conv_ok else '⚠️'}"
    print(msg_line if msg_ok else f"{YELLOW}{msg_line}{RESET}")
    print(conv_line if conv_ok else f"{YELLOW}{conv_line}{RESET}")
    print(f"Tickets logged: {convos}")
    print()


def weekly_report(data):
    today = datetime.now().date()
    dates = week_dates_for(datetime.now())
    # produce past 7 days ending today (mon-sun)
    # But user may expect "last 7 days", we'll show last 7 days up to today.
    last7 = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]  # oldest -> newest
    total_msgs = 0
    total_convos = 0
    print()
    print(f"{BOLD}Weekly report (last 7 days){RESET}")
    print(f"{'Date':<12}{'Messages':<12}{'New Convos'}")
    print("-" * 36)
    for d in last7:
        day = data.get(d, {"messages": 0, "links": []})
        msgs = day.get("messages", 0)
        convs = len(day.get("links", []))
        total_msgs += msgs
        total_convos += convs
        print(f"{d:<12}{str(msgs):<12}{str(convs)}")
    avg_msgs = total_msgs / 7
    avg_convos = total_convos / 7
    print("-" * 36)
    print(f"{'Total:':<12}{str(total_msgs):<12}{str(total_convos)}")
    print(f"{'Average/day:':<12}{avg_msgs:.1f}{'':<7}{avg_convos:.1f}")
    print()


def export_to_csv(data):
    # flatten into rows per date; links combined as pipe-separated string so the CSV looks noice
    rows = []
    for d in sorted(data.keys()):
        day = data[d]
        msgs = day.get("messages", 0)
        links = day.get("links", [])
        convs = len(links)
        links_joined = " | ".join(links)
        rows.append({
            "Date": d,
            "Messages": msgs,
            "New Conversations": convs,
            "Links": links_joined
        })

    if not rows:
        print(f"{YELLOW}No data to export.{RESET}")
        return data

    try:
        # figure out the current week range (Mon–Sun)
        today = datetime.now().date()
        monday = today - timedelta(days=today.weekday())
        sunday = monday + timedelta(days=6)
        week_label = f"{monday.strftime('%Y-%m-%d')}_to_{sunday.strftime('%Y-%m-%d')}"

        # create dynamic filename
        csv_filename = f"support_activity_report_{week_label}.csv"

        # keep the for-loop INSIDE the 'with' block
        with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["Date", "Messages", "New Conversations", "Links"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for r in rows:
                writer.writerow(r)

        # only print AFTER file closes
        print(f"{GREEN}Export complete → {csv_filename}{RESET}")

    except Exception as e:
        print(f"{YELLOW}Failed to export CSV: {e}{RESET}")
        return data

    # Ask about clearing cache
    while True:
        clear = input("Clear local cache? (y/n) ").strip().lower()
        if clear in ("y", "yes"):
            try:
                if os.path.exists(DATA_FILE):
                    os.remove(DATA_FILE)
                print(f"{MAGENTA}Local cache cleared.{RESET}")
                return {}
            except Exception as e:
                print(f"{YELLOW}Could not clear cache: {e}{RESET}")
                return data
        elif clear in ("n", "no"):
            print("Cache retained.")
            return data
        else:
            print("Please answer 'y' or 'n'.")
def print_header():
    # ASCII Ollie counting 
    ollie = r"""
            __
 (___()'`;\
 /,    /`   💻  click clack...
 \\"--\\
    """
    banner = f"""
{MAGENTA}{BOLD}
            
  / __ \| | (_)    ( )     | | (_)    | |      | |                         | |           
 | |  | | | |_  ___|/ ___  | |_ _  ___| | _____| |_    ___ ___  _   _ _ __ | |_ ___ _ __ 
 | |  | | | | |/ _ \ / __| | __| |/ __| |/ / _ \ __|  / __/ _ \| | | | '_ \| __/ _ \ '__|
 | |__| | | | |  __/ \__ \ | |_| | (__|   <  __/ |_  | (_| (_) | |_| | | | | ||  __/ |   
  \____/|_|_|_|\___| |___/  \__|_|\___|_|\_\___|\__|  \___\___/ \__,_|_| |_|\__\___|_|   
                                                                                         
{RESET}
"""
    print(banner)
    print(ollie)
    print(f"{CYAN}Targets: {MESSAGE_GOAL} messages/day  ·  {CONVERSATION_GOAL} new convos/day{RESET}")
    print()


def main_loop():
    data = load_data()
    print_header()
    while True:
        print("Menu:")
        print("1. Log new ticket")
        print("2. Log message sent (+1)")
        print("3. View today's progress")
        print("4. View weekly report")
        print("5. Export to CSV")
        print("6. Exit")
        choice = input("Choose an option (1-6): ").strip()
        if choice == "1":
            data = add_new_ticket(data)
        elif choice == "2":
            data = log_message_sent(data)
        elif choice == "3":
            view_todays_progress(data)
        elif choice == "4":
            weekly_report(data)
        elif choice == "5":
            data = export_to_csv(data)
            # save current state after export/clear decisions
            save_data(data)
        elif choice == "6":
            print("Bye. Keep counting. ✨")
            break
        else:
            print("Invalid choice. Pick 1-6.")
        # slight space between cycles
        print()


if __name__ == "__main__":
    main_loop()
