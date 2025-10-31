#!/usr/bin/env python3
import argparse
from ollies_ticket_counter.tracker_core import (
    load_data, save_data, add_new_ticket, log_message_sent,
    view_todays_progress, weekly_report, export_to_csv
)

def main():
    parser = argparse.ArgumentParser(
        description="🐾 Ollie’s Ticket Counter — Track daily messages, tickets, and export progress."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: log a new ticket
    subparsers.add_parser("add", help="Add a new ticket link (interactive input)")

    # Command: add message
    msg_parser = subparsers.add_parser("msg", help="Log a message (+1)")
    msg_parser.add_argument("--count", type=int, default=1, help="Number of messages to add")

    # Command: view today’s progress
    subparsers.add_parser("today", help="View today’s stats")

    # Command: weekly report
    subparsers.add_parser("week", help="Show the weekly report")

    # Command: export to CSV
    subparsers.add_parser("export", help="Export data to CSV (optional cache clear)")

    # Command: full interactive menu
    subparsers.add_parser("menu", help="Run the classic interactive menu")

    args = parser.parse_args()
    data = load_data()

    if args.command == "add":
        data = add_new_ticket(data)
        save_data(data)
    elif args.command == "msg":
        for _ in range(args.count):
            data = log_message_sent(data)
        save_data(data)
    elif args.command == "today":
        view_todays_progress(data)
    elif args.command == "week":
        weekly_report(data)
    elif args.command == "export":
        data = export_to_csv(data)
        save_data(data)
    elif args.command == "menu":
        from ollies_ticket_counter.tracker_core import main_loop
        main_loop()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
