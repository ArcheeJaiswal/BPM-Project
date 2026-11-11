"""
========================================================================================
PNML (Petri Net Markup Language) Exporter
Exports catalog Place/Transition nets to ISO/IEC 15909 standard PNML XML.
========================================================================================
"""

import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from catalog import COMPLEXITY_CATALOG


def generate_pnml_xml(level_key: str, variant: str) -> str:
    """Generates standard PNML XML string for a catalog Petri net."""
    comp = COMPLEXITY_CATALOG[level_key]
    var_data = comp[variant]
    pn_spec = var_data["petri_net"]
    title = f"{comp['title']} - {variant.capitalize()} Variant"
    net_id = f"net_{level_key}_{variant}"

    pnml = ET.Element("pnml", xmlns="http://www.pnml.org/version-2009/grammar/pnml")
    net = ET.SubElement(pnml, "net", id=net_id, type="http://www.pnml.org/version-2009/grammar/ptnet")
    
    net_name = ET.SubElement(net, "name")
    ET.SubElement(net_name, "text").text = title

    page = ET.SubElement(net, "page", id="page_0")

    # 1. Places
    for pl in pn_spec["places"]:
        p_elem = ET.SubElement(page, "place", id=pl["id"])
        p_name = ET.SubElement(p_elem, "name")
        ET.SubElement(p_name, "text").text = pl.get("label", pl["id"])
        
        init_m = pl.get("initial_tokens", 0)
        if init_m > 0:
            init_elem = ET.SubElement(p_elem, "initialMarking")
            ET.SubElement(init_elem, "text").text = str(init_m)

    # 2. Transitions
    for tid, tinfo in pn_spec["transitions"].items():
        t_elem = ET.SubElement(page, "transition", id=tid)
        t_name = ET.SubElement(t_elem, "name")
        ET.SubElement(t_name, "text").text = tinfo.get("label", tid)

    # 3. Arcs
    arc_idx = 1
    for tid, tinfo in pn_spec["transitions"].items():
        # Input places -> transition
        for pin in tinfo.get("inputs", []):
            arc = ET.SubElement(page, "arc", id=f"arc_{arc_idx}", source=pin, target=tid)
            insc = ET.SubElement(arc, "inscription")
            ET.SubElement(insc, "text").text = "1"
            arc_idx += 1
            
        # Transition -> output places
        for pout in tinfo.get("outputs", []):
            arc = ET.SubElement(page, "arc", id=f"arc_{arc_idx}", source=tid, target=pout)
            insc = ET.SubElement(arc, "inscription")
            ET.SubElement(insc, "text").text = "1"
            arc_idx += 1

    # Pretty-print
    xml_str = ET.tostring(pnml, encoding="utf-8")
    parsed = minidom.parseString(xml_str)
    return parsed.toprettyxml(indent="  ")


def export_all_models(output_dir: str = "dataset") -> None:
    """Exports all six workflow catalog models to PNML XML files."""
    os.makedirs(output_dir, exist_ok=True)
    for level_key in ["level1", "level2", "level3"]:
        for variant in ["compliant", "violating"]:
            xml_content = generate_pnml_xml(level_key, variant)
            filename = f"{level_key}_{variant}.pnml"
            filepath = os.path.join(output_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(xml_content)
            print(f"Exported: {filepath}")


if __name__ == "__main__":
    export_all_models()

