"""
========================================================================================
Process Catalog & Model Definitions
========================================================================================
Defines the unified enterprise domain: Banking Loan Origination across
three progressive architectural complexity levels:
  - Level 1: Basic (Sequential Flow + Exclusive XOR Decision)
  - Level 2: Medium (Parallel Concurrency via AND-Split Fork & AND-Join Synchronization)
  - Level 3: Advanced (Enterprise Multi-Tier Governance, Concurrency & Document Rework Loop)

Features:
  - Dual BPMN Representations: Streamlined Control-Flow View AND Swimlane Organizational View.
  - Multi-Lane Petri Net Tuples (P, T, F, M0) tagged with organizational departments.
  - Formal Compliance Precedence Rules and Diagnostic Remediation Guidelines.
========================================================================================
"""

COMPLEXITY_CATALOG = {
    "level1": {
        "title": "Level 1: Basic Loan Approval",
        "domain": "Retail Banking (Standard Personal Loan)",
        "complexity_level": "Level 1: Basic",
        "complexity_badge": "🟢 Basic",
        "architecture_summary": "Sequential Control-Flow with Exclusive (XOR) Decision Gateway",
        "concurrency_degree": "1 Token (Sequential / Safe WF-Net)",
        "swimlane_roles": [
            "Lane 1: Front-Office Desk (Intake)",
            "Lane 2: Credit & Risk Analysis Dept",
            "Lane 3: Loan Officer (Approval Authority)"
        ],
        "rule_text": "A loan must not be approved without a preceding credit check.",
        "rule_spec": {
            "prerequisite": "Credit Check",
            "target": "Approve Loan"
        },
        "description": (
            "A standard retail loan origination process. A customer submits an application. "
            "The bank performs a mandatory Credit Check. Based on creditworthiness, the loan "
            "officer makes an exclusive (XOR) decision to either Approve or Reject the loan."
        ),
        "remediation": {
            "violation_title": "XOR Bypass Around Mandatory Prerequisite",
            "root_cause": "An unauthorized sequence flow bypasses the Credit Check activity and connects directly to the Loan Approval gateway, skipping the Credit & Risk Dept swimlane.",
            "remediation": "Remove the cross-lane bypass flow edge. Enforce that the Credit Check activity in Lane 2 is a mandatory predecessor to the approval decision."
        },
        "compliant": {
            "description": "Standard regulatory-compliant linear flow. Every application strictly undergoes a Credit Check before any loan approval or rejection decision.",
            "bpmn_dot": """
            digraph BPMN_L1_Compliant {
                rankdir=LR;
                node [fontname="Helvetica, Arial, sans-serif", fontsize=11];
                edge [fontname="Helvetica, Arial, sans-serif", fontsize=10, color="#334155"];

                start [shape=circle, label="", width=0.35, height=0.35, style=filled, fillcolor="#86EFAC", color="#16A34A", penwidth=2];
                t_recv [shape=rect, style="rounded,filled", fillcolor="#DBEAFE", color="#2563EB", penwidth=1.5, label="Submit Application"];
                t_check [shape=rect, style="rounded,filled", fillcolor="#DBEAFE", color="#2563EB", penwidth=1.5, label="Credit Check\\n(Mandatory)"];
                xor_dec [shape=diamond, width=0.45, height=0.45, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.5, label="×", fontsize=16];
                t_app [shape=rect, style="rounded,filled", fillcolor="#DCFCE7", color="#16A34A", penwidth=1.5, label="Approve Loan"];
                t_rej [shape=rect, style="rounded,filled", fillcolor="#FEE2E2", color="#DC2626", penwidth=1.5, label="Reject Loan"];
                end_app [shape=doublecircle, label="", width=0.35, height=0.35, style=filled, fillcolor="#FCA5A5", color="#DC2626", penwidth=2];
                end_rej [shape=doublecircle, label="", width=0.35, height=0.35, style=filled, fillcolor="#FCA5A5", color="#DC2626", penwidth=2];

                start -> t_recv;
                t_recv -> t_check;
                t_check -> xor_dec;
                xor_dec -> t_app [label="Eligible"];
                xor_dec -> t_rej [label="Ineligible"];
                t_app -> end_app;
                t_rej -> end_rej;
            }
            """,
            "bpmn_swimlane_dot": """
            digraph BPMN_L1_Swimlane_Compliant {
                rankdir=LR;
                compound=true;
                newrank=true;
                node [fontname="Helvetica, Arial, sans-serif", fontsize=10];
                edge [fontname="Helvetica, Arial, sans-serif", fontsize=9, color="#334155"];

                # Pool 1: Customer / Borrower Portal (Top Pool)
                subgraph cluster_pool_portal {
                    label = "🏊 Pool: Customer / Borrower Portal";
                    style = "filled,rounded";
                    fillcolor = "#F0FDF4";
                    color = "#16A34A";
                    penwidth = 2.0;
                    fontsize = 12;
                    fontcolor = "#166534";

                    p_start [shape=circle, label="", width=0.32, height=0.32, style=filled, fillcolor="#86EFAC", color="#16A34A", penwidth=2];
                    p_submit [shape=rect, style="rounded,filled", fillcolor="#FFFFFF", color="#16A34A", penwidth=1.5, label="👤 Access Portal &\\nSubmit Loan Request"];
                    p_receive_dec [shape=rect, style="rounded,filled", fillcolor="#FFFFFF", color="#16A34A", penwidth=1.5, label="✉️ Receive Loan\\nDecision Letter"];
                    p_end [shape=doublecircle, label="", width=0.32, height=0.32, style=filled, fillcolor="#FCA5A5", color="#DC2626", penwidth=2];

                    p_start -> p_submit;
                    p_receive_dec -> p_end;
                }

                # Pool 2: Loan Provider Organization (Outer box containing internal swimlanes)
                subgraph cluster_pool_provider {
                    label = "🏦 Pool: Loan Provider (Financial Institution)";
                    style = "filled";
                    fillcolor = "#FFFFFF";
                    color = "#1E3A8A";
                    penwidth = 2.5;
                    fontsize = 13;
                    fontcolor = "#1E3A8A";

                    subgraph cluster_lane_frontoffice {
                        label = "🏊 Lane 1: Front-Office Desk (Intake)";
                        style = "filled,rounded";
                        fillcolor = "#EFF6FF";
                        color = "#3B82F6";
                        penwidth = 1.5;
                        fontsize = 11;
                        fontcolor = "#1D4ED8";

                        t_recv [shape=rect, style="rounded,filled", fillcolor="#FFFFFF", color="#2563EB", penwidth=1.5, label="Create Loan Dossier"];
                    }

                    subgraph cluster_lane_risk {
                        label = "🏊 Lane 2: Credit & Risk Analysis Dept";
                        style = "filled,rounded";
                        fillcolor = "#FEFCE8";
                        color = "#F59E0B";
                        penwidth = 1.5;
                        fontsize = 11;
                        fontcolor = "#B45309";

                        t_check [shape=rect, style="rounded,filled", fillcolor="#FFFFFF", color="#2563EB", penwidth=1.5, label="Credit Check\\n(Mandatory Prerequisite)"];
                    }

                    subgraph cluster_lane_underwriting {
                        label = "🏊 Lane 3: Loan Officer (Approval Authority)";
                        style = "filled,rounded";
                        fillcolor = "#FAF5FF";
                        color = "#A855F7";
                        penwidth = 1.5;
                        fontsize = 11;
                        fontcolor = "#7E22CE";

                        xor_dec [shape=diamond, width=0.42, height=0.42, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.5, label="×", fontsize=14, tooltip="Exclusive Decision (XOR)"];
                        t_app [shape=rect, style="rounded,filled", fillcolor="#DCFCE7", color="#16A34A", penwidth=1.5, label="Approve Loan"];
                        t_rej [shape=rect, style="rounded,filled", fillcolor="#FEE2E2", color="#DC2626", penwidth=1.5, label="Reject Loan"];
                        t_notify [shape=rect, style="rounded,filled", fillcolor="#FFFFFF", color="#7E22CE", penwidth=1.5, label="✉️ Dispatch Decision\\nNotification"];
                        end_app [shape=doublecircle, label="", width=0.32, height=0.32, style=filled, fillcolor="#FCA5A5", color="#DC2626", penwidth=2];
                        end_rej [shape=doublecircle, label="", width=0.32, height=0.32, style=filled, fillcolor="#FCA5A5", color="#DC2626", penwidth=2];
                    }

                    # Sequence Flows inside Loan Provider
                    t_recv -> t_check [label="Cross-Lane Handoff"];
                    t_check -> xor_dec [label="Risk Report"];
                    xor_dec -> t_app [label="Eligible"];
                    xor_dec -> t_rej [label="Ineligible"];
                    t_app -> t_notify;
                    t_rej -> t_notify;
                    t_app -> end_app;
                    t_rej -> end_rej;
                }

                # Cross-Pool Message Flows (Dashed arrows, exactly like BPMN standards)
                p_submit -> t_recv [label="Application Dossier", style=dashed, color="#2563EB", penwidth=1.3];
                t_notify -> p_receive_dec [label="Decision Letter", style=dashed, color="#2563EB", penwidth=1.3];
            }
            """,
            "petri_net": {
                "places": [
                    {"id": "p_start", "label": "p_start (Application Submitted)", "initial_tokens": 1, "lane": "Lane 1: Front-Office Desk"},
                    {"id": "p_received", "label": "p_received (Awaiting Credit Check)", "initial_tokens": 0, "lane": "Lane 2: Credit & Risk Dept"},
                    {"id": "p_checked", "label": "p_checked (Credit Check Complete)", "initial_tokens": 0, "lane": "Lane 3: Loan Officer"},
                    {"id": "p_end", "label": "p_end (Process Terminated)", "initial_tokens": 0, "lane": "Lane 3: Loan Officer"}
                ],
                "transitions": {
                    "t_recv": {
                        "label": "Submit Application",
                        "inputs": ["p_start"],
                        "outputs": ["p_received"],
                        "type": "standard",
                        "lane": "Lane 1: Front-Office Desk"
                    },
                    "t_check": {
                        "label": "Credit Check",
                        "inputs": ["p_received"],
                        "outputs": ["p_checked"],
                        "type": "prerequisite",
                        "lane": "Lane 2: Credit & Risk Dept"
                    },
                    "t_app": {
                        "label": "Approve Loan",
                        "inputs": ["p_checked"],
                        "outputs": ["p_end"],
                        "type": "decision",
                        "lane": "Lane 3: Loan Officer"
                    },
                    "t_rej": {
                        "label": "Reject Loan",
                        "inputs": ["p_checked"],
                        "outputs": ["p_end"],
                        "type": "decision",
                        "lane": "Lane 3: Loan Officer"
                    }
                },
                "initial_marking": {"p_start": 1, "p_received": 0, "p_checked": 0, "p_end": 0},
                "final_place": "p_end"
            }
        },
        "violating": {
            "description": "Flawed process design with an unauthorized cross-lane bypass path. An XOR gateway permits approving loans directly without the Credit & Risk Dept lane.",
            "bpmn_dot": """
            digraph BPMN_L1_Violating {
                rankdir=LR;
                node [fontname="Helvetica, Arial, sans-serif", fontsize=11];
                edge [fontname="Helvetica, Arial, sans-serif", fontsize=10, color="#334155"];

                start [shape=circle, label="", width=0.35, height=0.35, style=filled, fillcolor="#86EFAC", color="#16A34A", penwidth=2];
                t_recv [shape=rect, style="rounded,filled", fillcolor="#DBEAFE", color="#2563EB", penwidth=1.5, label="Submit Application"];
                xor_split [shape=diamond, width=0.45, height=0.45, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.5, label="×", fontsize=16];
                t_check [shape=rect, style="rounded,filled", fillcolor="#DBEAFE", color="#2563EB", penwidth=1.5, label="Credit Check\\n(Mandatory)"];
                xor_dec [shape=diamond, width=0.45, height=0.45, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.5, label="×", fontsize=16];
                t_app [shape=rect, style="rounded,filled", fillcolor="#DCFCE7", color="#16A34A", penwidth=1.5, label="Approve Loan"];
                t_rej [shape=rect, style="rounded,filled", fillcolor="#FEE2E2", color="#DC2626", penwidth=1.5, label="Reject Loan"];
                end_app [shape=doublecircle, label="", width=0.35, height=0.35, style=filled, fillcolor="#FCA5A5", color="#DC2626", penwidth=2];
                end_rej [shape=doublecircle, label="", width=0.35, height=0.35, style=filled, fillcolor="#FCA5A5", color="#DC2626", penwidth=2];

                start -> t_recv;
                t_recv -> xor_split;
                xor_split -> t_check [label="Standard Route"];
                t_check -> xor_dec;
                xor_dec -> t_app [label="Eligible"];
                xor_dec -> t_rej [label="Ineligible"];
                
                # Compliance Violation Bypass Edge
                xor_split -> t_app [label="⚠️ Bypass Credit Check (Violation)", color="#DC2626", fontcolor="#DC2626", style=dashed, penwidth=2];

                t_app -> end_app;
                t_rej -> end_rej;
            }
            """,
            "bpmn_swimlane_dot": """
            digraph BPMN_L1_Swimlane_Violating {
                rankdir=LR;
                compound=true;
                newrank=true;
                node [fontname="Helvetica, Arial, sans-serif", fontsize=10];
                edge [fontname="Helvetica, Arial, sans-serif", fontsize=9, color="#334155"];

                # Pool 1: Customer / Borrower Portal (Top Pool)
                subgraph cluster_pool_portal {
                    label = "🏊 Pool: Customer / Borrower Portal";
                    style = "filled,rounded";
                    fillcolor = "#F0FDF4";
                    color = "#16A34A";
                    penwidth = 2.0;
                    fontsize = 12;
                    fontcolor = "#166534";

                    p_start [shape=circle, label="", width=0.32, height=0.32, style=filled, fillcolor="#86EFAC", color="#16A34A", penwidth=2];
                    p_submit [shape=rect, style="rounded,filled", fillcolor="#FFFFFF", color="#16A34A", penwidth=1.5, label="👤 Access Portal &\\nSubmit Loan Request"];
                    p_receive_dec [shape=rect, style="rounded,filled", fillcolor="#FFFFFF", color="#16A34A", penwidth=1.5, label="✉️ Receive Loan\\nDecision Letter"];
                    p_end [shape=doublecircle, label="", width=0.32, height=0.32, style=filled, fillcolor="#FCA5A5", color="#DC2626", penwidth=2];

                    p_start -> p_submit;
                    p_receive_dec -> p_end;
                }

                # Pool 2: Loan Provider Organization (Outer box containing internal swimlanes)
                subgraph cluster_pool_provider {
                    label = "🏦 Pool: Loan Provider (Financial Institution)";
                    style = "filled";
                    fillcolor = "#FFFFFF";
                    color = "#1E3A8A";
                    penwidth = 2.5;
                    fontsize = 13;
                    fontcolor = "#1E3A8A";

                    subgraph cluster_lane_frontoffice {
                        label = "🏊 Lane 1: Front-Office Desk (Intake)";
                        style = "filled,rounded";
                        fillcolor = "#EFF6FF";
                        color = "#3B82F6";
                        penwidth = 1.5;
                        fontsize = 11;
                        fontcolor = "#1D4ED8";

                        t_recv [shape=rect, style="rounded,filled", fillcolor="#FFFFFF", color="#2563EB", penwidth=1.5, label="Create Loan Dossier"];
                        xor_split [shape=diamond, width=0.42, height=0.42, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.5, label="×", fontsize=14, tooltip="Exclusive Route (XOR)"];
                    }

                    subgraph cluster_lane_risk {
                        label = "🏊 Lane 2: Credit & Risk Analysis Dept";
                        style = "filled,rounded";
                        fillcolor = "#FEFCE8";
                        color = "#F59E0B";
                        penwidth = 1.5;
                        fontsize = 11;
                        fontcolor = "#B45309";

                        t_check [shape=rect, style="rounded,filled", fillcolor="#FFFFFF", color="#2563EB", penwidth=1.5, label="Credit Check\\n(Mandatory Prerequisite)"];
                    }

                    subgraph cluster_lane_underwriting {
                        label = "🏊 Lane 3: Loan Officer (Approval Authority)";
                        style = "filled,rounded";
                        fillcolor = "#FAF5FF";
                        color = "#A855F7";
                        penwidth = 1.5;
                        fontsize = 11;
                        fontcolor = "#7E22CE";

                        xor_dec [shape=diamond, width=0.42, height=0.42, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.5, label="×", fontsize=14, tooltip="Exclusive Decision (XOR)"];
                        t_app [shape=rect, style="rounded,filled", fillcolor="#DCFCE7", color="#16A34A", penwidth=1.5, label="Approve Loan"];
                        t_rej [shape=rect, style="rounded,filled", fillcolor="#FEE2E2", color="#DC2626", penwidth=1.5, label="Reject Loan"];
                        t_notify [shape=rect, style="rounded,filled", fillcolor="#FFFFFF", color="#7E22CE", penwidth=1.5, label="✉️ Dispatch Decision\\nNotification"];
                        end_app [shape=doublecircle, label="", width=0.32, height=0.32, style=filled, fillcolor="#FCA5A5", color="#DC2626", penwidth=2];
                        end_rej [shape=doublecircle, label="", width=0.32, height=0.32, style=filled, fillcolor="#FCA5A5", color="#DC2626", penwidth=2];
                    }

                    # Sequence Flows inside Loan Provider
                    t_recv -> xor_split;
                    xor_split -> t_check [label="Standard Route"];
                    t_check -> xor_dec [label="Handoff"];
                    xor_dec -> t_app [label="Eligible"];
                    xor_dec -> t_rej [label="Ineligible"];

                    # Cross-Lane Violation Bypass Edge
                    xor_split -> t_app [label="⚠️ Cross-Lane Bypass (Skip Lane 2)", color="#DC2626", fontcolor="#DC2626", style=dashed, penwidth=2.2];

                    t_app -> t_notify;
                    t_rej -> t_notify;
                    t_app -> end_app;
                    t_rej -> end_rej;
                }

                # Cross-Pool Message Flows
                p_submit -> t_recv [label="Application Dossier", style=dashed, color="#2563EB", penwidth=1.3];
                t_notify -> p_receive_dec [label="Decision Letter", style=dashed, color="#2563EB", penwidth=1.3];
            }
            """,
            "petri_net": {
                "places": [
                    {"id": "p_start", "label": "p_start (Application Submitted)", "initial_tokens": 1, "lane": "Lane 1: Front-Office Desk"},
                    {"id": "p_received", "label": "p_received (Awaiting Decision/Check)", "initial_tokens": 0, "lane": "Lane 1: Front-Office Desk"},
                    {"id": "p_checked", "label": "p_checked (Credit Check Complete)", "initial_tokens": 0, "lane": "Lane 2: Credit & Risk Dept"},
                    {"id": "p_bypassed", "label": "p_bypassed (Check Skipped)", "initial_tokens": 0, "lane": "Lane 3: Loan Officer"},
                    {"id": "p_end", "label": "p_end (Process Terminated)", "initial_tokens": 0, "lane": "Lane 3: Loan Officer"}
                ],
                "transitions": {
                    "t_recv": {
                        "label": "Submit Application",
                        "inputs": ["p_start"],
                        "outputs": ["p_received"],
                        "type": "standard",
                        "lane": "Lane 1: Front-Office Desk"
                    },
                    "t_check": {
                        "label": "Credit Check",
                        "inputs": ["p_received"],
                        "outputs": ["p_checked"],
                        "type": "prerequisite",
                        "lane": "Lane 2: Credit & Risk Dept"
                    },
                    "t_bypass": {
                        "label": "Bypass Credit Check",
                        "inputs": ["p_received"],
                        "outputs": ["p_bypassed"],
                        "type": "violation",
                        "lane": "Lane 1: Front-Office Desk"
                    },
                    "t_app": {
                        "label": "Approve Loan",
                        "inputs": ["p_checked"],
                        "outputs": ["p_end"],
                        "type": "decision",
                        "lane": "Lane 3: Loan Officer"
                    },
                    "t_rej": {
                        "label": "Reject Loan",
                        "inputs": ["p_checked"],
                        "outputs": ["p_end"],
                        "type": "decision",
                        "lane": "Lane 3: Loan Officer"
                    },
                    "t_bypass_app": {
                        "label": "Approve Loan (Unchecked)",
                        "inputs": ["p_bypassed"],
                        "outputs": ["p_end"],
                        "type": "violation",
                        "lane": "Lane 3: Loan Officer"
                    }
                },
                "initial_marking": {"p_start": 1, "p_received": 0, "p_checked": 0, "p_bypassed": 0, "p_end": 0},
                "final_place": "p_end"
            }
        }
    },

    "level2": {
        "title": "Level 2: Medium (Parallel Concurrency)",
        "domain": "Commercial & Mortgage Lending",
        "complexity_level": "Level 2: Medium",
        "complexity_badge": "🟡 Medium",
        "architecture_summary": "Parallel Concurrency via AND-Split (Fork) and AND-Join (Synchronization)",
        "concurrency_degree": "2 Concurrent Tokens (Multi-Threaded Petri Net)",
        "swimlane_roles": [
            "Lane 1: Loan Origination & Intake Desk",
            "Lane 2: Financial Risk Assessment Dept",
            "Lane 3: Legal & AML / KYC Compliance Dept",
            "Lane 4: Commercial Underwriting Officer"
        ],
        "rule_text": "A loan must not be approved without completing BOTH Credit Risk Assessment and KYC/AML Identity Verification.",
        "rule_spec": {
            "prerequisite": ["Credit Risk Assessment", "KYC Identity Verification"],
            "target": "Approve Loan"
        },
        "description": (
            "Mortgage and commercial loan applications require dual independent verification under federal regulations: "
            "(1) Financial Credit Risk Assessment and (2) KYC / Anti-Money Laundering (AML) Identity Verification. "
            "These two tasks execute concurrently across separate departments (Swimlanes 2 & 3). An AND-Join gateway synchronizes "
            "both results in Lane 4 before the underwriting team can approve or reject the application."
        ),
        "remediation": {
            "violation_title": "Premature Approval & Cross-Lane Synchronization Bypass",
            "root_cause": "An unauthorized transition allows approving the loan without waiting for the Financial Risk Assessment department (Lane 2) to complete and synchronize at the AND-Join.",
            "remediation": "Enforce strict AND-Join synchronization. In the Petri net, ensure transition 'Approve Loan' in Lane 4 requires tokens from both parallel departmental assessment places before enabling."
        },
        "compliant": {
            "description": "Compliant concurrent workflow. Both parallel departmental branches strictly execute and synchronize via AND-Join before the loan decision.",
            "bpmn_dot": """
            digraph BPMN_L2_Compliant {
                rankdir=LR;
                node [fontname="Helvetica, Arial, sans-serif", fontsize=11];
                edge [fontname="Helvetica, Arial, sans-serif", fontsize=10, color="#334155"];

                start [shape=circle, label="", width=0.35, height=0.35, style=filled, fillcolor="#86EFAC", color="#16A34A", penwidth=2];
                t_recv [shape=rect, style="rounded,filled", fillcolor="#DBEAFE", color="#2563EB", penwidth=1.5, label="Submit Application"];
                and_split [shape=diamond, width=0.45, height=0.45, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.5, label="+", fontsize=18];
                t_credit [shape=rect, style="rounded,filled", fillcolor="#DBEAFE", color="#2563EB", penwidth=1.5, label="Credit Risk Assessment\\n(Mandatory)"];
                t_kyc [shape=rect, style="rounded,filled", fillcolor="#DBEAFE", color="#2563EB", penwidth=1.5, label="KYC Identity Verification\\n(Mandatory)"];
                and_join [shape=diamond, width=0.45, height=0.45, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.5, label="+", fontsize=18];
                xor_dec [shape=diamond, width=0.45, height=0.45, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.5, label="×", fontsize=16];
                t_app [shape=rect, style="rounded,filled", fillcolor="#DCFCE7", color="#16A34A", penwidth=1.5, label="Approve Loan"];
                t_rej [shape=rect, style="rounded,filled", fillcolor="#FEE2E2", color="#DC2626", penwidth=1.5, label="Reject Loan"];
                end_app [shape=doublecircle, label="", width=0.35, height=0.35, style=filled, fillcolor="#FCA5A5", color="#DC2626", penwidth=2];
                end_rej [shape=doublecircle, label="", width=0.35, height=0.35, style=filled, fillcolor="#FCA5A5", color="#DC2626", penwidth=2];

                start -> t_recv;
                t_recv -> and_split;
                and_split -> t_credit [label="Parallel Branch 1"];
                and_split -> t_kyc [label="Parallel Branch 2"];
                t_credit -> and_join;
                t_kyc -> and_join;
                and_join -> xor_dec;
                xor_dec -> t_app [label="Eligible"];
                xor_dec -> t_rej [label="Ineligible"];
                t_app -> end_app;
                t_rej -> end_rej;
            }
            """,
            "bpmn_swimlane_dot": """
            digraph BPMN_L2_Swimlane_Compliant {
                rankdir=LR;
                compound=true;
                newrank=true;
                node [fontname="Helvetica, Arial, sans-serif", fontsize=10];
                edge [fontname="Helvetica, Arial, sans-serif", fontsize=9, color="#334155"];

                # Pool 1: Commercial Borrower Portal (Top Pool)
                subgraph cluster_pool_portal {
                    label = "🏊 Pool: Commercial Borrower Portal";
                    style = "filled,rounded";
                    fillcolor = "#F0FDF4";
                    color = "#16A34A";
                    penwidth = 2.0;
                    fontsize = 12;
                    fontcolor = "#166534";

                    p_start [shape=circle, label="", width=0.32, height=0.32, style=filled, fillcolor="#86EFAC", color="#16A34A", penwidth=2];
                    p_submit [shape=rect, style="rounded,filled", fillcolor="#FFFFFF", color="#16A34A", penwidth=1.5, label="👤 Access Portal &\\nSubmit Commercial Dossier"];
                    p_receive_dec [shape=rect, style="rounded,filled", fillcolor="#FFFFFF", color="#16A34A", penwidth=1.5, label="✉️ Receive Commitment\\nApproval Notice"];
                    p_end [shape=doublecircle, label="", width=0.32, height=0.32, style=filled, fillcolor="#FCA5A5", color="#DC2626", penwidth=2];

                    p_start -> p_submit;
                    p_receive_dec -> p_end;
                }

                # Pool 2: Commercial Loan Provider (Outer box containing internal departmental swimlanes)
                subgraph cluster_pool_provider {
                    label = "🏦 Pool: Commercial Loan Provider (Financial Institution)";
                    style = "filled";
                    fillcolor = "#FFFFFF";
                    color = "#1E3A8A";
                    penwidth = 2.5;
                    fontsize = 13;
                    fontcolor = "#1E3A8A";

                    subgraph cluster_lane_intake {
                        label = "🏊 Lane 1: Loan Origination & Intake Desk";
                        style = "filled,rounded";
                        fillcolor = "#EFF6FF";
                        color = "#3B82F6";
                        penwidth = 1.5;
                        fontsize = 11;
                        fontcolor = "#1D4ED8";

                        t_recv [shape=rect, style="rounded,filled", fillcolor="#FFFFFF", color="#2563EB", penwidth=1.5, label="Initialize Commercial File"];
                        and_split [shape=diamond, width=0.42, height=0.42, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.5, label="+", fontsize=16, tooltip="Parallel Fork (AND-Split)"];
                    }

                    subgraph cluster_lane_risk {
                        label = "🏊 Lane 2: Financial Risk Assessment Dept";
                        style = "filled,rounded";
                        fillcolor = "#FEFCE8";
                        color = "#F59E0B";
                        penwidth = 1.5;
                        fontsize = 11;
                        fontcolor = "#B45309";

                        t_credit [shape=rect, style="rounded,filled", fillcolor="#FFFFFF", color="#2563EB", penwidth=1.5, label="Credit Risk Assessment\\n(Mandatory Prerequisite)"];
                    }

                    subgraph cluster_lane_compliance {
                        label = "🏊 Lane 3: Legal & AML / KYC Compliance Dept";
                        style = "filled,rounded";
                        fillcolor = "#FFF1F2";
                        color = "#F43F5E";
                        penwidth = 1.5;
                        fontsize = 11;
                        fontcolor = "#BE123C";

                        t_kyc [shape=rect, style="rounded,filled", fillcolor="#FFFFFF", color="#2563EB", penwidth=1.5, label="KYC Identity Verification\\n(Mandatory Prerequisite)"];
                    }

                    subgraph cluster_lane_underwriting {
                        label = "🏊 Lane 4: Commercial Underwriting Officer";
                        style = "filled,rounded";
                        fillcolor = "#FAF5FF";
                        color = "#A855F7";
                        penwidth = 1.5;
                        fontsize = 11;
                        fontcolor = "#7E22CE";

                        and_join [shape=diamond, width=0.42, height=0.42, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.5, label="+", fontsize=16, tooltip="Parallel Synchronization (AND-Join)"];
                        xor_dec [shape=diamond, width=0.42, height=0.42, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.5, label="×", fontsize=14, tooltip="Exclusive Decision (XOR)"];
                        t_app [shape=rect, style="rounded,filled", fillcolor="#DCFCE7", color="#16A34A", penwidth=1.5, label="Approve Loan"];
                        t_rej [shape=rect, style="rounded,filled", fillcolor="#FEE2E2", color="#DC2626", penwidth=1.5, label="Reject Loan"];
                        t_notify [shape=rect, style="rounded,filled", fillcolor="#FFFFFF", color="#7E22CE", penwidth=1.5, label="✉️ Send Underwriting\\nCommitment"];
                        end_app [shape=doublecircle, label="", width=0.32, height=0.32, style=filled, fillcolor="#FCA5A5", color="#DC2626", penwidth=2];
                        end_rej [shape=doublecircle, label="", width=0.32, height=0.32, style=filled, fillcolor="#FCA5A5", color="#DC2626", penwidth=2];
                    }

                    # Sequence Flows inside Loan Provider
                    t_recv -> and_split;
                    and_split -> t_credit [label="Concurrent Branch 1"];
                    and_split -> t_kyc [label="Concurrent Branch 2"];
                    t_credit -> and_join [label="Risk Cleared"];
                    t_kyc -> and_join [label="KYC Cleared"];
                    and_join -> xor_dec [label="Synchronized"];
                    xor_dec -> t_app [label="Eligible"];
                    xor_dec -> t_rej [label="Ineligible"];
                    t_app -> t_notify;
                    t_rej -> t_notify;
                    t_app -> end_app;
                    t_rej -> end_rej;
                }

                # Cross-Pool Message Flows (Dashed lines, matching picture!)
                p_submit -> t_recv [label="Commercial Dossier", style=dashed, color="#2563EB", penwidth=1.3];
                t_notify -> p_receive_dec [label="Commitment Notice", style=dashed, color="#2563EB", penwidth=1.3];
            }
            """,
            "petri_net": {
                "places": [
                    {"id": "p_start", "label": "p_start (Application Submitted)", "initial_tokens": 1, "lane": "Lane 1: Intake Desk"},
                    {"id": "p_split", "label": "p_split (Ready for Parallel Vetting)", "initial_tokens": 0, "lane": "Lane 1: Intake Desk"},
                    {"id": "p_cred_wait", "label": "p_cred_wait (Awaiting Credit Check)", "initial_tokens": 0, "lane": "Lane 2: Financial Risk Dept"},
                    {"id": "p_kyc_wait", "label": "p_kyc_wait (Awaiting KYC Check)", "initial_tokens": 0, "lane": "Lane 3: Legal & Compliance"},
                    {"id": "p_cred_done", "label": "p_cred_done (Credit Check Finished)", "initial_tokens": 0, "lane": "Lane 2: Financial Risk Dept"},
                    {"id": "p_kyc_done", "label": "p_kyc_done (KYC Finished)", "initial_tokens": 0, "lane": "Lane 3: Legal & Compliance"},
                    {"id": "p_synced", "label": "p_synced (Both Audits Synchronized)", "initial_tokens": 0, "lane": "Lane 4: Underwriting Officer"},
                    {"id": "p_end", "label": "p_end (Process Terminated)", "initial_tokens": 0, "lane": "Lane 4: Underwriting Officer"}
                ],
                "transitions": {
                    "t_submit": {
                        "label": "Submit Application",
                        "inputs": ["p_start"],
                        "outputs": ["p_split"],
                        "type": "standard",
                        "lane": "Lane 1: Intake Desk"
                    },
                    "t_and_split": {
                        "label": "AND-Split (Fork)",
                        "inputs": ["p_split"],
                        "outputs": ["p_cred_wait", "p_kyc_wait"],
                        "type": "standard",
                        "lane": "Lane 1: Intake Desk"
                    },
                    "t_credit": {
                        "label": "Credit Risk Assessment",
                        "inputs": ["p_cred_wait"],
                        "outputs": ["p_cred_done"],
                        "type": "prerequisite",
                        "lane": "Lane 2: Financial Risk Dept"
                    },
                    "t_kyc": {
                        "label": "KYC Identity Verification",
                        "inputs": ["p_kyc_wait"],
                        "outputs": ["p_kyc_done"],
                        "type": "prerequisite",
                        "lane": "Lane 3: Legal & Compliance"
                    },
                    "t_and_join": {
                        "label": "AND-Join (Synchronize)",
                        "inputs": ["p_cred_done", "p_kyc_done"],
                        "outputs": ["p_synced"],
                        "type": "standard",
                        "lane": "Lane 4: Underwriting Officer"
                    },
                    "t_app": {
                        "label": "Approve Loan",
                        "inputs": ["p_synced"],
                        "outputs": ["p_end"],
                        "type": "decision",
                        "lane": "Lane 4: Underwriting Officer"
                    },
                    "t_rej": {
                        "label": "Reject Loan",
                        "inputs": ["p_synced"],
                        "outputs": ["p_end"],
                        "type": "decision",
                        "lane": "Lane 4: Underwriting Officer"
                    }
                },
                "initial_marking": {
                    "p_start": 1, "p_split": 0, "p_cred_wait": 0, "p_kyc_wait": 0,
                    "p_cred_done": 0, "p_kyc_done": 0, "p_synced": 0, "p_end": 0
                },
                "final_place": "p_end"
            }
        },
        "violating": {
            "description": "Defective concurrent process. An unauthorized cross-lane bypass allows fast-track approval without performing the Credit Risk Assessment in Lane 2.",
            "bpmn_dot": """
            digraph BPMN_L2_Violating {
                rankdir=LR;
                node [fontname="Helvetica, Arial, sans-serif", fontsize=11];
                edge [fontname="Helvetica, Arial, sans-serif", fontsize=10, color="#334155"];

                start [shape=circle, label="", width=0.35, height=0.35, style=filled, fillcolor="#86EFAC", color="#16A34A", penwidth=2];
                t_recv [shape=rect, style="rounded,filled", fillcolor="#DBEAFE", color="#2563EB", penwidth=1.5, label="Submit Application"];
                and_split [shape=diamond, width=0.45, height=0.45, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.5, label="+", fontsize=18];
                t_credit [shape=rect, style="rounded,filled", fillcolor="#DBEAFE", color="#2563EB", penwidth=1.5, label="Credit Risk Assessment\\n(Mandatory)"];
                t_kyc [shape=rect, style="rounded,filled", fillcolor="#DBEAFE", color="#2563EB", penwidth=1.5, label="KYC Identity Verification\\n(Mandatory)"];
                and_join [shape=diamond, width=0.45, height=0.45, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.5, label="+", fontsize=18];
                xor_dec [shape=diamond, width=0.45, height=0.45, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.5, label="×", fontsize=16];
                t_app [shape=rect, style="rounded,filled", fillcolor="#DCFCE7", color="#16A34A", penwidth=1.5, label="Approve Loan"];
                t_rej [shape=rect, style="rounded,filled", fillcolor="#FEE2E2", color="#DC2626", penwidth=1.5, label="Reject Loan"];
                end_app [shape=doublecircle, label="", width=0.35, height=0.35, style=filled, fillcolor="#FCA5A5", color="#DC2626", penwidth=2];
                end_rej [shape=doublecircle, label="", width=0.35, height=0.35, style=filled, fillcolor="#FCA5A5", color="#DC2626", penwidth=2];

                start -> t_recv;
                t_recv -> and_split;
                and_split -> t_credit [label="Parallel Branch 1"];
                and_split -> t_kyc [label="Parallel Branch 2"];
                t_credit -> and_join;
                t_kyc -> and_join;
                and_join -> xor_dec;
                xor_dec -> t_app [label="Eligible"];
                xor_dec -> t_rej [label="Ineligible"];
                
                # Compliance Violation: Direct bypass around Credit Check
                and_split -> and_join [label="⚠️ Bypass Credit Check (Violation)", color="#DC2626", fontcolor="#DC2626", style=dashed, penwidth=2];

                t_app -> end_app;
                t_rej -> end_rej;
            }
            """,
            "bpmn_swimlane_dot": """
            digraph BPMN_L2_Swimlane_Violating {
                rankdir=LR;
                compound=true;
                newrank=true;
                node [fontname="Helvetica, Arial, sans-serif", fontsize=10];
                edge [fontname="Helvetica, Arial, sans-serif", fontsize=9, color="#334155"];

                # Pool 1: Commercial Borrower Portal (Top Pool)
                subgraph cluster_pool_portal {
                    label = "🏊 Pool: Commercial Borrower Portal";
                    style = "filled,rounded";
                    fillcolor = "#F0FDF4";
                    color = "#16A34A";
                    penwidth = 2.0;
                    fontsize = 12;
                    fontcolor = "#166534";

                    p_start [shape=circle, label="", width=0.32, height=0.32, style=filled, fillcolor="#86EFAC", color="#16A34A", penwidth=2];
                    p_submit [shape=rect, style="rounded,filled", fillcolor="#FFFFFF", color="#16A34A", penwidth=1.5, label="👤 Access Portal &\\nSubmit Commercial Dossier"];
                    p_receive_dec [shape=rect, style="rounded,filled", fillcolor="#FFFFFF", color="#16A34A", penwidth=1.5, label="✉️ Receive Commitment\\nApproval Notice"];
                    p_end [shape=doublecircle, label="", width=0.32, height=0.32, style=filled, fillcolor="#FCA5A5", color="#DC2626", penwidth=2];

                    p_start -> p_submit;
                    p_receive_dec -> p_end;
                }

                # Pool 2: Commercial Loan Provider (Outer box containing internal departmental swimlanes)
                subgraph cluster_pool_provider {
                    label = "🏦 Pool: Commercial Loan Provider (Financial Institution)";
                    style = "filled";
                    fillcolor = "#FFFFFF";
                    color = "#1E3A8A";
                    penwidth = 2.5;
                    fontsize = 13;
                    fontcolor = "#1E3A8A";

                    subgraph cluster_lane_intake {
                        label = "🏊 Lane 1: Loan Origination & Intake Desk";
                        style = "filled,rounded";
                        fillcolor = "#EFF6FF";
                        color = "#3B82F6";
                        penwidth = 1.5;
                        fontsize = 11;
                        fontcolor = "#1D4ED8";

                        t_recv [shape=rect, style="rounded,filled", fillcolor="#FFFFFF", color="#2563EB", penwidth=1.5, label="Initialize Commercial File"];
                        and_split [shape=diamond, width=0.42, height=0.42, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.5, label="+", fontsize=16, tooltip="Parallel Fork (AND-Split)"];
                    }

                    subgraph cluster_lane_risk {
                        label = "🏊 Lane 2: Financial Risk Assessment Dept";
                        style = "filled,rounded";
                        fillcolor = "#FEFCE8";
                        color = "#F59E0B";
                        penwidth = 1.5;
                        fontsize = 11;
                        fontcolor = "#B45309";

                        t_credit [shape=rect, style="rounded,filled", fillcolor="#FFFFFF", color="#2563EB", penwidth=1.5, label="Credit Risk Assessment\\n(Mandatory Prerequisite)"];
                    }

                    subgraph cluster_lane_compliance {
                        label = "🏊 Lane 3: Legal & AML / KYC Compliance Dept";
                        style = "filled,rounded";
                        fillcolor = "#FFF1F2";
                        color = "#F43F5E";
                        penwidth = 1.5;
                        fontsize = 11;
                        fontcolor = "#BE123C";

                        t_kyc [shape=rect, style="rounded,filled", fillcolor="#FFFFFF", color="#2563EB", penwidth=1.5, label="KYC Identity Verification\\n(Mandatory Prerequisite)"];
                    }

                    subgraph cluster_lane_underwriting {
                        label = "🏊 Lane 4: Commercial Underwriting Officer";
                        style = "filled,rounded";
                        fillcolor = "#FAF5FF";
                        color = "#A855F7";
                        penwidth = 1.5;
                        fontsize = 11;
                        fontcolor = "#7E22CE";

                        and_join [shape=diamond, width=0.42, height=0.42, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.5, label="+", fontsize=16, tooltip="Parallel Synchronization (AND-Join)"];
                        xor_dec [shape=diamond, width=0.42, height=0.42, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.5, label="×", fontsize=14, tooltip="Exclusive Decision (XOR)"];
                        t_app [shape=rect, style="rounded,filled", fillcolor="#DCFCE7", color="#16A34A", penwidth=1.5, label="Approve Loan"];
                        t_rej [shape=rect, style="rounded,filled", fillcolor="#FEE2E2", color="#DC2626", penwidth=1.5, label="Reject Loan"];
                        t_notify [shape=rect, style="rounded,filled", fillcolor="#FFFFFF", color="#7E22CE", penwidth=1.5, label="✉️ Send Underwriting\\nCommitment"];
                        end_app [shape=doublecircle, label="", width=0.32, height=0.32, style=filled, fillcolor="#FCA5A5", color="#DC2626", penwidth=2];
                        end_rej [shape=doublecircle, label="", width=0.32, height=0.32, style=filled, fillcolor="#FCA5A5", color="#DC2626", penwidth=2];
                    }

                    # Sequence Flows inside Loan Provider
                    t_recv -> and_split;
                    and_split -> t_credit [label="Concurrent Branch 1"];
                    and_split -> t_kyc [label="Concurrent Branch 2"];
                    t_credit -> and_join [label="Risk Cleared"];
                    t_kyc -> and_join [label="KYC Cleared"];
                    
                    # Cross-Lane Violation Bypass Edge
                    and_split -> and_join [label="⚠️ Skip Lane 2 (Credit Risk)", color="#DC2626", fontcolor="#DC2626", style=dashed, penwidth=2.2];

                    and_join -> xor_dec [label="Decision"];
                    xor_dec -> t_app [label="Eligible"];
                    xor_dec -> t_rej [label="Ineligible"];
                    t_app -> t_notify;
                    t_rej -> t_notify;
                    t_app -> end_app;
                    t_rej -> end_rej;
                }

                # Cross-Pool Message Flows
                p_submit -> t_recv [label="Commercial Dossier", style=dashed, color="#2563EB", penwidth=1.3];
                t_notify -> p_receive_dec [label="Commitment Notice", style=dashed, color="#2563EB", penwidth=1.3];
            }
            """,
            "petri_net": {
                "places": [
                    {"id": "p_start", "label": "p_start (Application Submitted)", "initial_tokens": 1, "lane": "Lane 1: Intake Desk"},
                    {"id": "p_split", "label": "p_split (Ready for Parallel Vetting)", "initial_tokens": 0, "lane": "Lane 1: Intake Desk"},
                    {"id": "p_cred_wait", "label": "p_cred_wait (Awaiting Credit Check)", "initial_tokens": 0, "lane": "Lane 2: Financial Risk Dept"},
                    {"id": "p_kyc_wait", "label": "p_kyc_wait (Awaiting KYC Check)", "initial_tokens": 0, "lane": "Lane 3: Legal & Compliance"},
                    {"id": "p_cred_done", "label": "p_cred_done (Credit Check Finished)", "initial_tokens": 0, "lane": "Lane 2: Financial Risk Dept"},
                    {"id": "p_kyc_done", "label": "p_kyc_done (KYC Finished)", "initial_tokens": 0, "lane": "Lane 3: Legal & Compliance"},
                    {"id": "p_synced", "label": "p_synced (Audits Synchronized)", "initial_tokens": 0, "lane": "Lane 4: Underwriting Officer"},
                    {"id": "p_cred_bypassed", "label": "p_cred_bypassed (Credit Skipped)", "initial_tokens": 0, "lane": "Lane 2: Financial Risk Dept"},
                    {"id": "p_synced_unverified", "label": "p_synced_unverified (Unverified Sync)", "initial_tokens": 0, "lane": "Lane 4: Underwriting Officer"},
                    {"id": "p_end", "label": "p_end (Process Terminated)", "initial_tokens": 0, "lane": "Lane 4: Underwriting Officer"}
                ],
                "transitions": {
                    "t_submit": {
                        "label": "Submit Application",
                        "inputs": ["p_start"],
                        "outputs": ["p_split"],
                        "type": "standard",
                        "lane": "Lane 1: Intake Desk"
                    },
                    "t_and_split": {
                        "label": "AND-Split (Fork)",
                        "inputs": ["p_split"],
                        "outputs": ["p_cred_wait", "p_kyc_wait"],
                        "type": "standard",
                        "lane": "Lane 1: Intake Desk"
                    },
                    "t_credit": {
                        "label": "Credit Risk Assessment",
                        "inputs": ["p_cred_wait"],
                        "outputs": ["p_cred_done"],
                        "type": "prerequisite",
                        "lane": "Lane 2: Financial Risk Dept"
                    },
                    "t_kyc": {
                        "label": "KYC Identity Verification",
                        "inputs": ["p_kyc_wait"],
                        "outputs": ["p_kyc_done"],
                        "type": "prerequisite",
                        "lane": "Lane 3: Legal & Compliance"
                    },
                    "t_and_join": {
                        "label": "AND-Join (Synchronize)",
                        "inputs": ["p_cred_done", "p_kyc_done"],
                        "outputs": ["p_synced"],
                        "type": "standard",
                        "lane": "Lane 4: Underwriting Officer"
                    },
                    "t_app": {
                        "label": "Approve Loan",
                        "inputs": ["p_synced"],
                        "outputs": ["p_end"],
                        "type": "decision",
                        "lane": "Lane 4: Underwriting Officer"
                    },
                    "t_rej": {
                        "label": "Reject Loan",
                        "inputs": ["p_synced"],
                        "outputs": ["p_end"],
                        "type": "decision",
                        "lane": "Lane 4: Underwriting Officer"
                    },
                    "t_skip_cred": {
                        "label": "Bypass Credit Risk Assessment",
                        "inputs": ["p_cred_wait"],
                        "outputs": ["p_cred_bypassed"],
                        "type": "violation",
                        "lane": "Lane 2: Financial Risk Dept"
                    },
                    "t_unverified_join": {
                        "label": "AND-Join (Unverified Bypass)",
                        "inputs": ["p_cred_bypassed", "p_kyc_done"],
                        "outputs": ["p_synced_unverified"],
                        "type": "violation",
                        "lane": "Lane 4: Underwriting Officer"
                    },
                    "t_premature_app": {
                        "label": "Approve Loan (Credit Skipped)",
                        "inputs": ["p_synced_unverified"],
                        "outputs": ["p_end"],
                        "type": "violation",
                        "lane": "Lane 4: Underwriting Officer"
                    }
                },
                "initial_marking": {
                    "p_start": 1, "p_split": 0, "p_cred_wait": 0, "p_kyc_wait": 0,
                    "p_cred_done": 0, "p_kyc_done": 0, "p_synced": 0, "p_cred_bypassed": 0,
                    "p_synced_unverified": 0, "p_end": 0
                },
                "final_place": "p_end"
            }
        }
    },

    "level3": {
        "title": "Level 3: Advanced (Multi-Gateway: Inclusive, Parallel & Exclusive)",
        "domain": "Corporate & Syndicated Commercial Lending",
        "complexity_level": "Level 3: Advanced",
        "complexity_badge": "🔴 Advanced",
        "architecture_summary": "Multi-Gateway Architecture: Parallel AND Fork/Join + Inclusive OR Collateral Vetting + Multi-Tier Exclusive XOR Decisions & Document Rework Loop",
        "concurrency_degree": "Multi-Token Concurrency (AND/OR Gateways) + Cyclic State Space (Rework Loop)",
        "swimlane_roles": [
            "Lane 1: Client & Relationship Manager (Borrower Portal)",
            "Lane 2: Technical & Collateral Audit Group",
            "Lane 3: Branch Credit Committee (Tier 1 Authority)",
            "Lane 4: Senior Credit Committee & Executive Board (Tier 2 Authority)"
        ],
        "rule_text": "All approved loans must have Credit Risk Assessment, and High-Risk/Escalated loans must strictly obtain Senior Credit Committee Review before Committee Approval.",
        "rule_spec": {
            "prerequisite": "Credit Risk Assessment",
            "target": "Approve",
            "escalation_rule": {
                "trigger": "Escalate to Senior Risk Committee",
                "prerequisite": "Senior Committee Review",
                "target": "Committee Approve Loan"
            }
        },
        "description": (
            "An enterprise syndicated loan underwriting pipeline spanning 4 departmental swimlanes, combining all 3 primary BPMN gateway types: "
            "(1) Parallel Gateway (AND-Split): Simultaneously branches into Financial Credit Risk Assessment and Security/Collateral Clearance. "
            "(2) Inclusive Gateway (OR-Split): Evaluates borrower security options—activating Real Estate Asset Appraisal, Corporate Guarantor Audit, "
            "or BOTH concurrently based on loan requirements. The matching Inclusive OR-Join synchronizes whichever security branches were executed. "
            "(3) Parallel Gateway (AND-Join): Synchronizes the Credit Risk and Collateral clearance tracks before underwriting evaluation. "
            "(4) Exclusive Gateways (XOR Decisions): In Lane 3, evaluates loan tier (Low Risk -> Standard Approval, Critical Risk -> Reject, "
            "Incomplete Dossier -> Document Rework Loop back to Lane 1, or High Risk / Jumbo -> Escalation to Lane 4 Senior Committee). "
            "(5) Second Exclusive Gateway (XOR): In Lane 4, convenes Senior Committee Quorum Review before final approval or rejection."
        ),
        "remediation": {
            "violation_title": "Executive Fast-Track Override (Governance Bypass)",
            "root_cause": "An unauthorized fast-track override transition allows high-risk / escalated applications to be approved without convening the Senior Credit Committee Review in Lane 4.",
            "remediation": "Implement Dual-Control / Separation of Duties (SoD) access control. Remove the direct executive override transition and enforce quorum review for escalated loan markings in Lane 4."
        },
        "compliant": {
            "description": "Compliant enterprise multi-gateway model. Simultaneously enforces Parallel AND concurrency, Inclusive OR security vetting, and Exclusive XOR governance with Senior Committee Review.",
            "bpmn_dot": """
            digraph BPMN_L3_Compliant {
                rankdir=LR;
                node [fontname="Helvetica, Arial, sans-serif", fontsize=11];
                edge [fontname="Helvetica, Arial, sans-serif", fontsize=10, color="#334155"];

                start [shape=circle, label="", width=0.35, height=0.35, style=filled, fillcolor="#86EFAC", color="#16A34A", penwidth=2];
                t_recv [shape=rect, style="rounded,filled", fillcolor="#DBEAFE", color="#2563EB", penwidth=1.5, label="Submit Application"];
                
                # 1. Parallel Gateway (AND-Split)
                and_split [shape=diamond, width=0.46, height=0.46, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.8, label="+", fontsize=20, tooltip="Parallel Gateway (AND-Split)"];
                
                # Branch 1: Credit Risk
                t_credit [shape=rect, style="rounded,filled", fillcolor="#DBEAFE", color="#2563EB", penwidth=1.5, label="Credit Risk Assessment\\n(Mandatory Prerequisite)"];
                
                # Branch 2: Inclusive Gateway (OR-Split)
                or_split [shape=diamond, width=0.46, height=0.46, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.8, label="◯", fontsize=16, tooltip="Inclusive Gateway (OR-Split)"];
                t_prop [shape=rect, style="rounded,filled", fillcolor="#DBEAFE", color="#2563EB", penwidth=1.5, label="Real Estate Appraisal\\n(Collateral Track 1)"];
                t_guar [shape=rect, style="rounded,filled", fillcolor="#DBEAFE", color="#2563EB", penwidth=1.5, label="Corporate Guarantor Audit\\n(Collateral Track 2)"];
                or_join [shape=diamond, width=0.46, height=0.46, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.8, label="◯", fontsize=16, tooltip="Inclusive Gateway (OR-Join)"];

                # Parallel Gateway (AND-Join)
                and_join [shape=diamond, width=0.46, height=0.46, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.8, label="+", fontsize=20, tooltip="Parallel Gateway (AND-Join)"];
                
                # Exclusive Gateway (XOR Decision)
                xor_eval [shape=diamond, width=0.46, height=0.46, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.8, label="×", fontsize=16, tooltip="Exclusive Gateway (XOR Decision)"];
                t_low_app [shape=rect, style="rounded,filled", fillcolor="#DCFCE7", color="#16A34A", penwidth=1.5, label="Standard Manager Approval\\n(Low Risk)"];
                t_rej [shape=rect, style="rounded,filled", fillcolor="#FEE2E2", color="#DC2626", penwidth=1.5, label="Reject Loan\\n(Critical Risk)"];
                
                # Document Rework Loop
                t_rework [shape=rect, style="rounded,filled", fillcolor="#FEF3C7", color="#D97706", penwidth=1.5, label="Request Documents\\n(Rework Loop)"];
                t_resubmit [shape=rect, style="rounded,filled", fillcolor="#FEF3C7", color="#D97706", penwidth=1.5, label="Resubmit Documents\\n(Borrower Action)"];

                # Escalation to Senior Committee
                t_escalate [shape=rect, style="rounded,filled", fillcolor="#EDE9FE", color="#7C3AED", penwidth=1.5, label="Escalate to Committee\\n(High Risk / Jumbo)"];
                t_comm_rev [shape=rect, style="rounded,filled", fillcolor="#DBEAFE", color="#2563EB", penwidth=1.5, label="Senior Committee Review\\n(Mandatory Governance)"];
                xor_comm [shape=diamond, width=0.46, height=0.46, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.8, label="×", fontsize=16, tooltip="Exclusive Gateway (XOR Escalation)"];
                t_comm_app [shape=rect, style="rounded,filled", fillcolor="#DCFCE7", color="#16A34A", penwidth=1.5, label="Committee Approve Loan"];
                t_comm_rej [shape=rect, style="rounded,filled", fillcolor="#FEE2E2", color="#DC2626", penwidth=1.5, label="Committee Reject Loan"];

                end_app [shape=doublecircle, label="", width=0.35, height=0.35, style=filled, fillcolor="#FCA5A5", color="#DC2626", penwidth=2];
                end_rej [shape=doublecircle, label="", width=0.35, height=0.35, style=filled, fillcolor="#FCA5A5", color="#DC2626", penwidth=2];

                start -> t_recv;
                t_recv -> and_split [label="Intake Handoff"];
                
                # Parallel Split into Credit and Inclusive Security Tracks
                and_split -> t_credit [label="Parallel 1 (Credit)"];
                and_split -> or_split [label="Parallel 2 (Security)"];

                # Inclusive OR Split: Property, Guarantor, or Both
                or_split -> t_prop [label="Property Collateral"];
                or_split -> t_guar [label="Guarantor Backed"];
                t_prop -> or_join [label="Appraised"];
                t_guar -> or_join [label="Vetted"];

                # Synchronizations
                or_join -> and_join [label="Security Cleared"];
                t_credit -> and_join [label="Credit Cleared"];
                and_join -> xor_eval [label="Audits Synchronized"];

                # Exclusive XOR Choices
                xor_eval -> t_low_app [label="Low Risk"];
                xor_eval -> t_rej [label="Critical Risk"];
                xor_eval -> t_rework [label="Doc Incomplete"];
                t_rework -> t_resubmit [label="Sent to Borrower", style=dashed, color="#D97706"];
                t_resubmit -> xor_eval [label="Re-evaluate", style=dashed, color="#D97706"];

                xor_eval -> t_escalate [label="High Risk / Jumbo"];
                t_escalate -> t_comm_rev [label="Mandatory Escalation"];
                t_comm_rev -> xor_comm;
                xor_comm -> t_comm_app [label="Approved"];
                xor_comm -> t_comm_rej [label="Rejected"];

                t_low_app -> end_app;
                t_comm_app -> end_app;
                t_rej -> end_rej;
                t_comm_rej -> end_rej;
            }
            """,
            "bpmn_swimlane_dot": """
            digraph BPMN_L3_Swimlane_Compliant {
                rankdir=LR;
                compound=true;
                newrank=true;
                node [fontname="Helvetica, Arial, sans-serif", fontsize=10];
                edge [fontname="Helvetica, Arial, sans-serif", fontsize=9, color="#334155"];

                # Pool 1: Customer / Borrower Portal (Top Pool)
                subgraph cluster_pool_portal {
                    label = "🏊 Pool: Customer / Borrower Portal";
                    style = "filled,rounded";
                    fillcolor = "#F0FDF4";
                    color = "#16A34A";
                    penwidth = 2.0;
                    fontsize = 12;
                    fontcolor = "#166534";

                    p_start [shape=circle, label="", width=0.32, height=0.32, style=filled, fillcolor="#86EFAC", color="#16A34A", penwidth=2];
                    p_submit [shape=rect, style="rounded,filled", fillcolor="#FFFFFF", color="#16A34A", penwidth=1.5, label="👤 Access Portal &\\nSubmit Syndicated Request"];
                    p_resubmit [shape=rect, style="rounded,filled", fillcolor="#FEF3C7", color="#D97706", penwidth=1.5, label="📄 Upload Additional\\nRequested Disclosures"];
                    p_receive_dec [shape=rect, style="rounded,filled", fillcolor="#FFFFFF", color="#16A34A", penwidth=1.5, label="✉️ Receive Final\\nCommittee Decision"];
                    p_end [shape=doublecircle, label="", width=0.32, height=0.32, style=filled, fillcolor="#FCA5A5", color="#DC2626", penwidth=2];

                    p_start -> p_submit;
                    p_receive_dec -> p_end;
                }

                # Pool 2: Corporate Loan Provider (Outer box containing internal departmental swimlanes)
                subgraph cluster_pool_provider {
                    label = "🏦 Pool: Corporate Loan Provider (Financial Institution)";
                    style = "filled";
                    fillcolor = "#FFFFFF";
                    color = "#1E3A8A";
                    penwidth = 2.5;
                    fontsize = 13;
                    fontcolor = "#1E3A8A";

                    subgraph cluster_lane_applicant {
                        label = "🏊 Lane 1: Commercial Credit Broker & Intake Desk";
                        style = "filled,rounded";
                        fillcolor = "#EFF6FF";
                        color = "#3B82F6";
                        penwidth = 1.5;
                        fontsize = 11;
                        fontcolor = "#1D4ED8";

                        t_recv [shape=rect, style="rounded,filled", fillcolor="#FFFFFF", color="#2563EB", penwidth=1.5, label="Create Loan Dossier"];
                    }

                    subgraph cluster_lane_audit {
                        label = "🏊 Lane 2: Technical & Collateral Audit Group";
                        style = "filled,rounded";
                        fillcolor = "#FEFCE8";
                        color = "#F59E0B";
                        penwidth = 1.5;
                        fontsize = 11;
                        fontcolor = "#B45309";

                        and_split [shape=diamond, width=0.42, height=0.42, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.5, label="+", fontsize=18, tooltip="Parallel Gateway (AND-Split)"];
                        t_credit [shape=rect, style="rounded,filled", fillcolor="#FFFFFF", color="#2563EB", penwidth=1.5, label="Credit Risk Assessment\\n(Mandatory Prerequisite)"];
                        
                        or_split [shape=diamond, width=0.42, height=0.42, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.5, label="◯", fontsize=15, tooltip="Inclusive Gateway (OR-Split)"];
                        t_prop [shape=rect, style="rounded,filled", fillcolor="#FFFFFF", color="#2563EB", penwidth=1.5, label="Real Estate Appraisal\\n(Collateral Track 1)"];
                        t_guar [shape=rect, style="rounded,filled", fillcolor="#FFFFFF", color="#2563EB", penwidth=1.5, label="Corporate Guarantor Audit\\n(Collateral Track 2)"];
                        or_join [shape=diamond, width=0.42, height=0.42, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.5, label="◯", fontsize=15, tooltip="Inclusive Gateway (OR-Join)"];

                        and_join [shape=diamond, width=0.42, height=0.42, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.5, label="+", fontsize=18, tooltip="Parallel Gateway (AND-Join)"];
                    }

                    subgraph cluster_lane_branch {
                        label = "🏊 Lane 3: Branch Credit Committee (Tier 1 Authority)";
                        style = "filled,rounded";
                        fillcolor = "#FFF1F2";
                        color = "#F43F5E";
                        penwidth = 1.5;
                        fontsize = 11;
                        fontcolor = "#BE123C";

                        xor_eval [shape=diamond, width=0.42, height=0.42, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.5, label="×", fontsize=16, tooltip="Exclusive Gateway (XOR Decision)"];
                        t_low_app [shape=rect, style="rounded,filled", fillcolor="#DCFCE7", color="#16A34A", penwidth=1.5, label="Standard Manager Approval\\n(Low Risk)"];
                        t_rej [shape=rect, style="rounded,filled", fillcolor="#FEE2E2", color="#DC2626", penwidth=1.5, label="Reject Loan\\n(Critical Risk)"];
                        t_rework [shape=rect, style="rounded,filled", fillcolor="#FEF3C7", color="#D97706", penwidth=1.5, label="Request Additional Documents\\n(Trigger Rework Loop)"];
                        t_escalate [shape=rect, style="rounded,filled", fillcolor="#EDE9FE", color="#7C3AED", penwidth=1.5, label="Escalate to Senior Committee\\n(High Risk / Jumbo)"];
                    }

                    subgraph cluster_lane_executive {
                        label = "🏊 Lane 4: Senior Credit Committee & Executive Board (Tier 2 Authority)";
                        style = "filled,rounded";
                        fillcolor = "#FAF5FF";
                        color = "#A855F7";
                        penwidth = 1.5;
                        fontsize = 11;
                        fontcolor = "#7E22CE";

                        t_comm_rev [shape=rect, style="rounded,filled", fillcolor="#FFFFFF", color="#7E22CE", penwidth=1.5, label="Senior Committee Review\\n(Mandatory Governance)"];
                        xor_comm [shape=diamond, width=0.42, height=0.42, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.5, label="×", fontsize=16, tooltip="Exclusive Gateway (XOR Escalation)"];
                        t_comm_app [shape=rect, style="rounded,filled", fillcolor="#DCFCE7", color="#16A34A", penwidth=1.5, label="Committee Approve Loan"];
                        t_comm_rej [shape=rect, style="rounded,filled", fillcolor="#FEE2E2", color="#DC2626", penwidth=1.5, label="Committee Reject Loan"];
                        t_notify [shape=rect, style="rounded,filled", fillcolor="#FFFFFF", color="#7E22CE", penwidth=1.5, label="✉️ Dispatch Decision\\nNotification"];
                        end_app [shape=doublecircle, label="", width=0.32, height=0.32, style=filled, fillcolor="#FCA5A5", color="#DC2626", penwidth=2];
                        end_rej [shape=doublecircle, label="", width=0.32, height=0.32, style=filled, fillcolor="#FCA5A5", color="#DC2626", penwidth=2];
                    }

                    # Lane 1 -> Lane 2 Handoff
                    t_recv -> and_split [label="Intake Handoff"];
                    
                    # Lane 2 Parallel & Inclusive Branching
                    and_split -> t_credit [label="Parallel 1 (Credit)"];
                    and_split -> or_split [label="Parallel 2 (Security)"];
                    or_split -> t_prop [label="Property Collateral"];
                    or_split -> t_guar [label="Guarantor Audit"];
                    t_prop -> or_join [label="Property Cleared"];
                    t_guar -> or_join [label="Guarantor Cleared"];
                    or_join -> and_join [label="Security Cleared"];
                    t_credit -> and_join [label="Credit Cleared"];
                    and_join -> xor_eval [label="Audits Vetted"];

                    # Lane 3 Exclusive Decisions
                    xor_eval -> t_low_app [label="Low Risk"];
                    xor_eval -> t_rej [label="Critical Risk"];

                    # Cross-lane Escalation: Branch Manager -> Senior Committee
                    xor_eval -> t_escalate [label="Jumbo Loan"];
                    t_escalate -> t_comm_rev [label="Escalation Handoff"];
                    t_comm_rev -> xor_comm;
                    xor_comm -> t_comm_app [label="Approved"];
                    xor_comm -> t_comm_rej [label="Rejected"];

                    t_low_app -> t_notify;
                    t_comm_app -> t_notify;
                    t_rej -> t_notify;
                    t_comm_rej -> t_notify;

                    t_low_app -> end_app;
                    t_comm_app -> end_app;
                    t_rej -> end_rej;
                    t_comm_rej -> end_rej;
                }

                # Cross-Pool Message Flows (Dashed lines, matching picture!)
                p_submit -> t_recv [label="Syndicated File", style=dashed, color="#2563EB", penwidth=1.3];
                xor_eval -> t_rework [label="Doc Incomplete"];
                t_rework -> p_resubmit [label="Disclosures Required", style=dashed, color="#D97706", penwidth=1.3];
                p_resubmit -> xor_eval [label="Client Resubmission", style=dashed, color="#D97706", penwidth=1.3];
                t_notify -> p_receive_dec [label="Official Verdict", style=dashed, color="#2563EB", penwidth=1.3];
            }
            """,
            "petri_net": {
                "places": [
                    {"id": "p_start", "label": "p_start (Application Submitted)", "initial_tokens": 1, "lane": "Lane 1: Relationship Manager"},
                    {"id": "p_split", "label": "p_split (Ready for Parallel Vetting)", "initial_tokens": 0, "lane": "Lane 2: Technical Audit Group"},
                    {"id": "p_cred_wait", "label": "p_cred_wait (Awaiting Credit Risk Check)", "initial_tokens": 0, "lane": "Lane 2: Technical Audit Group"},
                    {"id": "p_cred_done", "label": "p_cred_done (Credit Check Finished)", "initial_tokens": 0, "lane": "Lane 2: Technical Audit Group"},
                    {"id": "p_sec_wait", "label": "p_sec_wait (Awaiting Security Evaluation)", "initial_tokens": 0, "lane": "Lane 2: Technical Audit Group"},
                    {"id": "p_prop_wait", "label": "p_prop_wait (Awaiting Property Appraisal)", "initial_tokens": 0, "lane": "Lane 2: Technical Audit Group"},
                    {"id": "p_guar_wait", "label": "p_guar_wait (Awaiting Guarantor Audit)", "initial_tokens": 0, "lane": "Lane 2: Technical Audit Group"},
                    {"id": "p_prop_skip", "label": "p_prop_skip (Property Appraisal Not Required)", "initial_tokens": 0, "lane": "Lane 2: Technical Audit Group"},
                    {"id": "p_guar_skip", "label": "p_guar_skip (Guarantor Audit Not Required)", "initial_tokens": 0, "lane": "Lane 2: Technical Audit Group"},
                    {"id": "p_prop_done", "label": "p_prop_done (Property Appraisal Finished)", "initial_tokens": 0, "lane": "Lane 2: Technical Audit Group"},
                    {"id": "p_guar_done", "label": "p_guar_done (Guarantor Audit Finished)", "initial_tokens": 0, "lane": "Lane 2: Technical Audit Group"},
                    {"id": "p_sec_done", "label": "p_sec_done (Security Clearance Complete)", "initial_tokens": 0, "lane": "Lane 2: Technical Audit Group"},
                    {"id": "p_evaluated", "label": "p_evaluated (Audits Synchronized / Risk Evaluation)", "initial_tokens": 0, "lane": "Lane 3: Branch Committee"},
                    {"id": "p_rework", "label": "p_rework (Additional Documents Requested)", "initial_tokens": 0, "lane": "Lane 1: Relationship Manager"},
                    {"id": "p_escalated", "label": "p_escalated (Escalated to Committee)", "initial_tokens": 0, "lane": "Lane 4: Senior Committee"},
                    {"id": "p_comm_vetted", "label": "p_comm_vetted (Senior Committee Review Completed)", "initial_tokens": 0, "lane": "Lane 4: Senior Committee"},
                    {"id": "p_end", "label": "p_end (Process Terminated)", "initial_tokens": 0, "lane": "Lane 4: Senior Committee"}
                ],
                "transitions": {
                    "t_submit": {
                        "label": "Submit Application",
                        "inputs": ["p_start"],
                        "outputs": ["p_split"],
                        "type": "standard",
                        "lane": "Lane 1: Relationship Manager"
                    },
                    "t_and_split": {
                        "label": "AND-Split (Fork Concurrency)",
                        "inputs": ["p_split"],
                        "outputs": ["p_cred_wait", "p_sec_wait"],
                        "type": "gateway",
                        "lane": "Lane 2: Technical Audit Group"
                    },
                    "t_credit": {
                        "label": "Credit Risk Assessment",
                        "inputs": ["p_cred_wait"],
                        "outputs": ["p_cred_done"],
                        "type": "prerequisite",
                        "lane": "Lane 2: Technical Audit Group"
                    },
                    "t_or_prop": {
                        "label": "OR-Split: Property Collateral Only",
                        "inputs": ["p_sec_wait"],
                        "outputs": ["p_prop_wait", "p_guar_skip"],
                        "type": "gateway",
                        "lane": "Lane 2: Technical Audit Group"
                    },
                    "t_or_guar": {
                        "label": "OR-Split: Corporate Guarantor Only",
                        "inputs": ["p_sec_wait"],
                        "outputs": ["p_guar_wait", "p_prop_skip"],
                        "type": "gateway",
                        "lane": "Lane 2: Technical Audit Group"
                    },
                    "t_or_both": {
                        "label": "OR-Split: Both Collateral & Guarantor",
                        "inputs": ["p_sec_wait"],
                        "outputs": ["p_prop_wait", "p_guar_wait"],
                        "type": "gateway",
                        "lane": "Lane 2: Technical Audit Group"
                    },
                    "t_prop_appraisal": {
                        "label": "Real Estate Asset Appraisal",
                        "inputs": ["p_prop_wait"],
                        "outputs": ["p_prop_done"],
                        "type": "prerequisite",
                        "lane": "Lane 2: Technical Audit Group"
                    },
                    "t_guar_audit": {
                        "label": "Corporate Guarantor Audit",
                        "inputs": ["p_guar_wait"],
                        "outputs": ["p_guar_done"],
                        "type": "prerequisite",
                        "lane": "Lane 2: Technical Audit Group"
                    },
                    "t_or_join_prop": {
                        "label": "OR-Join: Property Synchronized",
                        "inputs": ["p_prop_done", "p_guar_skip"],
                        "outputs": ["p_sec_done"],
                        "type": "gateway",
                        "lane": "Lane 2: Technical Audit Group"
                    },
                    "t_or_join_guar": {
                        "label": "OR-Join: Guarantor Synchronized",
                        "inputs": ["p_guar_done", "p_prop_skip"],
                        "outputs": ["p_sec_done"],
                        "type": "gateway",
                        "lane": "Lane 2: Technical Audit Group"
                    },
                    "t_or_join_both": {
                        "label": "OR-Join: Both Synchronized",
                        "inputs": ["p_prop_done", "p_guar_done"],
                        "outputs": ["p_sec_done"],
                        "type": "gateway",
                        "lane": "Lane 2: Technical Audit Group"
                    },
                    "t_and_join": {
                        "label": "AND-Join (Synchronize Audits)",
                        "inputs": ["p_cred_done", "p_sec_done"],
                        "outputs": ["p_evaluated"],
                        "type": "gateway",
                        "lane": "Lane 2: Technical Audit Group"
                    },
                    "t_low_app": {
                        "label": "Standard Manager Approval",
                        "inputs": ["p_evaluated"],
                        "outputs": ["p_end"],
                        "type": "decision",
                        "lane": "Lane 3: Branch Committee"
                    },
                    "t_direct_rej": {
                        "label": "Reject Loan",
                        "inputs": ["p_evaluated"],
                        "outputs": ["p_end"],
                        "type": "decision",
                        "lane": "Lane 3: Branch Committee"
                    },
                    "t_req_docs": {
                        "label": "Request Additional Documents (Rework)",
                        "inputs": ["p_evaluated"],
                        "outputs": ["p_rework"],
                        "type": "standard",
                        "lane": "Lane 3: Branch Committee"
                    },
                    "t_resubmit": {
                        "label": "Resubmit Updated Documents",
                        "inputs": ["p_rework"],
                        "outputs": ["p_evaluated"],
                        "type": "standard",
                        "lane": "Lane 1: Relationship Manager"
                    },
                    "t_escalate": {
                        "label": "Escalate to Senior Risk Committee",
                        "inputs": ["p_evaluated"],
                        "outputs": ["p_escalated"],
                        "type": "standard",
                        "lane": "Lane 3: Branch Committee"
                    },
                    "t_comm_rev": {
                        "label": "Senior Committee Review",
                        "inputs": ["p_escalated"],
                        "outputs": ["p_comm_vetted"],
                        "type": "prerequisite",
                        "lane": "Lane 4: Senior Committee"
                    },
                    "t_comm_app": {
                        "label": "Committee Approve Loan",
                        "inputs": ["p_comm_vetted"],
                        "outputs": ["p_end"],
                        "type": "decision",
                        "lane": "Lane 4: Senior Committee"
                    },
                    "t_comm_rej": {
                        "label": "Committee Reject Loan",
                        "inputs": ["p_comm_vetted"],
                        "outputs": ["p_end"],
                        "type": "decision",
                        "lane": "Lane 4: Senior Committee"
                    }
                },
                "initial_marking": {
                    "p_start": 1, "p_split": 0, "p_cred_wait": 0, "p_cred_done": 0,
                    "p_sec_wait": 0, "p_prop_wait": 0, "p_guar_wait": 0,
                    "p_prop_skip": 0, "p_guar_skip": 0, "p_prop_done": 0, "p_guar_done": 0,
                    "p_sec_done": 0, "p_evaluated": 0, "p_rework": 0,
                    "p_escalated": 0, "p_comm_vetted": 0, "p_end": 0
                },
                "final_place": "p_end"
            }
        },
        "violating": {
            "description": "Enterprise compliance violation. An unauthorized Executive Fast-Track Override allows approving escalated high-risk loans without convening the Senior Committee Review in Lane 4.",
            "bpmn_dot": """
            digraph BPMN_L3_Violating {
                rankdir=LR;
                node [fontname="Helvetica, Arial, sans-serif", fontsize=11];
                edge [fontname="Helvetica, Arial, sans-serif", fontsize=10, color="#334155"];

                start [shape=circle, label="", width=0.35, height=0.35, style=filled, fillcolor="#86EFAC", color="#16A34A", penwidth=2];
                t_recv [shape=rect, style="rounded,filled", fillcolor="#DBEAFE", color="#2563EB", penwidth=1.5, label="Submit Application"];
                
                # 1. Parallel Gateway (AND-Split)
                and_split [shape=diamond, width=0.46, height=0.46, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.8, label="+", fontsize=20, tooltip="Parallel Gateway (AND-Split)"];
                
                # Branch 1: Credit Risk
                t_credit [shape=rect, style="rounded,filled", fillcolor="#DBEAFE", color="#2563EB", penwidth=1.5, label="Credit Risk Assessment\\n(Mandatory Prerequisite)"];
                
                # Branch 2: Inclusive Gateway (OR-Split)
                or_split [shape=diamond, width=0.46, height=0.46, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.8, label="◯", fontsize=16, tooltip="Inclusive Gateway (OR-Split)"];
                t_prop [shape=rect, style="rounded,filled", fillcolor="#DBEAFE", color="#2563EB", penwidth=1.5, label="Real Estate Appraisal\\n(Collateral Track 1)"];
                t_guar [shape=rect, style="rounded,filled", fillcolor="#DBEAFE", color="#2563EB", penwidth=1.5, label="Corporate Guarantor Audit\\n(Collateral Track 2)"];
                or_join [shape=diamond, width=0.46, height=0.46, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.8, label="◯", fontsize=16, tooltip="Inclusive Gateway (OR-Join)"];

                # Parallel Gateway (AND-Join)
                and_join [shape=diamond, width=0.46, height=0.46, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.8, label="+", fontsize=20, tooltip="Parallel Gateway (AND-Join)"];
                
                # Exclusive Gateway (XOR Decision)
                xor_eval [shape=diamond, width=0.46, height=0.46, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.8, label="×", fontsize=16, tooltip="Exclusive Gateway (XOR Decision)"];
                t_low_app [shape=rect, style="rounded,filled", fillcolor="#DCFCE7", color="#16A34A", penwidth=1.5, label="Standard Manager Approval\\n(Low Risk)"];
                t_rej [shape=rect, style="rounded,filled", fillcolor="#FEE2E2", color="#DC2626", penwidth=1.5, label="Reject Loan\\n(Critical Risk)"];
                
                # Document Rework Loop
                t_rework [shape=rect, style="rounded,filled", fillcolor="#FEF3C7", color="#D97706", penwidth=1.5, label="Request Documents\\n(Rework Loop)"];
                t_resubmit [shape=rect, style="rounded,filled", fillcolor="#FEF3C7", color="#D97706", penwidth=1.5, label="Resubmit Documents\\n(Borrower Action)"];

                # Escalation
                t_escalate [shape=rect, style="rounded,filled", fillcolor="#EDE9FE", color="#7C3AED", penwidth=1.5, label="Escalate to Committee\\n(High Risk / Jumbo)"];
                t_comm_rev [shape=rect, style="rounded,filled", fillcolor="#DBEAFE", color="#2563EB", penwidth=1.5, label="Senior Committee Review\\n(Mandatory Governance)"];
                xor_comm [shape=diamond, width=0.46, height=0.46, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.8, label="×", fontsize=16, tooltip="Exclusive Gateway (XOR Escalation)"];
                t_comm_app [shape=rect, style="rounded,filled", fillcolor="#DCFCE7", color="#16A34A", penwidth=1.5, label="Committee Approve Loan"];
                t_comm_rej [shape=rect, style="rounded,filled", fillcolor="#FEE2E2", color="#DC2626", penwidth=1.5, label="Committee Reject Loan"];

                end_app [shape=doublecircle, label="", width=0.35, height=0.35, style=filled, fillcolor="#FCA5A5", color="#DC2626", penwidth=2];
                end_rej [shape=doublecircle, label="", width=0.35, height=0.35, style=filled, fillcolor="#FCA5A5", color="#DC2626", penwidth=2];

                start -> t_recv;
                t_recv -> and_split [label="Intake Handoff"];
                
                # Parallel Split
                and_split -> t_credit [label="Parallel 1 (Credit)"];
                and_split -> or_split [label="Parallel 2 (Security)"];

                # Inclusive OR Split
                or_split -> t_prop [label="Property Collateral"];
                or_split -> t_guar [label="Guarantor Backed"];
                t_prop -> or_join [label="Appraised"];
                t_guar -> or_join [label="Vetted"];

                # Synchronizations
                or_join -> and_join [label="Security Cleared"];
                t_credit -> and_join [label="Credit Cleared"];
                and_join -> xor_eval [label="Audits Synchronized"];

                # Exclusive XOR Choices
                xor_eval -> t_low_app [label="Low Risk"];
                xor_eval -> t_rej [label="Critical Risk"];
                xor_eval -> t_rework [label="Doc Incomplete"];
                t_rework -> t_resubmit [label="Sent to Borrower"];
                t_resubmit -> xor_eval [label="Re-evaluate", style=dashed, color="#D97706"];

                xor_eval -> t_escalate [label="High Risk / Jumbo"];
                t_escalate -> t_comm_rev [label="Mandatory Escalation"];
                t_comm_rev -> xor_comm;
                xor_comm -> t_comm_app [label="Approved"];
                xor_comm -> t_comm_rej [label="Rejected"];

                # Compliance Violation: Unauthorized Executive Fast-Track Override
                t_escalate -> t_comm_app [label="⚠️ Executive Fast-Track Override (Skip Committee Review)", color="#DC2626", fontcolor="#DC2626", style=dashed, penwidth=2];

                t_low_app -> end_app;
                t_comm_app -> end_app;
                t_rej -> end_rej;
                t_comm_rej -> end_rej;
            }
            """,
            "bpmn_swimlane_dot": """
            digraph BPMN_L3_Swimlane_Violating {
                rankdir=LR;
                compound=true;
                newrank=true;
                node [fontname="Helvetica, Arial, sans-serif", fontsize=10];
                edge [fontname="Helvetica, Arial, sans-serif", fontsize=9, color="#334155"];

                # Pool 1: Customer / Borrower Portal (Top Pool)
                subgraph cluster_pool_portal {
                    label = "🏊 Pool: Customer / Borrower Portal";
                    style = "filled,rounded";
                    fillcolor = "#F0FDF4";
                    color = "#16A34A";
                    penwidth = 2.0;
                    fontsize = 12;
                    fontcolor = "#166534";

                    p_start [shape=circle, label="", width=0.32, height=0.32, style=filled, fillcolor="#86EFAC", color="#16A34A", penwidth=2];
                    p_submit [shape=rect, style="rounded,filled", fillcolor="#FFFFFF", color="#16A34A", penwidth=1.5, label="👤 Access Portal &\\nSubmit Syndicated Request"];
                    p_resubmit [shape=rect, style="rounded,filled", fillcolor="#FEF3C7", color="#D97706", penwidth=1.5, label="📄 Upload Additional\\nRequested Disclosures"];
                    p_receive_dec [shape=rect, style="rounded,filled", fillcolor="#FFFFFF", color="#16A34A", penwidth=1.5, label="✉️ Receive Final\\nCommittee Decision"];
                    p_end [shape=doublecircle, label="", width=0.32, height=0.32, style=filled, fillcolor="#FCA5A5", color="#DC2626", penwidth=2];

                    p_start -> p_submit;
                    p_receive_dec -> p_end;
                }

                # Pool 2: Corporate Loan Provider (Outer box containing internal departmental swimlanes)
                subgraph cluster_pool_provider {
                    label = "🏦 Pool: Corporate Loan Provider (Financial Institution)";
                    style = "filled";
                    fillcolor = "#FFFFFF";
                    color = "#1E3A8A";
                    penwidth = 2.5;
                    fontsize = 13;
                    fontcolor = "#1E3A8A";

                    subgraph cluster_lane_applicant {
                        label = "🏊 Lane 1: Commercial Credit Broker & Intake Desk";
                        style = "filled,rounded";
                        fillcolor = "#EFF6FF";
                        color = "#3B82F6";
                        penwidth = 1.5;
                        fontsize = 11;
                        fontcolor = "#1D4ED8";

                        t_recv [shape=rect, style="rounded,filled", fillcolor="#FFFFFF", color="#2563EB", penwidth=1.5, label="Create Loan Dossier"];
                    }

                    subgraph cluster_lane_audit {
                        label = "🏊 Lane 2: Technical & Collateral Audit Group";
                        style = "filled,rounded";
                        fillcolor = "#FEFCE8";
                        color = "#F59E0B";
                        penwidth = 1.5;
                        fontsize = 11;
                        fontcolor = "#B45309";

                        and_split [shape=diamond, width=0.42, height=0.42, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.5, label="+", fontsize=18, tooltip="Parallel Gateway (AND-Split)"];
                        t_credit [shape=rect, style="rounded,filled", fillcolor="#FFFFFF", color="#2563EB", penwidth=1.5, label="Credit Risk Assessment\\n(Mandatory Prerequisite)"];
                        
                        or_split [shape=diamond, width=0.42, height=0.42, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.5, label="◯", fontsize=15, tooltip="Inclusive Gateway (OR-Split)"];
                        t_prop [shape=rect, style="rounded,filled", fillcolor="#FFFFFF", color="#2563EB", penwidth=1.5, label="Real Estate Appraisal\\n(Collateral Track 1)"];
                        t_guar [shape=rect, style="rounded,filled", fillcolor="#FFFFFF", color="#2563EB", penwidth=1.5, label="Corporate Guarantor Audit\\n(Collateral Track 2)"];
                        or_join [shape=diamond, width=0.42, height=0.42, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.5, label="◯", fontsize=15, tooltip="Inclusive Gateway (OR-Join)"];

                        and_join [shape=diamond, width=0.42, height=0.42, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.5, label="+", fontsize=18, tooltip="Parallel Gateway (AND-Join)"];
                    }

                    subgraph cluster_lane_branch {
                        label = "🏊 Lane 3: Branch Credit Committee (Tier 1 Authority)";
                        style = "filled,rounded";
                        fillcolor = "#FFF1F2";
                        color = "#F43F5E";
                        penwidth = 1.5;
                        fontsize = 11;
                        fontcolor = "#BE123C";

                        xor_eval [shape=diamond, width=0.42, height=0.42, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.5, label="×", fontsize=16, tooltip="Exclusive Gateway (XOR Decision)"];
                        t_low_app [shape=rect, style="rounded,filled", fillcolor="#DCFCE7", color="#16A34A", penwidth=1.5, label="Standard Manager Approval\\n(Low Risk)"];
                        t_rej [shape=rect, style="rounded,filled", fillcolor="#FEE2E2", color="#DC2626", penwidth=1.5, label="Reject Loan\\n(Critical Risk)"];
                        t_rework [shape=rect, style="rounded,filled", fillcolor="#FEF3C7", color="#D97706", penwidth=1.5, label="Request Additional Documents\\n(Trigger Rework Loop)"];
                        t_escalate [shape=rect, style="rounded,filled", fillcolor="#EDE9FE", color="#7C3AED", penwidth=1.5, label="Escalate to Committee\\n(High Risk / Jumbo)"];
                    }

                    subgraph cluster_lane_executive {
                        label = "🏊 Lane 4: Senior Credit Committee & Executive Board (Tier 2 Authority)";
                        style = "filled,rounded";
                        fillcolor = "#FAF5FF";
                        color = "#A855F7";
                        penwidth = 1.5;
                        fontsize = 11;
                        fontcolor = "#7E22CE";

                        t_comm_rev [shape=rect, style="rounded,filled", fillcolor="#FFFFFF", color="#7E22CE", penwidth=1.5, label="Senior Committee Review\\n(Mandatory Governance)"];
                        xor_comm [shape=diamond, width=0.42, height=0.42, style=filled, fillcolor="#FEF3C7", color="#D97706", penwidth=1.5, label="×", fontsize=16, tooltip="Exclusive Gateway (XOR Escalation)"];
                        t_comm_app [shape=rect, style="rounded,filled", fillcolor="#DCFCE7", color="#16A34A", penwidth=1.5, label="Committee Approve Loan"];
                        t_comm_rej [shape=rect, style="rounded,filled", fillcolor="#FEE2E2", color="#DC2626", penwidth=1.5, label="Committee Reject Loan"];
                        t_notify [shape=rect, style="rounded,filled", fillcolor="#FFFFFF", color="#7E22CE", penwidth=1.5, label="✉️ Dispatch Decision\\nNotification"];
                        end_app [shape=doublecircle, label="", width=0.32, height=0.32, style=filled, fillcolor="#FCA5A5", color="#DC2626", penwidth=2];
                        end_rej [shape=doublecircle, label="", width=0.32, height=0.32, style=filled, fillcolor="#FCA5A5", color="#DC2626", penwidth=2];
                    }

                    # Lane 1 -> Lane 2 Handoff
                    t_recv -> and_split [label="Intake Handoff"];
                    
                    # Lane 2 Parallel & Inclusive Branching
                    and_split -> t_credit [label="Parallel 1 (Credit)"];
                    and_split -> or_split [label="Parallel 2 (Security)"];
                    or_split -> t_prop [label="Property Collateral"];
                    or_split -> t_guar [label="Guarantor Audit"];
                    t_prop -> or_join [label="Property Cleared"];
                    t_guar -> or_join [label="Guarantor Cleared"];
                    or_join -> and_join [label="Security Cleared"];
                    t_credit -> and_join [label="Credit Cleared"];
                    and_join -> xor_eval [label="Audits Vetted"];

                    # Lane 3 Exclusive Decisions
                    xor_eval -> t_low_app [label="Low Risk"];
                    xor_eval -> t_rej [label="Critical Risk"];

                    # Escalation
                    xor_eval -> t_escalate [label="Jumbo Loan"];
                    t_escalate -> t_comm_rev [label="Mandatory Path"];
                    t_comm_rev -> xor_comm;
                    xor_comm -> t_comm_app [label="Approved"];
                    xor_comm -> t_comm_rej [label="Rejected"];

                    # Unauthorized Executive Fast-Track Override
                    t_escalate -> t_comm_app [label="⚠️ Executive Fast-Track Override (Skip Committee Review)", color="#DC2626", fontcolor="#DC2626", style=dashed, penwidth=2.2];

                    t_low_app -> t_notify;
                    t_comm_app -> t_notify;
                    t_rej -> t_notify;
                    t_comm_rej -> t_notify;

                    t_low_app -> end_app;
                    t_comm_app -> end_app;
                    t_rej -> end_rej;
                    t_comm_rej -> end_rej;
                }

                # Cross-Pool Message Flows
                p_submit -> t_recv [label="Syndicated File", style=dashed, color="#2563EB", penwidth=1.3];
                xor_eval -> t_rework [label="Doc Incomplete"];
                t_rework -> p_resubmit [label="Disclosures Required", style=dashed, color="#D97706", penwidth=1.3];
                p_resubmit -> xor_eval [label="Client Resubmission", style=dashed, color="#D97706", penwidth=1.3];
                t_notify -> p_receive_dec [label="Official Verdict", style=dashed, color="#2563EB", penwidth=1.3];
            }
            """,
            "petri_net": {
                "places": [
                    {"id": "p_start", "label": "p_start (Application Submitted)", "initial_tokens": 1, "lane": "Lane 1: Relationship Manager"},
                    {"id": "p_split", "label": "p_split (Ready for Parallel Vetting)", "initial_tokens": 0, "lane": "Lane 2: Technical Audit Group"},
                    {"id": "p_cred_wait", "label": "p_cred_wait (Awaiting Credit Risk Check)", "initial_tokens": 0, "lane": "Lane 2: Technical Audit Group"},
                    {"id": "p_cred_done", "label": "p_cred_done (Credit Check Finished)", "initial_tokens": 0, "lane": "Lane 2: Technical Audit Group"},
                    {"id": "p_sec_wait", "label": "p_sec_wait (Awaiting Security Evaluation)", "initial_tokens": 0, "lane": "Lane 2: Technical Audit Group"},
                    {"id": "p_prop_wait", "label": "p_prop_wait (Awaiting Property Appraisal)", "initial_tokens": 0, "lane": "Lane 2: Technical Audit Group"},
                    {"id": "p_guar_wait", "label": "p_guar_wait (Awaiting Guarantor Audit)", "initial_tokens": 0, "lane": "Lane 2: Technical Audit Group"},
                    {"id": "p_prop_skip", "label": "p_prop_skip (Property Appraisal Not Required)", "initial_tokens": 0, "lane": "Lane 2: Technical Audit Group"},
                    {"id": "p_guar_skip", "label": "p_guar_skip (Guarantor Audit Not Required)", "initial_tokens": 0, "lane": "Lane 2: Technical Audit Group"},
                    {"id": "p_prop_done", "label": "p_prop_done (Property Appraisal Finished)", "initial_tokens": 0, "lane": "Lane 2: Technical Audit Group"},
                    {"id": "p_guar_done", "label": "p_guar_done (Guarantor Audit Finished)", "initial_tokens": 0, "lane": "Lane 2: Technical Audit Group"},
                    {"id": "p_sec_done", "label": "p_sec_done (Security Clearance Complete)", "initial_tokens": 0, "lane": "Lane 2: Technical Audit Group"},
                    {"id": "p_evaluated", "label": "p_evaluated (Audits Synchronized / Risk Evaluation)", "initial_tokens": 0, "lane": "Lane 3: Branch Committee"},
                    {"id": "p_rework", "label": "p_rework (Additional Documents Requested)", "initial_tokens": 0, "lane": "Lane 1: Relationship Manager"},
                    {"id": "p_escalated", "label": "p_escalated (Escalated to Committee)", "initial_tokens": 0, "lane": "Lane 4: Senior Committee"},
                    {"id": "p_comm_vetted", "label": "p_comm_vetted (Senior Committee Review Completed)", "initial_tokens": 0, "lane": "Lane 4: Senior Committee"},
                    {"id": "p_comm_bypassed", "label": "p_comm_bypassed (Committee Review Skipped)", "initial_tokens": 0, "lane": "Lane 4: Senior Committee"},
                    {"id": "p_end", "label": "p_end (Process Terminated)", "initial_tokens": 0, "lane": "Lane 4: Senior Committee"}
                ],
                "transitions": {
                    "t_submit": {
                        "label": "Submit Application",
                        "inputs": ["p_start"],
                        "outputs": ["p_split"],
                        "type": "standard",
                        "lane": "Lane 1: Relationship Manager"
                    },
                    "t_and_split": {
                        "label": "AND-Split (Fork Concurrency)",
                        "inputs": ["p_split"],
                        "outputs": ["p_cred_wait", "p_sec_wait"],
                        "type": "gateway",
                        "lane": "Lane 2: Technical Audit Group"
                    },
                    "t_credit": {
                        "label": "Credit Risk Assessment",
                        "inputs": ["p_cred_wait"],
                        "outputs": ["p_cred_done"],
                        "type": "prerequisite",
                        "lane": "Lane 2: Technical Audit Group"
                    },
                    "t_or_prop": {
                        "label": "OR-Split: Property Collateral Only",
                        "inputs": ["p_sec_wait"],
                        "outputs": ["p_prop_wait", "p_guar_skip"],
                        "type": "gateway",
                        "lane": "Lane 2: Technical Audit Group"
                    },
                    "t_or_guar": {
                        "label": "OR-Split: Corporate Guarantor Only",
                        "inputs": ["p_sec_wait"],
                        "outputs": ["p_guar_wait", "p_prop_skip"],
                        "type": "gateway",
                        "lane": "Lane 2: Technical Audit Group"
                    },
                    "t_or_both": {
                        "label": "OR-Split: Both Collateral & Guarantor",
                        "inputs": ["p_sec_wait"],
                        "outputs": ["p_prop_wait", "p_guar_wait"],
                        "type": "gateway",
                        "lane": "Lane 2: Technical Audit Group"
                    },
                    "t_prop_appraisal": {
                        "label": "Real Estate Asset Appraisal",
                        "inputs": ["p_prop_wait"],
                        "outputs": ["p_prop_done"],
                        "type": "prerequisite",
                        "lane": "Lane 2: Technical Audit Group"
                    },
                    "t_guar_audit": {
                        "label": "Corporate Guarantor Audit",
                        "inputs": ["p_guar_wait"],
                        "outputs": ["p_guar_done"],
                        "type": "prerequisite",
                        "lane": "Lane 2: Technical Audit Group"
                    },
                    "t_or_join_prop": {
                        "label": "OR-Join: Property Synchronized",
                        "inputs": ["p_prop_done", "p_guar_skip"],
                        "outputs": ["p_sec_done"],
                        "type": "gateway",
                        "lane": "Lane 2: Technical Audit Group"
                    },
                    "t_or_join_guar": {
                        "label": "OR-Join: Guarantor Synchronized",
                        "inputs": ["p_guar_done", "p_prop_skip"],
                        "outputs": ["p_sec_done"],
                        "type": "gateway",
                        "lane": "Lane 2: Technical Audit Group"
                    },
                    "t_or_join_both": {
                        "label": "OR-Join: Both Synchronized",
                        "inputs": ["p_prop_done", "p_guar_done"],
                        "outputs": ["p_sec_done"],
                        "type": "gateway",
                        "lane": "Lane 2: Technical Audit Group"
                    },
                    "t_and_join": {
                        "label": "AND-Join (Synchronize Audits)",
                        "inputs": ["p_cred_done", "p_sec_done"],
                        "outputs": ["p_evaluated"],
                        "type": "gateway",
                        "lane": "Lane 2: Technical Audit Group"
                    },
                    "t_low_app": {
                        "label": "Standard Manager Approval",
                        "inputs": ["p_evaluated"],
                        "outputs": ["p_end"],
                        "type": "decision",
                        "lane": "Lane 3: Branch Committee"
                    },
                    "t_direct_rej": {
                        "label": "Reject Loan",
                        "inputs": ["p_evaluated"],
                        "outputs": ["p_end"],
                        "type": "decision",
                        "lane": "Lane 3: Branch Committee"
                    },
                    "t_req_docs": {
                        "label": "Request Additional Documents (Rework)",
                        "inputs": ["p_evaluated"],
                        "outputs": ["p_rework"],
                        "type": "standard",
                        "lane": "Lane 3: Branch Committee"
                    },
                    "t_resubmit": {
                        "label": "Resubmit Updated Documents",
                        "inputs": ["p_rework"],
                        "outputs": ["p_evaluated"],
                        "type": "standard",
                        "lane": "Lane 1: Relationship Manager"
                    },
                    "t_escalate": {
                        "label": "Escalate to Senior Risk Committee",
                        "inputs": ["p_evaluated"],
                        "outputs": ["p_escalated"],
                        "type": "standard",
                        "lane": "Lane 3: Branch Committee"
                    },
                    "t_comm_rev": {
                        "label": "Senior Committee Review",
                        "inputs": ["p_escalated"],
                        "outputs": ["p_comm_vetted"],
                        "type": "prerequisite",
                        "lane": "Lane 4: Senior Committee"
                    },
                    "t_comm_app": {
                        "label": "Committee Approve Loan",
                        "inputs": ["p_comm_vetted"],
                        "outputs": ["p_end"],
                        "type": "decision",
                        "lane": "Lane 4: Senior Committee"
                    },
                    "t_comm_rej": {
                        "label": "Committee Reject Loan",
                        "inputs": ["p_comm_vetted"],
                        "outputs": ["p_end"],
                        "type": "decision",
                        "lane": "Lane 4: Senior Committee"
                    },
                    "t_comm_bypass": {
                        "label": "Executive Fast-Track Override (Skip Committee Review)",
                        "inputs": ["p_escalated"],
                        "outputs": ["p_comm_bypassed"],
                        "type": "violation",
                        "lane": "Lane 4: Senior Committee"
                    },
                    "t_unreviewed_app": {
                        "label": "Committee Approve Loan (Unreviewed)",
                        "inputs": ["p_comm_bypassed"],
                        "outputs": ["p_end"],
                        "type": "violation",
                        "lane": "Lane 4: Senior Committee"
                    }
                },
                "initial_marking": {
                    "p_start": 1, "p_split": 0, "p_cred_wait": 0, "p_cred_done": 0,
                    "p_sec_wait": 0, "p_prop_wait": 0, "p_guar_wait": 0,
                    "p_prop_skip": 0, "p_guar_skip": 0, "p_prop_done": 0, "p_guar_done": 0,
                    "p_sec_done": 0, "p_evaluated": 0, "p_rework": 0,
                    "p_escalated": 0, "p_comm_vetted": 0, "p_comm_bypassed": 0, "p_end": 0
                },
                "final_place": "p_end"
            }
        }
    }
}

if __name__ == "__main__":
    print(f"Catalog loaded successfully. Total complexity levels: {len(COMPLEXITY_CATALOG)}")
    for k, v in COMPLEXITY_CATALOG.items():
        print(f" - {k}: {v['title']} ({v['complexity_badge']}) with {len(v['swimlane_roles'])} swimlanes")
