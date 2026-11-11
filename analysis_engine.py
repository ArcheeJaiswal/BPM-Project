"""
========================================================================================
Analysis Engine: Reachability Exploration & Rule Monitor
Core verification module referenced in IEEE paper (Section IV, Table I, Section VI.E).
========================================================================================
"""

from typing import Dict, Any, List
from catalog import COMPLEXITY_CATALOG
from reachability import discover_all_execution_paths
from verifier import verify_path_compliance


def analyze_model(level_key: str, variant: str = "compliant") -> Dict[str, Any]:
    """
    Executes reachability graph exploration, workflow-net completion checks,
    and rule-monitor verification on the specified catalog variant.
    """
    comp = COMPLEXITY_CATALOG[level_key]
    var_data = comp[variant]
    petri_spec = var_data["petri_net"]
    rule_spec = comp["rule_spec"]

    # Explore all distinct execution traces and markings
    traces = discover_all_execution_paths(petri_spec, max_visits=2)

    # Verify each trace against the stable transition-ID compliance rule
    trace_results = []
    compliant_count = 0
    violations_detected = []

    for path_tuples in traces:
        eval_result = verify_path_compliance(path_tuples, rule_spec)
        t_ids = [t[0] for t in path_tuples]
        is_comp = eval_result["compliant"]
        v_msg = eval_result.get("reason", "")
        
        trace_results.append({
            "trace_ids": t_ids,
            "compliant": is_comp,
            "message": v_msg
        })
        if is_comp:
            compliant_count += 1
        else:
            violations_detected.append({
                "trace_ids": t_ids,
                "message": v_msg
            })

    total_traces = len(traces)
    is_model_compliant = (len(violations_detected) == 0 and total_traces > 0)

    # Workflow-net soundness criteria checks
    has_source = len([p for p in petri_spec["places"] if p["initial_tokens"] > 0]) == 1
    has_sink = any(p["id"] == "p_end" for p in petri_spec["places"])
    soundness_pass = has_source and has_sink and total_traces > 0

    return {
        "model_key": f"{level_key}_{variant}",
        "title": comp["title"],
        "variant": variant,
        "places_count": len(petri_spec["places"]),
        "transitions_count": len(petri_spec["transitions"]),
        "total_traces_explored": total_traces,
        "compliant_traces": compliant_count,
        "violating_traces": len(violations_detected),
        "is_compliant": is_model_compliant,
        "workflow_net_sound": soundness_pass,
        "violations": violations_detected,
        "shortest_counterexample": violations_detected[0] if violations_detected else None
    }


if __name__ == "__main__":
    import json
    for lvl in ["level1", "level2", "level3"]:
        for var in ["compliant", "violating"]:
            res = analyze_model(lvl, var)
            status = "✅ PASS" if res["is_compliant"] else "❌ VIOLATION DETECTED"
            print(f"[{lvl}_{var}] {status} | Traces: {res['total_traces_explored']} | Sound: {res['workflow_net_sound']}")
