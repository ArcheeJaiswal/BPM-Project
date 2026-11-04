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

- **True BPMN 2.0 Grid Swimlanes:** Full-width continuous horizontal swimlanes with vertical left-side headers and orthogonal (Manhattan) connectors, matching standard industry BPMN diagrams (SVG vector export available).
- **Multi-Gateway Support:**
  - **Exclusive Gateway (XOR):** Decision branching (`×`) for alternative conditional routes.
  - **Parallel Gateway (AND):** Concurrent thread fork (`+`) and token synchronization join (`+`).
  - **Inclusive Gateway (OR):** Multi-choice branching (`◯`) activating one, several, or all branches concurrently (e.g. Real Estate Appraisal, Corporate Guarantor Audit, or both) and synchronizing whichever branches fired.
  - **Complex / Evaluation Gateway:** Multi-condition decision aggregation (e.g. tripartite evaluation count satisfaction).
- **Architectural Complexity Levels:**
  - **Level 1 (Basic):** Sequential flow with Exclusive (XOR) decision gateway.
  - **Level 2 (Medium):** Parallel branches with AND-Split (Fork) and AND-Join (Synchronization) gateways.
  - **Level 3 (Advanced):** Multi-Gateway enterprise syndicated lending pipeline combining Parallel (AND), Inclusive (OR), and Exclusive (XOR) gateways with a document rework loop and committee escalation across continuous horizontal swimlanes.
- **Petri Net Simulation:** Step-by-step token simulator showing transition firing.
- **Compliance Verification:** DFS reachability check to catch violations (skipping credit checks, missing parallel approvals, unauthorized bypasses).
