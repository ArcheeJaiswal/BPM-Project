"""
========================================================================================
Dataset Generator for BPM Compliance Studio
Generates all 6 workflow diagram models into the dataset/ directory in:
  - .bpmn (Standard BPMN 2.0 XML)
  - .svg  (Publication-grade SVG Vector Diagram)
  - .json (Structured Process Specification)
  - .pnml (Standard Petri Net Markup Language XML)
========================================================================================
"""

import os
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom

from swimlane_svg import get_swimlane_svg, get_swimlane_engine
from catalog import COMPLEXITY_CATALOG
from export_pnml import generate_pnml_xml


def generate_bpmn_xml(level_key: str, variant: str) -> str:
    """Generates standard BPMN 2.0 XML for the specified workflow."""
    is_violating = (variant == "violating")
    engine = get_swimlane_engine(level_key, variant)
    comp = COMPLEXITY_CATALOG[level_key]

    root = ET.Element("bpmn:definitions", {
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xmlns:bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        "xmlns:bpmndi": "http://www.omg.org/spec/BPMN/20100524/DI",
        "xmlns:dc": "http://www.omg.org/spec/DD/20100524/DC",
        "xmlns:di": "http://www.omg.org/spec/DD/20100524/DI",
        "id": f"Definitions_{level_key}_{variant}",
        "targetNamespace": "http://bpmn.io/schema/bpmn",
        "exporter": "Compliance Verification Studio BPMN 2.0 Engine"
    })

    # Collaboration
    collab = ET.SubElement(root, "bpmn:collaboration", id=f"Collaboration_{level_key}")
    
    # Top Pool (Borrower Portal)
    ET.SubElement(collab, "bpmn:participant", {
        "id": "Participant_Portal",
        "name": "Customer / Borrower Portal",
        "processRef": f"Process_{level_key}_Portal"
    })
    
    # Primary Bank Pool
    ET.SubElement(collab, "bpmn:participant", {
        "id": "Participant_Bank",
        "name": engine.pool_title,
        "processRef": f"Process_{level_key}_Bank"
    })

    # Portal Process
    proc_portal = ET.SubElement(root, "bpmn:process", id=f"Process_{level_key}_Portal", isExecutable="false")
    if engine.raw_top_pool:
        for node in engine.raw_top_pool.get("nodes", []):
            nid = node["id"]
            lbl = node.get("label", nid).replace("\n", " ")
            ntype = node.get("type", "task")
            if ntype == "start_event":
                ET.SubElement(proc_portal, "bpmn:startEvent", id=nid, name=lbl)
            elif ntype == "end_event":
                ET.SubElement(proc_portal, "bpmn:endEvent", id=nid, name=lbl)
            elif node.get("task_type") == "receive":
                ET.SubElement(proc_portal, "bpmn:receiveTask", id=nid, name=lbl)
            else:
                ET.SubElement(proc_portal, "bpmn:userTask", id=nid, name=lbl)

    # Bank Process with Lanes
    proc_bank = ET.SubElement(root, "bpmn:process", id=f"Process_{level_key}_Bank", isExecutable="true")
    lane_set = ET.SubElement(proc_bank, "bpmn:laneSet", id=f"LaneSet_{level_key}")
    
    for lane in engine.raw_lanes:
        lid = lane["id"]
        lname = lane.get("name", lid)
        lane_elem = ET.SubElement(lane_set, "bpmn:lane", id=lid, name=lname)
        # Add flow node references
        for n in engine.raw_nodes:
            if n.get("lane") == lid:
                ET.SubElement(lane_elem, "bpmn:flowNodeRef").text = n["id"]

    # Bank Nodes
    for n in engine.raw_nodes:
        nid = n["id"]
        lbl = n.get("label", nid).replace("\n", " ")
        ntype = n.get("type", "task")
        ttype = n.get("task_type", "abstract")

        if ntype == "start_event":
            ET.SubElement(proc_bank, "bpmn:startEvent", id=nid, name=lbl)
        elif ntype == "end_event":
            ET.SubElement(proc_bank, "bpmn:endEvent", id=nid, name=lbl)
        elif "xor" in ntype:
            ET.SubElement(proc_bank, "bpmn:exclusiveGateway", id=nid, name=lbl)
        elif "and" in ntype:
            ET.SubElement(proc_bank, "bpmn:parallelGateway", id=nid, name=lbl)
        elif "or" in ntype:
            ET.SubElement(proc_bank, "bpmn:inclusiveGateway", id=nid, name=lbl)
        elif ttype == "service":
            ET.SubElement(proc_bank, "bpmn:serviceTask", id=nid, name=lbl)
        elif ttype == "user":
            ET.SubElement(proc_bank, "bpmn:userTask", id=nid, name=lbl)
        elif ttype == "receive":
            ET.SubElement(proc_bank, "bpmn:receiveTask", id=nid, name=lbl)
        else:
            ET.SubElement(proc_bank, "bpmn:task", id=nid, name=lbl)

    # Sequence Flows & Message Flows
    flow_idx = 1
    msg_idx = 1
    for edge in engine.raw_edges:
        src = edge["from"]
        dst = edge["to"]
        lbl = edge.get("label", "")
        is_dashed = edge.get("dashed", False)
        is_violation = edge.get("violation", False)

        if is_dashed:
            # Message Flow
            mf = ET.SubElement(collab, "bpmn:messageFlow", {
                "id": f"MsgFlow_{msg_idx}",
                "sourceRef": src,
                "targetRef": dst
            })
            if lbl:
                mf.set("name", lbl)
            msg_idx += 1
        else:
            # Sequence Flow
            sf = ET.SubElement(proc_bank, "bpmn:sequenceFlow", {
                "id": f"Flow_{flow_idx}",
                "sourceRef": src,
                "targetRef": dst
            })
            if lbl:
                sf.set("name", lbl)
            if is_violation:
                sf.set("xsi:type", "bpmn:tViolationFlow")
            flow_idx += 1

    xml_str = ET.tostring(root, encoding="utf-8")
    parsed = minidom.parseString(xml_str)
    return parsed.toprettyxml(indent="  ")


def generate_json_spec(level_key: str, variant: str) -> dict:
    """Generates structured JSON schema definition for the workflow."""
    engine = get_swimlane_engine(level_key, variant)
    comp = COMPLEXITY_CATALOG[level_key]
    var_data = comp[variant]

    return {
        "model_id": f"{level_key}_{variant}",
        "title": comp["title"],
        "variant": variant,
        "domain": comp["domain"],
        "architecture_summary": comp["architecture_summary"],
        "concurrency_degree": comp["concurrency_degree"],
        "compliance_rule": {
            "text": comp["rule_text"],
            "rule_spec": comp["rule_spec"]
        },
        "pools": {
            "top_pool": engine.raw_top_pool,
            "primary_pool": {
                "title": engine.pool_title,
                "lanes": engine.raw_lanes
            }
        },
        "flow_nodes": engine.raw_nodes,
        "flow_edges": engine.raw_edges,
        "petri_net_spec": var_data["petri_net"]
    }


def build_dataset(dataset_dir: str = "dataset") -> None:
    """Builds the complete dataset directory containing all 6 workflow models in BPMN, SVG, JSON, and PNML."""
    os.makedirs(dataset_dir, exist_ok=True)
    models = [
        ("level1", "compliant", "Basic Sequential + Exclusive XOR (Compliant)"),
        ("level1", "violating", "Basic Sequential + Exclusive XOR with Credit Check Bypass (Violation)"),
        ("level2", "compliant", "Medium Parallel Concurrency AND-Split/Join (Compliant)"),
        ("level2", "violating", "Medium Parallel Concurrency with Premature Approval (Violation)"),
        ("level3", "compliant", "Advanced Enterprise Multi-Gateway AND/OR/XOR & Rework Loop (Compliant)"),
        ("level3", "violating", "Advanced Enterprise Multi-Gateway with Executive Board Bypass (Violation)")
    ]

    manifest = []

    for level_key, variant, desc in models:
        prefix = f"{level_key}_{variant}"
        print(f"Generating dataset files for [{prefix}] - {desc}...")

        # 1. BPMN 2.0 XML (.bpmn)
        bpmn_path = os.path.join(dataset_dir, f"{prefix}.bpmn")
        with open(bpmn_path, "w", encoding="utf-8") as f:
            f.write(generate_bpmn_xml(level_key, variant))

        # 2. Vector SVG (.svg)
        svg_path = os.path.join(dataset_dir, f"{prefix}.svg")
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(get_swimlane_svg(level_key, variant))

        # 3. JSON Model Specification (.json)
        json_path = os.path.join(dataset_dir, f"{prefix}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(generate_json_spec(level_key, variant), f, indent=2)

        # 4. Petri Net Markup Language XML (.pnml)
        pnml_path = os.path.join(dataset_dir, f"{prefix}.pnml")
        with open(pnml_path, "w", encoding="utf-8") as f:
            f.write(generate_pnml_xml(level_key, variant))

        manifest.append({
            "model_key": f"{level_key}_{variant}",
            "description": desc,
            "files": {
                "bpmn_xml": bpmn_path,
                "svg_diagram": svg_path,
                "json_spec": json_path,
                "pnml_petri_net": pnml_path
            }
        })

    # Save dataset manifest
    manifest_path = os.path.join(dataset_dir, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"\n✅ Dataset generation complete! All files generated in '{dataset_dir}/'.")


if __name__ == "__main__":
    build_dataset()
