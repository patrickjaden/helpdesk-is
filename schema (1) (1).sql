
-- ==========================================================
-- Help Desk Information System — Complete Schema (DDL)
-- Includes all ERD tables + PK/FK/NOT NULL/CHECK constraints
-- + sensible indexes + timestamp integrity rules
-- ==========================================================


-- ======================
-- Customers Table
-- ======================
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    email       TEXT
);


-- ======================
-- Agents Table
-- ======================
CREATE TABLE agents (
    agent_id   INTEGER PRIMARY KEY,
    full_name  TEXT NOT NULL,
    email      TEXT,
    team       TEXT
);


-- ======================
-- Priority Lookup Table
-- ======================
CREATE TABLE priority (
    priority_id   INTEGER PRIMARY KEY,
    priority_name TEXT NOT NULL UNIQUE
);


-- ======================
-- Status Lookup Table
-- ======================
CREATE TABLE status (
    status_id   INTEGER PRIMARY KEY,
    status_name TEXT NOT NULL UNIQUE
);


-- ======================
-- Channel Lookup Table
-- ======================
CREATE TABLE channel (
    channel_id   INTEGER PRIMARY KEY,
    channel_name TEXT NOT NULL UNIQUE
);


-- ==========================================================
-- Tickets Table (POLISHED VERSION)
-- ==========================================================
CREATE TABLE tickets (
    ticket_id INTEGER PRIMARY KEY,

    customer_id INTEGER NOT NULL,
    agent_id    INTEGER NOT NULL,
    priority_id INTEGER NOT NULL,
    status_id   INTEGER NOT NULL,
    channel_id  INTEGER NOT NULL,

    created_at TEXT NOT NULL,
    resolved_at TEXT,

    -- SLA (0 = failed, 1 = met)
    sla_met INTEGER CHECK (sla_met IN (0, 1)),

    -- Timestamp integrity: resolved_at cannot be before created_at
    CHECK (resolved_at IS NULL OR resolved_at >= created_at),

    -- Foreign Keys
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (agent_id)    REFERENCES agents(agent_id),
    FOREIGN KEY (priority_id) REFERENCES priority(priority_id),
    FOREIGN KEY (status_id)   REFERENCES status(status_id),
    FOREIGN KEY (channel_id)  REFERENCES channel(channel_id)
);


-- ==========================================================
-- Indexes (Sensible for Analytics + Dashboard Filtering)
-- ==========================================================
CREATE INDEX idx_tickets_priority ON tickets(priority_id);
CREATE INDEX idx_tickets_status   ON tickets(status_id);
CREATE INDEX idx_tickets_agent    ON tickets(agent_id);
CREATE INDEX idx_tickets_created  ON tickets(created_at);

