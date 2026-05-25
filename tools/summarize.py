#!/usr/bin/env python3
"""
Read access_compiled.json and produce:
  access_summary.md          — human-readable overview
  access_graph_compact.json  — stripped graph (no Control/Event/Module nodes)
  access_index.json          — per-form event/subform index

Usage: python tools/summarize.py path/to/access_compiled.json
"""
import json
import pathlib
import sys
from collections import defaultdict

_DAO_TYPES: dict[int, str] = {
    1: "Boolean",
    2: "Byte",
    3: "Integer",
    4: "Long Integer",
    5: "Currency",
    6: "Single",
    7: "Double",
    8: "Date/Time",
    9: "Binary",
    10: "Text",
    11: "OLE Object",
    12: "Memo",
    15: "GUID",
    16: "Big Integer",
}

_COMPACT_NODE_KINDS = {"Form", "Subform", "Table", "Procedure", "Macro"}
_COMPACT_EDGE_KINDS = {
    "EVENT_TRIGGERS", "EVENT_OPENS_FORM", "EVENT_RUNS_QUERY",
    "CALLS", "EMBEDS_SUBFORM", "DEPENDS_ON",
}

_VBA_BUILTINS: frozenset[str] = frozenset({
    "Shell", "MsgBox", "InputBox", "IsNull", "IsEmpty", "Nz",
    "DLookup", "DCount", "DSum", "DFirst", "DLast", "DMax", "DMin", "DAvg",
    "Format", "CStr", "CInt", "CLng", "CDbl", "CBool", "CDate",
    "Left", "Right", "Mid", "Len", "Trim", "UCase", "LCase",
    "InStr", "Replace", "Split", "Join", "Array",
    "Now", "Date", "Time", "DateAdd", "DateDiff", "DatePart",
    "Year", "Month", "Day", "Weekday", "Timer",
    "Environ", "Dir", "EOF",
})


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def run_summarize(input_path: pathlib.Path) -> dict[str, pathlib.Path]:
    """Write the three summary files and return their paths."""
    data = json.loads(input_path.read_text(encoding="utf-8"))
    out_dir = input_path.parent

    nodes: dict[str, dict] = {n["id"]: n for n in data["nodes"]}
    edges: list[dict] = data["edges"]
    hierarchy: dict = data.get("hierarchy", {})

    edges_by_src: dict[str, list[dict]] = defaultdict(list)
    edges_by_dst: dict[str, list[dict]] = defaultdict(list)
    edges_by_kind: dict[str, list[dict]] = defaultdict(list)
    for e in edges:
        edges_by_src[e["src"]].append(e)
        edges_by_dst[e["dst"]].append(e)
        edges_by_kind[e["kind"]].append(e)

    nodes_by_kind: dict[str, list[dict]] = defaultdict(list)
    for n in nodes.values():
        nodes_by_kind[n["kind"]].append(n)

    md_path      = out_dir / "access_summary.md"
    compact_path = out_dir / "access_graph_compact.json"
    index_path   = out_dir / "access_index.json"

    md_path.write_text(
        _build_summary(nodes, nodes_by_kind, edges_by_src, edges_by_dst, edges_by_kind, hierarchy),
        encoding="utf-8",
    )
    compact_path.write_text(
        json.dumps(_build_compact(nodes_by_kind, edges), indent=2),
        encoding="utf-8",
    )
    index_path.write_text(
        json.dumps(_build_index(nodes_by_kind, edges_by_src, edges_by_kind, hierarchy), indent=2),
        encoding="utf-8",
    )

    return {"summary_md": md_path, "compact_json": compact_path, "index_json": index_path}


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python summarize.py <access_compiled.json>")
        sys.exit(1)

    input_path = pathlib.Path(sys.argv[1])
    paths = run_summarize(input_path)

    data = json.loads(input_path.read_text(encoding="utf-8"))
    nodes_by_kind: dict[str, list[dict]] = defaultdict(list)
    for n in data["nodes"]:
        nodes_by_kind[n["kind"]].append(n)

    print(f"Input:   {input_path}  ({input_path.stat().st_size:>10,} bytes)")
    for label, path in (("Summary", paths["summary_md"]), ("Compact", paths["compact_json"]), ("Index", paths["index_json"])):
        print(f"{label:<8} {path}  ({path.stat().st_size:>10,} bytes)")
    print()
    print(f"Forms: {len(nodes_by_kind['Form'])}  "
          f"Tables: {len(nodes_by_kind['Table'])}  "
          f"Queries: {len(nodes_by_kind['Query'])}  "
          f"Modules: {len(nodes_by_kind['Module'])}")
    print(f"Controls: {len(nodes_by_kind['Control'])}  "
          f"Events: {len(nodes_by_kind['Event'])}  "
          f"Procedures: {len(nodes_by_kind['Procedure'])}")
    print(f"Total nodes: {len(data['nodes'])}  Total edges: {len(data['edges'])}")


# ---------------------------------------------------------------------------
# 1. Markdown summary
# ---------------------------------------------------------------------------

def _build_summary(
    nodes: dict[str, dict],
    nodes_by_kind: dict[str, list[dict]],
    edges_by_src: dict[str, list[dict]],
    edges_by_dst: dict[str, list[dict]],
    edges_by_kind: dict[str, list[dict]],
    hierarchy: dict,
) -> str:
    sections: list[str] = []

    # Overview table
    sections.append("# Access Application Summary\n")
    sections.append("## Overview\n")
    rows = [("Category", "Count"), ("---", "---")]
    for kind in ("Form", "Subform", "Table", "Query", "Module", "Control", "Event", "Procedure", "Macro"):
        rows.append((f"{kind}s", str(len(nodes_by_kind[kind]))))
    sections.append("\n".join(f"| {a} | {b} |" for a, b in rows))
    sections.append("")

    # Data model
    sections.append("## Data Model\n")
    for table in sorted(nodes_by_kind["Table"], key=lambda n: n["name"]):
        props = table.get("properties", {})
        rec = props.get("record_count")
        count_str = f" ({rec:,} records)" if isinstance(rec, int) else ""
        sections.append(f"### {table['name']}{count_str}\n")
        fields = props.get("fields", [])
        if fields:
            sections.append("| Field | Type |")
            sections.append("|-------|------|")
            for f in fields:
                type_str = _DAO_TYPES.get(f.get("type"), str(f.get("type", "")))
                sections.append(f"| {f.get('name', '')} | {type_str} |")
        sections.append("")

    # Form hierarchy
    sections.append("## Form Hierarchy\n")
    sections.append(_render_hierarchy(hierarchy))
    sections.append("")

    # Navigation flows
    sections.append("## Navigation Flows\n")
    flow_lines: list[str] = []
    seen_flows: set[str] = set()
    for edge in edges_by_kind["EVENT_OPENS_FORM"]:
        proc_id = edge["src"]
        target_name = edge["dst"].split(":", 1)[1]
        label = _proc_to_form_ctrl(proc_id, edges_by_dst)
        entry = f"- `{label}` → opens → `{target_name}`"
        if entry not in seen_flows:
            seen_flows.add(entry)
            flow_lines.append(entry)
    sections.append("\n".join(flow_lines) if flow_lines else "_None found._")
    sections.append("")

    # Key VBA procedures
    sections.append("## Key VBA Procedures (by outgoing CALLS)\n")
    call_counts = [
        (n["name"], sum(1 for e in edges_by_src[n["id"]] if e["kind"] == "CALLS"))
        for n in nodes_by_kind["Procedure"]
    ]
    call_counts = sorted(((n, c) for n, c in call_counts if c > 0), key=lambda x: x[1], reverse=True)
    if call_counts:
        sections.append("| Procedure | Outgoing Calls |")
        sections.append("|-----------|----------------|")
        for name, count in call_counts[:10]:
            sections.append(f"| {name} | {count} |")
    else:
        sections.append("_None found._")
    sections.append("")

    # Dead controls
    sections.append("## Dead Controls (no events, no control source)\n")
    dead: list[str] = []
    for n in nodes_by_kind["Control"]:
        props = n.get("properties", {})
        if not props.get("events") and not props.get("control_source"):
            ctrl_id = n["id"]  # "ctrl:FormName.CtrlName"
            try:
                form_ctrl = ctrl_id.split(":", 1)[1]
                form_name, ctrl_name = form_ctrl.rsplit(".", 1)
                dead.append(f"- `{form_name}` / `{ctrl_name}`")
            except ValueError:
                dead.append(f"- `{ctrl_id}`")
    sections.append("\n".join(sorted(dead)) if dead else "_None found._")
    sections.append("")

    return "\n".join(sections)


def _render_hierarchy(hierarchy: dict, indent: int = 0) -> str:
    lines: list[str] = []
    prefix = "  " * indent
    for form_id, entry in hierarchy.items():
        form_name = form_id.split(":", 1)[1]
        ctrl = entry.get("embedding_control")
        suffix = f" _(via {ctrl})_" if ctrl else ""
        lines.append(f"{prefix}- **{form_name}**{suffix}")
        children = entry.get("children", {})
        if children:
            lines.append(_render_hierarchy(children, indent + 1))
    return "\n".join(lines)


def _proc_to_form_ctrl(proc_id: str, edges_by_dst: dict[str, list[dict]]) -> str:
    """Resolve a proc node back to FormName.CtrlName via EVENT_TRIGGERS edge."""
    triggers = [e for e in edges_by_dst.get(proc_id, []) if e["kind"] == "EVENT_TRIGGERS"]
    if not triggers:
        return proc_id
    event_id = triggers[0]["src"]  # "event:ctrl:FormName.CtrlName.EventName"
    try:
        remainder = event_id[len("event:ctrl:"):]
        ctrl_dotted, _ = remainder.rsplit(".", 1)    # drop EventName
        form_name, ctrl_name = ctrl_dotted.rsplit(".", 1)
        return f"{form_name}.{ctrl_name}"
    except (ValueError, IndexError):
        return proc_id


# ---------------------------------------------------------------------------
# 2. Compact graph
# ---------------------------------------------------------------------------

def _build_compact(nodes_by_kind: dict[str, list[dict]], edges: list[dict]) -> dict:
    compact_nodes = [
        {"id": n["id"], "kind": n["kind"], "name": n["name"]}
        for kind in _COMPACT_NODE_KINDS
        for n in nodes_by_kind[kind]
    ]
    compact_edges = [
        {"src": e["src"], "dst": e["dst"], "kind": e["kind"]}
        for e in edges
        if e["kind"] in _COMPACT_EDGE_KINDS
        and not e["src"].startswith("query:")
        and not e["dst"].startswith("query:")
    ]
    return {
        "query_count": len(nodes_by_kind["Query"]),
        "nodes": compact_nodes,
        "edges": compact_edges,
    }


# ---------------------------------------------------------------------------
# 3. Per-form index
# ---------------------------------------------------------------------------

def _build_index(
    nodes_by_kind: dict[str, list[dict]],
    edges_by_src: dict[str, list[dict]],
    edges_by_kind: dict[str, list[dict]],
    hierarchy: dict,
) -> dict:

    def _subform_names(entry: dict) -> list[str]:
        result = []
        for child_id, child_entry in entry.get("children", {}).items():
            result.append(child_id.split(":", 1)[1])
            result.extend(_subform_names(child_entry))
        return result

    index: dict[str, dict] = {}

    for form_node in nodes_by_kind["Form"]:
        form_name = form_node["name"]
        form_id   = form_node["id"]
        ctrl_prefix = f"ctrl:{form_name}."

        ctrl_nodes = [n for n in nodes_by_kind["Control"] if n["id"].startswith(ctrl_prefix)]

        controls_with_events = [
            n["name"] for n in ctrl_nodes if n.get("properties", {}).get("events")
        ]

        fields = sorted({
            src
            for n in ctrl_nodes
            if (src := (n.get("properties") or {}).get("control_source"))
            and not src.startswith("=")
        })

        event_list: list[dict] = []
        for ctrl_node in ctrl_nodes:
            ctrl_id = ctrl_node["id"]
            for ce in edges_by_src.get(ctrl_id, []):
                if ce["kind"] != "CONTAINS":
                    continue
                event_id = ce["dst"]
                event_name = event_id.rsplit(".", 1)[-1]
                for te in edges_by_src.get(event_id, []):
                    if te["kind"] != "EVENT_TRIGGERS":
                        continue
                    proc_id = te["dst"]
                    out = edges_by_src.get(proc_id, [])
                    event_list.append({
                        "control": ctrl_node["name"],
                        "event":   event_name,
                        "calls": [
                            e["dst"] for e in out
                            if e["kind"] == "CALLS"
                            and e["dst"].removeprefix("proc:") not in _VBA_BUILTINS
                        ],
                        "opens":   [e["dst"] for e in out if e["kind"] == "EVENT_OPENS_FORM"],
                        "runs":    [e["dst"] for e in out if e["kind"] == "EVENT_RUNS_QUERY"],
                    })

        index[form_name] = {
            "fields":               fields,
            "controls_with_events": controls_with_events,
            "events":               event_list,
            "subforms":             _subform_names(hierarchy.get(form_id, {})),
        }

    return index


if __name__ == "__main__":
    main()
