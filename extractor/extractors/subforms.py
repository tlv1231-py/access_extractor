import logging

from extractor.graph.edges import Edge, EdgeKind
from extractor.graph.nodes import Node, NodeKind

_SUBFORM_CONTROL_TYPE = 112


def _safe_get(obj, attr, default=None):
    try:
        return getattr(obj, attr)
    except Exception:
        return default


def extract_subform_hierarchy(
    form_obj,
    form_name: str,
    builder,
    depth: int = 0,
    parent: dict | None = None,
    visited: set[str] | None = None,
) -> tuple[list[Node], list[Edge]]:
    if visited is None:
        visited = set()

    if form_name in visited:
        return [], []
    visited.add(form_name)

    nodes: list[Node] = []
    edges: list[Edge] = []

    form_id = f"form:{form_name}"
    nodes.append(Node(
        id=form_id,
        kind=NodeKind.Subform if depth > 0 else NodeKind.Form,
        name=form_name,
    ))

    if parent is not None:
        edges.append(Edge(
            src=parent["form_id"],
            dst=form_id,
            kind=EdgeKind.EMBEDS_SUBFORM,
            properties={
                "control_name": parent["control_name"],
                "depth": depth,
            },
        ))

    controls = _safe_get(form_obj, "Controls")
    if controls is None:
        return nodes, edges

    # Debug: log all control names + types so subform type integers are visible
    ctrl_summary = []
    for i in range(_safe_get(controls, "Count", 0)):
        try:
            ctrl = controls(i)
            ctrl_summary.append((_safe_get(ctrl, "Name", f"<{i}>"), _safe_get(ctrl, "ControlType")))
        except Exception:
            continue
    logging.debug("Form %r controls: %s", form_name, ctrl_summary)

    for i in range(_safe_get(controls, "Count", 0)):
        try:
            ctrl = controls(i)
        except Exception:
            continue

        if _safe_get(ctrl, "ControlType", 0) != _SUBFORM_CONTROL_TYPE:
            continue

        ctrl_name = _safe_get(ctrl, "Name", "")
        source_object = _safe_get(ctrl, "SourceObject", "") or ""

        if not source_object:
            continue

        sub_name = source_object.removeprefix("Form.")

        if sub_name in visited:
            continue

        # Access subform control exposes the embedded form via .Form —
        # no DoCmd.OpenForm needed, no design-view open required.
        sub_form_obj = _safe_get(ctrl, "Form")
        if sub_form_obj is None:
            continue

        child_nodes, child_edges = extract_subform_hierarchy(
            form_obj=sub_form_obj,
            form_name=sub_name,
            builder=builder,
            depth=depth + 1,
            parent={"form_id": form_id, "control_name": ctrl_name},
            visited=visited,
        )
        nodes.extend(child_nodes)
        edges.extend(child_edges)

    return nodes, edges
