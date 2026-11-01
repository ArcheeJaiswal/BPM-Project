"""
========================================================================================
Formal Compliance Verification Engine
========================================================================================
Evaluates regulatory compliance constraints over execution traces:
  1. Target Check: If target approval activity is absent (e.g. rejection), no violation.
  2. Prerequisite Precedence Constraint:
     Mandatory prerequisite(s) must be executed BEFORE the target approval activity:
     forall p in Prerequisites, p in trace AND index(p) < index(Target)
  3. Escalation Quorum Governance:
     If a high-risk / escalated state is triggered, senior committee review must strictly
     precede committee approval (no unauthorized fast-track executive override).
========================================================================================
"""

from typing import List, Tuple, Dict, Any, Union


def verify_path_compliance(path_tuples: List[Tuple[str, str, str]], rule_spec: Dict[str, Any]) -> Dict[str, Any]:
    """
    Verifies formal regulatory compliance constraints for a single execution path.

    Parameters:
        path_tuples (list): List of (transition_id, label, transition_type) tuples.
        rule_spec (dict): Compliance rule specification containing:
            - 'prerequisite': str or List[str] of mandatory audit activities.
            - 'target': str identifying target approval activity.
            - 'escalation_rule' (optional): Hierarchical escalation constraint dict.

    Returns:
        dict: Evaluation dictionary with keys:
            - 'compliant': bool (True for PASS, False for VIOLATION)
            - 'status': 'COMPLIANT' | 'VIOLATION'
            - 'reason': str explanation of the finding
    """
    labels = [t[1] for t in path_tuples]
    target = rule_spec["target"]
    has_target = any(target in label for label in labels)

    if not has_target:
        return {
            "compliant": True,
            "status": "COMPLIANT",
            "reason": f"Decision was Rejection. Target '{target}' was not executed, so no approval violation occurred."
        }

    prereqs = rule_spec["prerequisite"]
    if isinstance(prereqs, str):
        prereqs = [prereqs]

    first_target_idx = [i for i, label in enumerate(labels) if target in label][0]

    for p in prereqs:
        matching = [
            i for i, label in enumerate(labels)
            if (label == p or label.startswith(p)) and not ("Bypass" in label or "Skip" in label)
        ]
        if not matching:
            return {
                "compliant": False,
                "status": "VIOLATION",
                "reason": f"Mandatory prerequisite '{p}' was skipped or bypassed before approval!"
            }
        if matching[0] > first_target_idx:
            return {
                "compliant": False,
                "status": "VIOLATION",
                "reason": f"Ordering violation: '{p}' was performed after approval!"
            }

    # Escalation Rule Check (e.g., Senior Risk Committee for Level 3)
    if "escalation_rule" in rule_spec:
        esc = rule_spec["escalation_rule"]
        if any(esc["trigger"] in label for label in labels):
            has_esc_target = any(esc["target"] in label for label in labels)
            if has_esc_target:
                esc_target_idx = [i for i, label in enumerate(labels) if esc["target"] in label][0]
                esc_prereq_matches = [
                    i for i, label in enumerate(labels)
                    if (label == esc["prerequisite"] or label.startswith(esc["prerequisite"]))
                    and not ("Bypass" in label or "Skip" in label or "Override" in label)
                ]
                if not esc_prereq_matches:
                    return {
                        "compliant": False,
                        "status": "VIOLATION",
                        "reason": f"Mandatory escalation requirement '{esc['prerequisite']}' was bypassed (Unauthorized Executive Fast-Track Override)!"
                    }
                if esc_prereq_matches[0] > esc_target_idx:
                    return {
                        "compliant": False,
                        "status": "VIOLATION",
                        "reason": f"Ordering violation: '{esc['prerequisite']}' occurred after '{esc['target']}'!"
                    }

    prereq_str = ", ".join(prereqs)
    return {
        "compliant": True,
        "status": "COMPLIANT",
        "reason": f"All required prerequisite checks ({prereq_str}) completed before approval."
    }


if __name__ == "__main__":
    print("Testing Formal Compliance Verifier...")
    r_single = {"prerequisite": "Credit Check", "target": "Approve Loan"}
    p_pass = [("t1", "Submit Application", "standard"), ("t2", "Credit Check", "prerequisite"), ("t3", "Approve Loan", "decision")]
    p_fail = [("t1", "Submit Application", "standard"), ("t2", "Bypass Credit Check", "violation"), ("t3", "Approve Loan (Unchecked)", "violation")]

    res_pass = verify_path_compliance(p_pass, r_single)
    assert res_pass["compliant"], f"Expected pass, got: {res_pass}"

    res_fail = verify_path_compliance(p_fail, r_single)
    assert not res_fail["compliant"], f"Expected fail, got: {res_fail}"

    print("✅ Compliance verifier unit test passed successfully.")

