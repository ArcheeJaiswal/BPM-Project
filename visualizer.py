"""
========================================================================================
Graphviz Petri Net Diagram Generator
========================================================================================
Dynamically renders Graphviz DOT specifications for Petri Nets:
  - Standard Layout: Unified, compact workflow net layout.
  - Swimlane Departmental Partition: Automatically clusters places and transitions
    into visually distinct organizational swimlane boxes (subgraph cluster).
  - Places: Circles labeled with ID and live token markings (e.g. [ ● 1 token ]).
    Final sink place is displayed as a doublecircle.
  - Transitions: Filled rectangular boxes color-coded by semantic role:
      * Standard activities: Slate Grey (#475569)
      * Mandatory Prerequisite: Royal Blue (#2563EB)
      * Approval Decision: Forest Green (#059669)
      * Rejection Decision: Red (#DC2626)
      * Compliance Violation / Bypass: Crimson Red (#EF4444)
  - Arcs: Directed arrows representing Input arcs (Place -> Transition)
    and Output arcs (Transition -> Place).
========================================================================================
"""

from typing import Dict, Any, Optional


def generate_petri_net_dot(petri_net: Dict[str, Any], current_marking: Optional[Dict[str, int]] = None, use_swimlanes: bool = False) -> str:
    """
    Generates a clean Graphviz DOT diagram string reflecting the current Petri Net state.

    Parameters:
        petri_net (dict): Petri net specification with 'places', 'transitions',
            and 'final_place'.
        current_marking (dict, optional): Current token distribution mapping place IDs
            to token counts. If None, defaults to petri_net['initial_marking'].
        use_swimlanes (bool): If True, clusters places and transitions by their
            departmental 'lane' attribute.

    Returns:
        str: Valid Graphviz DOT representation ready for st.graphviz_chart.
    """
    if current_marking is None:
        current_marking = petri_net["initial_marking"]

    dot_lines = [
        "digraph PetriNet {",
        "    rankdir=LR;",
        "    compound=true;",
        '    node [fontname="Helvetica, Arial, sans-serif", fontsize=10];',
        '    edge [fontname="Helvetica, Arial, sans-serif", fontsize=9, color="#334155", penwidth=1.5];',
        ""
    ]

    def render_place(p: Dict[str, Any]) -> str:
        tokens = current_marking.get(p["id"], 0)
        token_str = (
            f"\\n[ ● {tokens} tokens ]" if tokens > 1
            else (f"\\n[ ● {tokens} token ]" if tokens == 1 else "\\n[ 0 ]")
        )

        if p["id"] == petri_net["final_place"]:
            shape = "doublecircle"
            fill = "#FEF3C7" if tokens > 0 else "#F1F5F9"
            color = "#D97706" if tokens > 0 else "#64748B"
        elif tokens > 0:
            shape = "circle"
            fill = "#FEF08A"
            color = "#CA8A04"
        else:
            shape = "circle"
            fill = "#F8FAFC"
            color = "#64748B"

        return (
            f'        {p["id"]} [shape={shape}, label="{p["id"]}{token_str}", style=filled, '
            f'fillcolor="{fill}", color="{color}", penwidth=2, width=0.75];'
        )

    def render_transition(t_id: str, t_info: Dict[str, Any]) -> str:
        t_type = t_info.get("type", "standard")
        if t_type == "violation":
            fill = "#EF4444"
            fontcolor = "white"
            color = "#B91C1C"
        elif t_type == "prerequisite":
            fill = "#2563EB"
            fontcolor = "white"
            color = "#1D4ED8"
        elif t_type == "decision":
            fill = "#059669" if "Approve" in t_info["label"] else "#DC2626"
            fontcolor = "white"
            color = "#047857" if "Approve" in t_info["label"] else "#B91C1C"
        else:
            fill = "#475569"
            fontcolor = "white"
            color = "#334155"

        return (
            f'        {t_id} [shape=rect, style=filled, fillcolor="{fill}", color="{color}", '
            f'fontcolor="{fontcolor}", label="{t_info["label"]}", penwidth=1.5, height=0.38];'
        )

    if use_swimlanes:
        # Group places and transitions by lane
        lanes = {}
        for p in petri_net["places"]:
            lane = p.get("lane", "General Workflow")
            lanes.setdefault(lane, {"places": [], "transitions": []})["places"].append(p)

        for t_id, t_info in petri_net["transitions"].items():
            lane = t_info.get("lane", "General Workflow")
            lanes.setdefault(lane, {"places": [], "transitions": []})["transitions"].append((t_id, t_info))

        for idx, (lane_name, elements) in enumerate(lanes.items()):
            fill = "#F8FAFC" if idx % 2 == 0 else "#F1F5F9"
            dot_lines.append(f'    subgraph cluster_pn_lane_{idx} {{')
            dot_lines.append(f'        label = "🏊 {lane_name}";')
            dot_lines.append('        style = "filled,rounded";')
            dot_lines.append(f'        fillcolor = "{fill}";')
            dot_lines.append('        color = "#94A3B8";')
            dot_lines.append('        penwidth = 1.5;')
            dot_lines.append('        fontsize = 11;')
            dot_lines.append('        fontcolor = "#1E3A8A";')
            dot_lines.append("")

            for p in elements["places"]:
                dot_lines.append(render_place(p))
            for t_id, t_info in elements["transitions"]:
                dot_lines.append(render_transition(t_id, t_info))

            dot_lines.append("    }")
            dot_lines.append("")
    else:
        for p in petri_net["places"]:
            dot_lines.append(render_place(p))
        dot_lines.append("")
        for t_id, t_info in petri_net["transitions"].items():
            dot_lines.append(render_transition(t_id, t_info))
        dot_lines.append("")

    # Input Arcs: Place -> Transition
    for t_id, t_info in petri_net["transitions"].items():
        for p_in in t_info["inputs"]:
            dot_lines.append(f'    {p_in} -> {t_id};')

    # Output Arcs: Transition -> Place
    for t_id, t_info in petri_net["transitions"].items():
        for p_out in t_info["outputs"]:
            dot_lines.append(f'    {t_id} -> {p_out};')

    dot_lines.append("}")
    return "\n".join(dot_lines)


if __name__ == "__main__":
    print("Testing Graphviz Petri Net Visualizer with Swimlanes...")
    sample_net = {
        "final_place": "p_end",
        "initial_marking": {"p_start": 1, "p_end": 0},
        "places": [
            {"id": "p_start", "label": "p_start", "lane": "Lane 1: Intake"},
            {"id": "p_end", "label": "p_end", "lane": "Lane 2: Underwriting"}
        ],
        "transitions": {
            "t1": {"label": "Activity", "inputs": ["p_start"], "outputs": ["p_end"], "type": "standard", "lane": "Lane 1: Intake"}
        }
    }
    dot_standard = generate_petri_net_dot(sample_net, use_swimlanes=False)
    dot_swimlane = generate_petri_net_dot(sample_net, use_swimlanes=True)
    assert "cluster_pn_lane_0" in dot_swimlane
    print("✅ Visualizer unit test passed successfully with swimlane partitioning.")
