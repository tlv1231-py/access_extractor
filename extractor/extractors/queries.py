import pythoncom

from extractor.extractors.base import BaseExtractor
from extractor.graph.edges import Edge
from extractor.graph.nodes import Node, NodeKind

# DAO QueryDef.Type constants
_QUERY_TYPE_MAP: dict[int, str] = {
    0: "select",
    16: "crosstab",
    32: "action",        # DELETE
    48: "action",        # UPDATE
    64: "action",        # APPEND
    80: "action",        # MAKE-TABLE
    96: "datadefinition",
    112: "passthrough",
    128: "union",
}


class QueryExtractor(BaseExtractor):
    def extract(self) -> tuple[list[Node], list[Edge]]:
        nodes = []
        db = self.app.CurrentDb()

        query_defs = db.QueryDefs
        for i in range(query_defs.Count):
            qd = query_defs(i)
            name = self.safe_get(qd, "Name", "")

            if not name or name.startswith("~"):
                continue

            raw_type = self.safe_get(qd, "Type", 0)
            node = Node(
                id=f"query:{name}",
                kind=NodeKind.Query,
                name=name,
                properties={
                    "sql": self.safe_get(qd, "SQL", ""),
                    "type": _QUERY_TYPE_MAP.get(raw_type, "select"),
                    "parameters": self._extract_parameters(qd),
                },
            )
            nodes.append(node)

        return nodes, []

    def _extract_parameters(self, qd) -> list[dict]:
        params = []
        param_defs = self.safe_get(qd, "Parameters")
        if param_defs is None:
            return params

        for i in range(self.safe_get(param_defs, "Count", 0)):
            try:
                p = param_defs(i)
                params.append({
                    "name": self.safe_get(p, "Name", ""),
                    "type": self.safe_get(p, "Type"),
                })
            except pythoncom.com_error:
                continue

        return params
