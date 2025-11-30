# Help Desk Information System (Open-Source MIS Project)

This project is a lightweight Help Desk Information System built using fully open-source tools:  
SQLite, Python, Pandas, Streamlit, diagrams.net, and Jupyter/Colab.  
It simulates realistic support tickets across several months, analyzes performance KPIs, and displays an interactive Streamlit dashboard.

---

## 📂 Project Structure
helpdesk-is/
│
├── README.md
├── requirements.txt
│
├── data/
│   └── tickets.db
│
├── diagrams/
│   ├── process_map.drawio
│   ├── process_map.png
│   ├── erd.drawio
│   └── erd.png
│
├── sql/
│   └── schema.sql
│
├── src/
│   ├── generate_data.py
│   ├── analysis.ipynb
│   └── app.py
│
└── screenshots/
    ├── screenshot_dashboard_home.png
    └── screenshot_filters_and_table.png

---

## 🚀 Setup & Installation

### **1. Install Python Packages**

Run this in the terminal inside your `helpdesk-is` folder:

```bash
pip install -r requirements.txt
# or
python -m pip install -r requirements.txt

---

## 📘 Data Dictionary

### **tickets table**
| Column            | Type    | Description |
|------------------|---------|-------------|
| ticket_id        | INT     | Unique ticket identifier |
| customer_id      | INT     | Links to customers table |
| agent_id         | INT     | Assigned support agent |
| priority_id      | INT     | Priority level (Low → Urgent) |
| status_id        | INT     | Ticket workflow status |
| channel_id       | INT     | Submission channel |
| created_at       | TEXT    | When ticket was opened |
| resolved_at      | TEXT    | When ticket was closed |
| sla_met          | INT     | 1 if SLA met, 0 if not |
| reopened         | INT     | 1 if ticket reopened |

### **customers table**
| Column        | Type | Description |
|---------------|------|-------------|
| customer_id   | INT  | Unique ID |
| name          | TEXT | Customer full name |

### **agents table**
| Column        | Type | Description |
|---------------|------|-------------|
| agent_id      | INT  | Unique agent ID |
| full_name     | TEXT | Name |
| email         | TEXT | Work email |
| team          | TEXT | Support team (Tier 1, Tier 2, Billing, etc.) |

### **priority table**
| priority_id | priority_name |
|-------------|----------------|

### **status table**
| status_id   | status_name   |

### **channel table**
| channel_id  | channel_name  |
