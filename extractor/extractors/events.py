import re

from extractor.graph.edges import Edge, EdgeKind
from extractor.graph.nodes import Node, NodeKind

_EVENT_PROCEDURE = "[Event Procedure]"

# Compiled once at import time
_RE_OPEN_FORM   = re.compile(r'DoCmd\.OpenForm\s+(?:FormName:=)?"([^"]+)"',    re.IGNORECASE)
_RE_RUN_QUERY   = re.compile(r'DoCmd\.RunQuery\s+(?:QueryName:=)?"([^"]+)"',   re.IGNORECASE)
_RE_OPEN_REPORT = re.compile(r'DoCmd\.OpenReport\s+(?:ReportName:=)?"([^"]+)"', re.IGNORECASE)
_RE_OPEN_QUERY  = re.compile(r'DoCmd\.OpenQuery\s+(?:QueryName:=)?"([^"]+)"',  re.IGNORECASE)
_RE_MODIFIES    = re.compile(r'(\w+)\.(Visible|Enabled)\s*=',                  re.IGNORECASE)
_RE_CALLS       = re.compile(r'\bCall\s+(\w+)',                                 re.IGNORECASE)


def resolve_event_bindings(ctrl_node: Node, builder) -> tuple[list[Node], list[Edge]]:
    nodes: list[Node] = []
    edges: list[Edge] = []

    events: dict = ctrl_node.properties.get("events", {})
    if not events:
        return nodes, edges

    ctrl_id = ctrl_node.id  # "ctrl:FormName.CtrlName"
    _, form_ctrl = ctrl_id.split(":", 1)
    form_name, _, ctrl_name = form_ctrl.partition(".")

    for event_name, raw_value in events.items():
        if not raw_value:
            continue

        event_id = f"event:{ctrl_id}.{event_name}"
        nodes.append(Node(
            id=event_id,
            kind=NodeKind.Event,
            name=f"{ctrl_name}_{event_name}",
        ))
        edges.append(Edge(src=ctrl_id, dst=event_id, kind=EdgeKind.CONTAINS))

        if raw_value == _EVENT_PROCEDURE:
            proc_name = f"{form_name}_{ctrl_name}_{event_name}"
            edges.append(Edge(
                src=event_id,
                dst=f"proc:{proc_name}",
                kind=EdgeKind.EVENT_TRIGGERS,
                properties={"binding": "VBA"},
            ))
        else:
            macro_id = f"macro:{raw_value}"
            if not builder.has_node(macro_id):
                nodes.append(Node(id=macro_id, kind=NodeKind.Macro, name=raw_value))
            edges.append(Edge(
                src=event_id,
                dst=macro_id,
                kind=EdgeKind.EVENT_TRIGGERS,
                properties={"binding": "Macro"},
            ))

    return nodes, edges


def analyze_procedure_source(proc_id: str, source_lines: list[str]) -> list[Edge]:
    edges: list[Edge] = []

    for line in source_lines:
        m = _RE_OPEN_FORM.search(line)
        if m:
            edges.append(Edge(src=proc_id, dst=f"form:{m.group(1)}", kind=EdgeKind.EVENT_OPENS_FORM))

        m = _RE_RUN_QUERY.search(line)
        if m:
            edges.append(Edge(src=proc_id, dst=f"query:{m.group(1)}", kind=EdgeKind.EVENT_RUNS_QUERY))

        m = _RE_OPEN_REPORT.search(line)
        if m:
            edges.append(Edge(src=proc_id, dst=f"report:{m.group(1)}", kind=EdgeKind.EVENT_OPENS_FORM))

        m = _RE_OPEN_QUERY.search(line)
        if m:
            edges.append(Edge(src=proc_id, dst=f"query:{m.group(1)}", kind=EdgeKind.EVENT_RUNS_QUERY))

        m = _RE_MODIFIES.search(line)
        if m:
            edges.append(Edge(
                src=proc_id,
                dst=f"ctrl:{m.group(1)}",
                kind=EdgeKind.EVENT_MODIFIES,
                properties={"property": m.group(2)},
            ))

        m = _RE_CALLS.search(line)
        if m:
            edges.append(Edge(src=proc_id, dst=f"proc:{m.group(1)}", kind=EdgeKind.CALLS))

    return edges
