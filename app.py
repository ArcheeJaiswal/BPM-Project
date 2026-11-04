"""
========================================================================================
Compliance Verification Studio
Formal Business Process Modeling & Verification using BPMN and Petri Nets
========================================================================================
Tech Stack: Python 3 + Streamlit + Graphviz

Modular Architecture:
  - catalog.py: Process models, Petri net specifications, and compliance rules.
  - simulation.py: Token enabling and firing rules (is_transition_enabled, fire_transition).
  - reachability.py: Depth-First Search reachability engine (discover_all_execution_paths).
  - verifier.py: Formal precedence and governance compliance checks (verify_path_compliance).
  - visualizer.py: Dynamic Graphviz Petri Net renderer with Swimlane partitioning.
  - styles.py: High-contrast CSS and layout components (apply_custom_css).
========================================================================================
"""

import streamlit as st
import streamlit.components.v1 as components

# Import dedicated modular functions
from catalog import COMPLEXITY_CATALOG
from simulation import is_transition_enabled, fire_transition
from reachability import discover_all_execution_paths
from verifier import verify_path_compliance
from visualizer import generate_petri_net_dot
from styles import apply_custom_css
from swimlane_svg import get_swimlane_svg, get_swimlane_dimensions


# ======================================================================================
# PAGE CONFIGURATION & STYLING
# ======================================================================================
st.set_page_config(
    page_title="Compliance Verification Studio",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply modular custom styling
apply_custom_css()


# ======================================================================================
# SESSION STATE INITIALIZATION
# ======================================================================================
def reset_downstream_stages():
    """Resets Petri net, simulation, verification, and report state upon configuration change."""
    st.session_state.petri_generated = False
    st.session_state.verified = False
    st.session_state.report_generated = False
    st.session_state.token_marking = None
    st.session_state.sim_history = []


if "active_complexity_key" not in st.session_state or st.session_state.active_complexity_key not in COMPLEXITY_CATALOG:
    st.session_state.active_complexity_key = "level3"
if "active_variant" not in st.session_state:
    st.session_state.active_variant = "compliant"
if "petri_generated" not in st.session_state:
    st.session_state.petri_generated = False
if "verified" not in st.session_state:
    st.session_state.verified = False
if "report_generated" not in st.session_state:
    st.session_state.report_generated = False
if "token_marking" not in st.session_state:
    st.session_state.token_marking = None
if "sim_history" not in st.session_state:
    st.session_state.sim_history = []


# ======================================================================================
# SIDEBAR CONTROLS
# ======================================================================================
with st.sidebar:
    st.markdown("""
    <div style="margin-bottom: 12px;">
        <h3 style="margin: 0; color: #1E3A8A !important; font-size: 1.25rem; font-weight: 800;">⚖️ Studio Controls</h3>
        <p style="margin: 3px 0 0 0; color: #475569 !important; font-size: 0.84rem;">
            Unified Domain: <strong>Banking Loan Origination</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 1. Complexity Selection
    complexity_options = {
        "level1": "🟢 Level 1: Basic (Sequential + XOR)",
        "level2": "🟡 Level 2: Medium (Parallel AND Gateways)",
        "level3": "🔴 Level 3: Advanced (Multi-Gateway: Inclusive, Parallel & XOR)"
    }

    selected_complexity = st.selectbox(
        "1. Select Architectural Complexity:",
        options=list(complexity_options.keys()),
        format_func=lambda k: complexity_options[k],
        index=list(complexity_options.keys()).index(st.session_state.active_complexity_key)
    )

    # 2. Variant Selection
    variant_options = {
        "compliant": "✅ Compliant Model",
        "violating": "⚠️ Model with Violation"
    }

    selected_variant = st.selectbox(
        "2. Select Model Variant:",
        options=list(variant_options.keys()),
        format_func=lambda k: variant_options[k],
        index=list(variant_options.keys()).index(st.session_state.active_variant)
    )

    # Detect selection change and reset downstream state
    if (selected_complexity != st.session_state.active_complexity_key or 
        selected_variant != st.session_state.active_variant):
        st.session_state.active_complexity_key = selected_complexity
        st.session_state.active_variant = selected_variant
        reset_downstream_stages()
        st.rerun()

    # Reset Button
    if st.button("🔄 Reset Workflow Stages", use_container_width=True):
        reset_downstream_stages()
        st.rerun()

    # Active Configuration Card
    active_comp = COMPLEXITY_CATALOG[st.session_state.active_complexity_key]
    swimlanes_list_html = "".join([f"<li><small>{lane}</small></li>" for lane in active_comp.get("swimlane_roles", [])])

    st.markdown(f"""
    <div class="sidebar-card">
        <p style="margin: 0 0 4px 0; font-size: 0.72rem; color: #64748B !important; text-transform: uppercase; font-weight: 800; letter-spacing: 0.6px;">ACTIVE CONFIGURATION</p>
        <p style="margin: 0 0 4px 0; font-size: 0.95rem; font-weight: 700; color: #1E3A8A !important;">{active_comp['complexity_badge']} {active_comp['title'].split(': ')[1]}</p>
        <p style="margin: 0 0 4px 0; font-size: 0.82rem; color: #334155 !important;"><strong>Domain:</strong> {active_comp['domain']}</p>
        <p style="margin: 0 0 4px 0; font-size: 0.82rem; color: #334155 !important;"><strong>Architecture:</strong> {active_comp['architecture_summary']}</p>
        <p style="margin: 0 0 4px 0; font-size: 0.82rem; color: #334155 !important;"><strong>Concurrency:</strong> {active_comp['concurrency_degree']}</p>
        <div style="border-top: 1px solid #E2E8F0; margin: 6px 0;"></div>
        <p style="margin: 0 0 3px 0; font-size: 0.75rem; font-weight: 800; color: #1E3A8A !important; text-transform: uppercase;">ORGANIZATIONAL SWIMLANES ({len(active_comp.get('swimlane_roles', []))}):</p>
        <ul style="margin: 0 0 6px 0; padding-left: 16px; color: #334155 !important;">
            {swimlanes_list_html}
        </ul>
        <div style="border-top: 1px solid #E2E8F0; margin: 6px 0;"></div>
        <p style="margin: 0 0 4px 0; font-size: 0.75rem; font-weight: 800; color: #1E3A8A !important; text-transform: uppercase;">MANDATORY COMPLIANCE RULE:</p>
        <div style="background-color: #EFF6FF; border-left: 3px solid #2563EB; padding: 6px 10px; border-radius: 4px;">
            <p style="margin: 0; font-size: 0.82rem; line-height: 1.35; color: #1E40AF !important; font-weight: 600;">
                \"{active_comp['rule_text']}\"
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ======================================================================================
# MAIN APPLICATION NAVBAR
# ======================================================================================
st.markdown("""
<div class="custom-navbar">
    <div style="display: flex; align-items: center; gap: 10px;">
        <span style="font-size: 1.35rem;">⚖️</span>
        <div>
            <div style="font-size: 1.15rem; font-weight: 800; color: #1E3A8A; line-height: 1.1;">Compliance Verification Studio</div>
            <div style="font-size: 0.76rem; color: #64748B;">Unified Domain: Banking Loan Origination Across Progressive Complexities with Multi-Type Gateways (AND, OR, XOR) & Swimlanes</div>
        </div>
    </div>
    <div>
        <span style="font-size: 0.78rem; background: #EFF6FF; color: #1D4ED8; font-weight: 600; padding: 4px 10px; border-radius: 14px; border: 1px solid #BFDBFE;">
            ⚡ Formal Reachability Engine
        </span>
    </div>
</div>
""", unsafe_allow_html=True)



# Active data references
active_comp = COMPLEXITY_CATALOG[st.session_state.active_complexity_key]
active_var_data = active_comp[st.session_state.active_variant]
petri_net_spec = active_var_data["petri_net"]
rule_spec = active_comp["rule_spec"]

# Stage Indicators
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown("<small style='color: #64748B;'>1. BPMN Model</small><br><strong>🟢 Ready</strong>", unsafe_allow_html=True)
with c2:
    s2 = "<strong style='color: #15803D;'>🟢 Done</strong>" if st.session_state.petri_generated else "<span style='color: #94A3B8;'>⚪ Pending</span>"
    st.markdown(f"<small style='color: #64748B;'>2. Petri Net</small><br>{s2}", unsafe_allow_html=True)
with c3:
    s3 = "<strong style='color: #15803D;'>🟢 Done</strong>" if st.session_state.verified else "<span style='color: #94A3B8;'>⚪ Pending</span>"
    st.markdown(f"<small style='color: #64748B;'>3. Verification</small><br>{s3}", unsafe_allow_html=True)
with c4:
    s4 = "<strong style='color: #15803D;'>🟢 Done</strong>" if st.session_state.report_generated else "<span style='color: #94A3B8;'>⚪ Pending</span>"
    st.markdown(f"<small style='color: #64748B;'>4. Diagnostic Report</small><br>{s4}", unsafe_allow_html=True)

st.markdown("<hr style='margin: 8px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)

# ----------------------------------------------------------------------------------
# STAGE 1: BPMN 2.0 ORGANIZATIONAL SWIMLANE MODEL
# ----------------------------------------------------------------------------------
st.markdown(f"### 1. BPMN Process Model: {active_comp['complexity_badge']} {active_comp['title']}")

v_badge = '<span class="badge-compliant">Compliant Model</span>' if st.session_state.active_variant == 'compliant' else '<span class="badge-violation">Model with Violation</span>'

st.markdown(f"""
<div class="compact-card" style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
    <div>
        <strong>Architecture:</strong> {active_comp['architecture_summary']} &nbsp;|&nbsp; 
        <strong>Rule:</strong> <em>"{active_comp['rule_text']}"</em>
    </div>
    <div>
        <strong>Variant:</strong> {v_badge}
    </div>
</div>
""", unsafe_allow_html=True)

st.caption("Displaying publication-grade BPMN 2.0 organizational swimlanes with left vertical headers and orthogonal obstacle-avoiding routing.")

svg_w, svg_h = get_swimlane_dimensions(st.session_state.active_complexity_key, st.session_state.active_variant)
svg_content = get_swimlane_svg(st.session_state.active_complexity_key, st.session_state.active_variant)
container_h = int(svg_h + 30)

html_wrapper = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{ margin: 0; padding: 0; background: #FFFFFF; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
  .scroll-wrapper {{ width: 100%; overflow-x: auto; overflow-y: hidden; background: #FFFFFF; padding: 6px; box-sizing: border-box; }}
</style>
</head>
<body>
  <div class="scroll-wrapper">
    {svg_content}
  </div>
</body>
</html>"""

components.html(html_wrapper, height=container_h, scrolling=True)
st.download_button(
    label="📥 Download BPMN 2.0 Swimlane Diagram (SVG)",
    data=svg_content,
    file_name=f"bpmn_swimlane_{st.session_state.active_complexity_key}_{st.session_state.active_variant}.svg",
    mime="image/svg+xml"
)

# ----------------------------------------------------------------------------------
# STAGE 2: PETRI NET GENERATION & TOKEN SIMULATOR (WITH SWIMLANE PARTITION)
# ----------------------------------------------------------------------------------
st.markdown("<hr style='margin: 10px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
st.markdown("### 2. Petri Net Formal Representation & Simulation")

col_btn1, col_info1 = st.columns([1, 4])
with col_btn1:
    if st.button("⚡ Generate Petri Net", type="primary", use_container_width=True):
        st.session_state.petri_generated = True
        st.session_state.token_marking = dict(petri_net_spec["initial_marking"])
        st.session_state.sim_history = [("M0", dict(petri_net_spec["initial_marking"]))]
        st.rerun()

with col_info1:
    if not st.session_state.petri_generated:
        st.caption("Click to convert the active BPMN workflow into formal places, transitions, and arcs (P, T, F, M0).")
    else:
        st.caption(f"✅ Petri Net model generated ({len(petri_net_spec['places'])} Places, {len(petri_net_spec['transitions'])} Transitions).")

if st.session_state.petri_generated:
    if st.session_state.token_marking is None:
        st.session_state.token_marking = dict(petri_net_spec["initial_marking"])

    # Petri Net Layout Selector: Swimlane Partition vs Unified
    pn_layout_choice = st.radio(
        "Select Petri Net Diagram Layout:",
        options=["🏊 Swimlane Department Partition", "⚡ Unified Workflow Net"],
        horizontal=True
    )
    use_pn_swimlanes = "Swimlane" in pn_layout_choice

    # Call visualizer.py function with swimlane flag
    pn_dot = generate_petri_net_dot(petri_net_spec, st.session_state.token_marking, use_swimlanes=use_pn_swimlanes)
    st.graphviz_chart(pn_dot, use_container_width=True)

    tab_pt, tab_sim = st.tabs(["📋 Formal Components (P, T, F, M0)", "🎮 Step-by-Step Token Simulator"])

    with tab_pt:
        c_p, c_t = st.columns(2)
        with c_p:
            st.markdown("**Places (P):**")
            p_table = []
            for p in petri_net_spec["places"]:
                cur = st.session_state.token_marking.get(p["id"], 0)
                meaning = p["label"].split(" (")[1].replace(")", "") if "(" in p["label"] else p["label"]
                p_table.append({
                    "Place": p["id"],
                    "Tokens": cur,
                    "Meaning": meaning,
                    "Department / Lane": p.get("lane", "General")
                })
            st.table(p_table)

        with c_t:
            st.markdown("**Transitions (T):**")
            t_table = []
            for t_id, t_info in petri_net_spec["transitions"].items():
                t_table.append({
                    "Transition": t_id,
                    "Activity": t_info["label"],
                    "Inputs (Pre)": ", ".join(t_info["inputs"]),
                    "Outputs (Post)": ", ".join(t_info["outputs"]),
                    "Role / Lane": t_info.get("lane", "General"),
                    "Type": t_info.get("type", "standard").capitalize()
                })
            st.table(t_table)

    with tab_sim:
        current_marking = st.session_state.token_marking
        # Call simulation.py function: is_transition_enabled
        enabled_transitions = {
            t_id: t_info for t_id, t_info in petri_net_spec["transitions"].items()
            if is_transition_enabled(t_info, current_marking)
        }

        col_s1, col_s2 = st.columns(2)
        with col_s1:
            final_sink_tokens = current_marking.get(petri_net_spec["final_place"], 0)
            if final_sink_tokens >= 1:
                st.success(f"Token arrived in terminal sink place '{petri_net_spec['final_place']}'. Workflow execution complete.")
            elif not enabled_transitions:
                st.warning("Deadlock / No enabled transitions in current marking.")
            else:
                sel_t = st.selectbox(
                    "Select enabled transition to fire:",
                    options=list(enabled_transitions.keys()),
                    format_func=lambda x: f"{x}: {enabled_transitions[x]['label']} [{enabled_transitions[x].get('lane', 'General')}]"
                )
                if st.button("▶ Fire Selected Transition", type="primary"):
                    # Call simulation.py function: fire_transition
                    new_m = fire_transition(enabled_transitions[sel_t], current_marking)
                    st.session_state.token_marking = new_m
                    st.session_state.sim_history.append((sel_t, new_m))
                    st.rerun()

            if st.button("↺ Reset Token to M0"):
                st.session_state.token_marking = dict(petri_net_spec["initial_marking"])
                st.session_state.sim_history = [("M0", dict(petri_net_spec["initial_marking"]))]
                st.rerun()

        with col_s2:
            st.markdown("**Active Token Distribution (Marking):**")
            active_p = [f"<code>{k}</code>: {v} token(s)" for k, v in current_marking.items() if v > 0]
            if active_p:
                st.markdown("<br>".join(active_p), unsafe_allow_html=True)
            else:
                st.write("No active tokens.")

            st.markdown(f"**Step History:** {len(st.session_state.sim_history)} step(s)")

# ----------------------------------------------------------------------------------
# STAGE 3: COMPLIANCE VERIFICATION
# ----------------------------------------------------------------------------------
st.markdown("<hr style='margin: 10px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
st.markdown("### 3. Compliance Verification via Reachability State-Space DFS")

col_btn2, col_info2 = st.columns([1, 4])
with col_btn2:
    v_disabled = not st.session_state.petri_generated
    if st.button("🔍 Verify Compliance", type="primary", disabled=v_disabled, use_container_width=True):
        st.session_state.verified = True
        st.session_state.report_generated = False
        st.rerun()

with col_info2:
    if v_disabled:
        st.caption("Generate Petri Net in Step 2 first.")
    elif not st.session_state.verified:
        st.caption("Click to explore all reachability paths and verify compliance rules.")
    else:
        st.caption("✅ State-space explored and paths verified.")

if st.session_state.verified and st.session_state.petri_generated:
    # Call reachability.py function: discover_all_execution_paths
    discovered_paths = discover_all_execution_paths(petri_net_spec, max_visits=2)
    path_evaluations = []
    has_violations = False

    for idx, path_tuples in enumerate(discovered_paths, 1):
        # Call verifier.py function: verify_path_compliance
        eval_result = verify_path_compliance(path_tuples, rule_spec)
        if not eval_result["compliant"]:
            has_violations = True
        path_evaluations.append({
            "path_id": idx,
            "tuples": path_tuples,
            "labels": [t[1] for t in path_tuples],
            "evaluation": eval_result
        })

    # Verdict Banner
    if not has_violations:
        st.markdown(f"""
        <div class="banner-pass">
            <strong>✅ VERIFIED COMPLIANT (PASS):</strong> All {len(path_evaluations)} discovered execution paths satisfy regulatory rule: 
            <em>\"{active_comp['rule_text']}\"</em>.
        </div>
        """, unsafe_allow_html=True)
    else:
        viol_num = sum(1 for p in path_evaluations if not p["evaluation"]["compliant"])
        st.markdown(f"""
        <div class="banner-fail">
            <strong>❌ COMPLIANCE VIOLATION DETECTED (FAIL):</strong> Found {viol_num} defective execution path(s) violating regulatory requirements!
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"**Discovered Complete Execution Sequences ({len(path_evaluations)}):**")
    for item in path_evaluations:
        p_id = item["path_id"]
        p_labels = item["labels"]
        eval_res = item["evaluation"]
        badge_cls = "badge-compliant" if eval_res["compliant"] else "badge-violation"
        seq = " ➔ ".join([f"<code>{lbl}</code>" for lbl in p_labels])

        st.markdown(f"""
        <div class="path-row">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span><strong>Path #{p_id}:</strong> {seq}</span>
                <span class="{badge_cls}">{eval_res['status']}</span>
            </div>
            <div style="color: #64748B; font-size: 0.8rem; margin-top: 3px;">
                {eval_res['reason']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------------------------------------------------------------
# STAGE 4: DIAGNOSTIC AUDIT REPORT
# ----------------------------------------------------------------------------------
st.markdown("<hr style='margin: 10px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
st.markdown("### 4. Diagnostic Audit Report & Remediation")

col_btn3, col_info3 = st.columns([1, 4])
with col_btn3:
    r_disabled = not st.session_state.verified
    if st.button("📋 Generate Diagnostic Report", type="primary", disabled=r_disabled, use_container_width=True):
        st.session_state.report_generated = True
        st.rerun()

with col_info3:
    if r_disabled:
        st.caption("Verify compliance in Step 3 first.")
    elif not st.session_state.report_generated:
        st.caption("Click to compile summary metrics and root-cause remediation guidance.")

if st.session_state.report_generated and st.session_state.verified:
    paths = discover_all_execution_paths(petri_net_spec, max_visits=2)
    total_paths = len(paths)
    evals = [verify_path_compliance(p, rule_spec) for p in paths]
    comp_count = sum(1 for e in evals if e["compliant"])
    viol_count = total_paths - comp_count

    # 4 Metric Cards
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""<div class="compact-card" style="text-align: center;"><small style="color: #64748B;">Total Paths</small><br><strong style="font-size: 1.15rem;">{total_paths}</strong></div>""", unsafe_allow_html=True)
    with m2:
        st.markdown(f"""<div class="compact-card" style="text-align: center;"><small style="color: #166534;">Compliant Paths</small><br><strong style="font-size: 1.15rem; color: #15803D;">{comp_count}</strong></div>""", unsafe_allow_html=True)
    with m3:
        v_col = "#DC2626" if viol_count > 0 else "#64748B"
        st.markdown(f"""<div class="compact-card" style="text-align: center;"><small style="color: {v_col};">Violations</small><br><strong style="font-size: 1.15rem; color: {v_col};">{viol_count}</strong></div>""", unsafe_allow_html=True)
    with m4:
        verd = "FAIL" if viol_count > 0 else "PASS"
        verd_col = "#DC2626" if viol_count > 0 else "#15803D"
        st.markdown(f"""<div class="compact-card" style="text-align: center;"><small style="color: {verd_col};">Final Audit Verdict</small><br><strong style="font-size: 1.15rem; color: {verd_col};">{verd}</strong></div>""", unsafe_allow_html=True)

    # Audit Table
    audit_rows = []
    for i, (p_tup, ev) in enumerate(zip(paths, evals), 1):
        lbls = " ➔ ".join([t[1] for t in p_tup])
        audit_rows.append({
            "Path": f"Path #{i}",
            "Activity Sequence": lbls,
            "Status": ev["status"],
            "Formal Finding": ev["reason"]
        })
    st.table(audit_rows)

    # Diagnostic finding & remediation guidance
    remed_info = active_comp["remediation"]
    if viol_count > 0:
        st.markdown(f"""
        <div class="compact-card" style="border-left: 4px solid #DC2626;">
            <strong style="color: #991B1B;">⚠️ Root Cause Diagnostic: {remed_info['violation_title']}</strong><br>
            <span style="color: #475569;">{remed_info['root_cause']}</span><br><br>
            <strong style="color: #1E3A8A;">🛠️ Formal Remediation Guidance:</strong><br>
            <span style="color: #0F172A;">{remed_info['remediation']}</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="compact-card" style="border-left: 4px solid #16A34A;">
            <strong style="color: #15803D;">✅ Process Certified Compliant:</strong> 
            Formal reachability analysis certified that every execution path enforces the mandatory compliance rule: 
            <code>{active_comp['rule_text']}</code>. No unauthorized bypass or race conditions were found across any swimlane.
        </div>
        """, unsafe_allow_html=True)


# ======================================================================================
