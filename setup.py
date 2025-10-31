from setuptools import setup, find_packages

setup(
    name="ollies-ticket-counter",
    version="1.0.0",
    description="🐾 Ollie’s Ticket Counter — Track support messages and tickets locally",
    author="Natspwns",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "ollies-ticket-counter=ollies_ticket_counter.cli:main",
        ],
    },
    python_requires=">=3.8",
)
