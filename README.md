# Compliance Verification Studio ⚖️

An interactive tool to model and formally verify business process compliance using **BPMN 2.0** and **Petri Nets**. The studio performs state-space reachability analysis to mathematically prove whether a business process satisfies regulatory compliance rules before deployment.

---

## ⚡ Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/BPM-Project.git
cd "BPM-Project"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the studio
streamlit run app.py
```
App opens at **`http://localhost:8501`**.

---

## 🚀 Key Features

- **Departmental Swimlanes:** Visualize workflows across organizational departments (Front-Office, Risk Dept, Underwriting, Senior Committee).
- **Automated Petri Net Transformation:** Formal mapping from BPMN constructs (tasks, gateways) to Workflow Nets $(P, T, F, M_0)$.
- **Interactive Token Simulator:** Step-by-step firing mechanism to observe token flow, parallel concurrency (AND-split), and synchronization (AND-join).
- **Exhaustive Reachability Analysis:** DFS state-space explorer discovering all execution paths, interleavings, and bounded rework loops.
- **Compliance & Diagnostic Audit:** Detects unauthorized bypasses, missing checks, and governance violations with root-cause reports.

---

## 📊 The 3 Architectural Levels (Loan Origination)

| Level | Architecture | Swimlanes | Key Mechanism Caught |
| :--- | :--- | :--- | :--- |
| **🟢 Level 1: Basic** | Sequential + XOR Gateway | 3 Lanes | XOR bypass skipping mandatory Credit Check. |
| **🟡 Level 2: Medium** | Parallel Concurrency (AND-Split / AND-Join) | 4 Lanes | Concurrency sync bypass skipping Financial Risk. |
| **🔴 Level 3: Advanced** | Parallel + Rework Loop + Escalation | 4 Lanes | Executive override bypassing Senior Committee quorum. |

---

## 📂 Project Structure

```
├── app.py           # Streamlit UI controller & dashboard
├── catalog.py       # BPMN DOT graphs, Petri net specs & compliance rules
├── simulation.py    # Petri net operational semantics & token firing
├── reachability.py  # DFS reachability engine over state space
├── verifier.py      # Regulatory rule checking & path audit
├── visualizer.py    # Graphviz renderer with swimlane subgraphs
├── styles.py        # Clean UI styling & custom badges
└── requirements.txt # Python dependencies
```

---

## 🛠️ Tech Stack

- **Python 3.8+**
- **Streamlit** (Interactive Web UI)
- **Graphviz** (Dynamic BPMN & Petri Net rendering)

---

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.
