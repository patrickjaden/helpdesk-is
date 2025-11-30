import sqlite3
import os
from faker import Faker
import random
from datetime import datetime, timedelta

# -------- Paths --------
DB_PATH = os.path.join("data", "tickets.db")

# Ensure data/ folder exists
os.makedirs("data", exist_ok=True)

fake = Faker()

# -------- Create connection --------
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# -------- Drop old tables --------
tables = ["tickets", "customers", "agents", "priority", "status", "channel"]
for t in tables:
    cur.execute(f"DROP TABLE IF EXISTS {t};")

# -------- Create lookup tables --------
cur.execute("""
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT
);
""")

cur.execute("""
CREATE TABLE agents (
    agent_id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT,
    team TEXT
);
""")

cur.execute("""
CREATE TABLE priority (
    priority_id INTEGER PRIMARY KEY,
    priority_name TEXT NOT NULL
);
""")

cur.execute("""
CREATE TABLE status (
    status_id INTEGER PRIMARY KEY,
    status_name TEXT NOT NULL
);
""")

cur.execute("""
CREATE TABLE channel (
    channel_id INTEGER PRIMARY KEY,
    channel_name TEXT NOT NULL
);
""")

cur.execute("""
CREATE TABLE tickets (
    ticket_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    agent_id INTEGER,
    priority_id INTEGER,
    status_id INTEGER,
    channel_id INTEGER,
    created_at TEXT,
    resolved_at TEXT,
    sla_met INTEGER,
    reopened INTEGER,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY(agent_id) REFERENCES agents(agent_id),
    FOREIGN KEY(priority_id) REFERENCES priority(priority_id),
    FOREIGN KEY(status_id) REFERENCES status(status_id),
    FOREIGN KEY(channel_id) REFERENCES channel(channel_id)
);
""")

# -------- Populate lookup tables --------
priorities = ["Low", "Medium", "High", "Urgent"]
statuses = ["Open", "Pending", "Closed"]
channels = ["Email", "Phone", "Chat", "Web"]

cur.executemany("INSERT INTO priority (priority_name) VALUES (?);", [(p,) for p in priorities])
cur.executemany("INSERT INTO status (status_name) VALUES (?);", [(s,) for s in statuses])
cur.executemany("INSERT INTO channel (channel_name) VALUES (?);", [(c,) for c in channels])

# -------- Generate customers --------
customer_rows = []
for i in range(1, 50 + 1):
    customer_rows.append((i, fake.name(), fake.email()))
cur.executemany("INSERT INTO customers VALUES (?, ?, ?);", customer_rows)

# -------- Generate agents --------
agent_rows = []
teams = ["Tier 1", "Tier 2", "Escalations", "Billing"]

for i in range(1, 10 + 1):
    agent_rows.append((i, fake.name(), fake.email(), random.choice(teams)))
cur.executemany("INSERT INTO agents VALUES (?, ?, ?, ?);", agent_rows)

# -------- Generate tickets --------
ticket_rows = []
num_tickets = random.randint(300, 500)
start_date = datetime.now() - timedelta(days=120)

for i in range(1, num_tickets + 1):
    customer_id = random.randint(1, 50)
    agent_id = random.randint(1, 10)
    priority_id = random.randint(1, 4)
    status_id = random.randint(1, 3)
    channel_id = random.randint(1, 4)

    created_at = start_date + timedelta(minutes=random.randint(0, 120 * 24 * 60))

    if status_id == 3:  # Closed
        resolve_delay = random.randint(1, 72)
        resolved_at = created_at + timedelta(hours=resolve_delay)
    else:
        resolved_at = None

    sla_threshold = 24
    sla_met = 1 if resolved_at and resolve_delay <= sla_threshold else 0

    reopened = 1 if resolved_at and random.random() < 0.1 else 0  # 10% reopen chance

    ticket_rows.append(
        (
            i,
            customer_id,
            agent_id,
            priority_id,
            status_id,
            channel_id,
            created_at.isoformat(" "),
            resolved_at.isoformat(" ") if resolved_at else None,
            sla_met,
            reopened
        )
    )

cur.executemany("""
INSERT INTO tickets (
    ticket_id, customer_id, agent_id, priority_id, status_id, channel_id,
    created_at, resolved_at, sla_met, reopened
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
""", ticket_rows)

conn.commit()
conn.close()

print(f"✔ Database created at {DB_PATH}")
print(f"✔ {len(ticket_rows)} tickets generated.")
