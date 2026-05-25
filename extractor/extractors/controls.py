import pythoncom

from extractor.extractors.base import BaseExtractor
from extractor.graph.edges import Edge, EdgeKind
from extractor.graph.nodes import Node, NodeKind

_CONTROL_TYPES: dict[int, str] = {
    100: "TextBox",
    101: "Label",
    102: "Rectangle",
    104: "CommandButton",
    106: "ComboBox",
    107: "ListBox",
    109: "Checkbox",
    110: "OptionButton",
    112: "Subform",
    114: "TabControl",
    118: "Image",
}

_EVENT_PROPS = (
    "OnClick", "OnDblClick", "OnChange",
    "AfterUpdate", "BeforeUpdate", "OnEnter", "OnExit",
    "OnGotFocus", "OnLostFocus", "OnKeyDown", "OnKeyUp",
    "OnLoad", "OnCurrent", "OnOpen", "OnClose", "OnTimer", "OnDirty",
)


class ControlExtractor(BaseExtractor):
    def __init__(self, app, builder, form, parent_node_id: str) -> None:
        super().__init__(app, builder)
        self.form = form
        self.parent_node_id = parent_node_id
        self._form_name = parent_node_id.split(":", 1)[-1]

    def extract(self) -> tuple[list[Node], list[Edge]]:
        nodes: list[Node] = []
        edges: list[Edge] = []

        controls = self.safe_get(self.form, "Controls")
        if controls is None:
            return nodes, edges

        for i in range(self.safe_get(controls, "Count", 0)):
            try:
                ctrl = controls(i)
            except pythoncom.com_error:
                continue

            name = self.safe_get(ctrl, "Name", "")
            if not name:
                continue

            node_id = f"ctrl:{self._form_name}.{name}"
            raw_type = self.safe_get(ctrl, "ControlType", 0)

            try:
                control_source = ctrl.ControlSource
            except Exception:
                control_source = None

            try:
                row_source = ctrl.RowSource
            except Exception:
                row_source = None

            try:
                visible = ctrl.Visible
            except Exception:
                visible = None

            try:
                enabled = ctrl.Enabled
            except Exception:
                enabled = None

            try:
                tab_index = ctrl.TabIndex
            except Exception:
                tab_index = None

            try:
                left = ctrl.Left
            except Exception:
                left = None

            try:
                top = ctrl.Top
            except Exception:
                top = None

            try:
                width = ctrl.Width
            except Exception:
                width = None

            try:
                height = ctrl.Height
            except Exception:
                height = None

            node = Node(
                id=node_id,
                kind=NodeKind.Control,
                name=name,
                properties={
                    "control_type": _CONTROL_TYPES.get(raw_type, str(raw_type)),
                    "control_source": control_source,
                    "row_source": row_source,
                    "visible": visible,
                    "enabled": enabled,
                    "tab_index": tab_index,
                    "left": left,
                    "top": top,
                    "width": width,
                    "height": height,
                    "events": self._extract_events(ctrl),
                },
            )
            nodes.append(node)
            edges.append(Edge(
                src=self.parent_node_id,
                dst=node_id,
                kind=EdgeKind.CONTAINS,
            ))

        return nodes, edges

    def _extract_events(self, ctrl) -> dict[str, str]:
        events: dict[str, str] = {}
        for prop in _EVENT_PROPS:
            try:
                val = getattr(ctrl, prop)
            except Exception:
                continue
            if val:
                events[prop] = val
        return events
