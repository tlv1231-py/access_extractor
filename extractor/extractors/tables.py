import pythoncom

from extractor.extractors.base import BaseExtractor
from extractor.graph.edges import Edge
from extractor.graph.nodes import Node, NodeKind


class TableExtractor(BaseExtractor):
    def extract(self) -> tuple[list[Node], list[Edge]]:
        nodes = []
        db = self.app.CurrentDb()

        table_defs = db.TableDefs
        for i in range(table_defs.Count):
            table_def = table_defs(i)
            name = self.safe_get(table_def, "Name", "")

            if not name or name.startswith("MSys") or name.startswith("~"):
                continue

            node = Node(
                id=f"table:{name}",
                kind=NodeKind.Table,
                name=name,
                properties={
                    "fields": self._extract_fields(table_def),
                    "record_count": self._get_record_count(db, name),
                },
            )
            nodes.append(node)

        return nodes, []

    def _extract_fields(self, table_def) -> list[dict]:
        fields = []
        field_defs = self.safe_get(table_def, "Fields")
        if field_defs is None:
            return fields

        for i in range(self.safe_get(field_defs, "Count", 0)):
            try:
                f = field_defs(i)
                fields.append({
                    "name": self.safe_get(f, "Name", ""),
                    "type": self.safe_get(f, "Type"),
                    "size": self.safe_get(f, "Size"),
                })
            except pythoncom.com_error:
                continue

        return fields

    def _get_record_count(self, db, table_name: str) -> int | None:
        try:
            rs = db.OpenRecordset(f"SELECT COUNT(*) FROM [{table_name}]")
            count = rs.Fields(0).Value
            rs.Close()
            return count
        except pythoncom.com_error:
            return None
