import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

# ---------------------------------------
# Load Database
# ---------------------------------------
DB_PATH = "../data/tickets.db"   # Adjusted for src/app.py location

def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("""
        SELECT 
            t.ticket_id,
            c.name AS customer_name,
            a.full_name AS agent_name,
            p.priority_name AS priority,
            s.status_name AS status,
            ch.channel_name AS channel,
            t.created_at,
            t.resolved_at,
            t.sla_met,
            t.reopened
        FROM tickets t
        JOIN customers c ON c.customer_id = t.customer_id
        JOIN agents a ON a.agent_id = t.agent_id
        JOIN priority p ON p.priority_id = t.priority_id
        JOIN status s ON s.status_id = t.status_id
        JOIN channel ch ON ch.channel_id = t.channel_id
    """, conn, parse_dates=["created_at", "resolved_at"])
    conn.close()
    return df

df = load_data()

# ---------------------------------------
# Sidebar Filters
# ---------------------------------------
st.sidebar.header("🔍 Filters")

# Date Range Filter
min_date = df["created_at"].min()
max_date = df["created_at"].max()

date_range = st.sidebar.date_input(
    "Select date range",
    value=[min_date, max_date]
)

# Priority Filter
priority_filter = st.sidebar.multiselect(
    "Filter by Priority",
    options=sorted(df["priority"].unique()),
    default=sorted(df["priority"].unique())
)

# Agent Filter
agent_filter = st.sidebar.multiselect(
    "Filter by Agent",
    options=sorted(df["agent_name"].unique()),
    default=sorted(df["agent_name"].unique())
)

# Status Filter
status_filter = st.sidebar.multiselect(
    "Filter by Status",
    options=sorted(df["status"].unique()),
    default=sorted(df["status"].unique())
)

# Apply Filters
filtered_df = df[
    (df["created_at"].dt.date >= date_range[0]) &
    (df["created_at"].dt.date <= date_range[1]) &
    (df["priority"].isin(priority_filter)) &
    (df["agent_name"].isin(agent_filter)) &
    (df["status"].isin(status_filter))
]

st.title("🎧 Help Desk Dashboard")

# ---------------------------------------
# KPI Cards
# ---------------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Tickets", len(filtered_df))
col2.metric("Median Resolution (hrs)", 
            round((filtered_df["resolved_at"] - filtered_df["created_at"])
                  .dt.total_seconds().dropna().median() / 3600, 2)
            if filtered_df["resolved_at"].notna().any() else "N/A")

col3.metric("SLA Breach %", 
            f"{100 * (1 - filtered_df['sla_met'].mean()):.2f}%")

col4.metric("Reopen Rate", 
            f"{100 * filtered_df['reopened'].mean():.2f}%")

# ---------------------------------------
# Chart 1 - Weekly Volume
# ---------------------------------------
st.header("📈 Tickets per Week")

weekly = (
    filtered_df
    .set_index("created_at")
    .resample("W")
    .size()
    .reset_index(name="count")
)

fig_week = px.line(
    weekly,
    x="created_at",
    y="count",
    title="Weekly Ticket Volume"
)

st.plotly_chart(fig_week, use_container_width=True)

# ---------------------------------------
# Chart 2 - Tickets by Priority
# ---------------------------------------
st.header("📊 Tickets by Priority")

priority_df = (
    filtered_df["priority"]
    .value_counts()
    .rename_axis("priority")
    .reset_index(name="count")
)

fig_priority = px.bar(
    priority_df,
    x="priority",
    y="count",
    title="Tickets by Priority"
)

st.plotly_chart(fig_priority, use_container_width=True)

# ---------------------------------------
# Chart 3 - Tickets by Agent
# ---------------------------------------
st.header("👤 Tickets by Agent")

agent_df = (
    filtered_df["agent_name"]
    .value_counts()
    .rename_axis("agent_name")
    .reset_index(name="count")
)

fig_agent = px.bar(
    agent_df,
    x="agent_name",
    y="count",
    title="Tickets Assigned per Agent"
)

st.plotly_chart(fig_agent, use_container_width=True)

# ---------------------------------------
# Data Table + Download Button
# ---------------------------------------
st.header("📋 Filtered Tickets Table")

st.dataframe(filtered_df)

csv_export = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download CSV",
    data=csv_export,
    file_name="filtered_tickets.csv",
    mime="text/csv"
)

# ---------------------------------------
# About Section
# ---------------------------------------
st.sidebar.markdown("---")
st.sidebar.subheader("ℹ️ About This App")
st.sidebar.write("""
This dashboard is part of an MIS Help Desk project.

**Assumptions:**
- Synthetic data generated using Faker.
- SLA window: 24 hours.
- Reopen probability: 10%.
- Tickets span 3–6 months.

**Data Refresh:**  
Re-run `generate_data.py` to rebuild `tickets.db`.
""")
