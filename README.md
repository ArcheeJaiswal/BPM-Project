# BPM Compliance Studio

A Streamlit application that models and checks business process compliance using BPMN and Petri Nets.

The project models a Banking Loan Origination workflow across three complexity levels (Basic, Medium, Advanced) with departmental swimlanes, and uses reachability analysis to verify that rules are not violated.

## How to Run

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

## Features

- **BPMN Swimlanes:** View processes divided by department (Front-Office, Risk Dept, Underwriting, Committee).
- **3 Complexity Levels:**
  - **Level 1 (Basic):** Sequential flow with XOR decision gateway.
  - **Level 2 (Medium):** Parallel branches with AND-Split and AND-Join gateways.
  - **Level 3 (Advanced):** Parallel checks with a document rework loop and committee escalation.
- **Petri Net Simulation:** Step-by-step token simulator showing transition firing.
- **Compliance Verification:** DFS reachability check to catch violations (skipping credit checks, missing parallel approvals, unauthorized bypasses).
