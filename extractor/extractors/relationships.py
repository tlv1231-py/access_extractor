import pythoncom

from extractor.extractors.base import BaseExtractor
from extractor.graph.edges import Edge, EdgeKind
from extractor.graph.nodes import Node

# DAO Relation.Attributes bit flags
_DONT_ENFORCE   = 2
_CASCADE_UPDATE = 256
_CASCADE_DELETE = 4096


class RelationshipExtractor(BaseExtractor):
    def extract(self) -> tuple[list[Node], list[Edge]]:
        edges = []
        db = self.app.CurrentDb()

        relations = db.Relations
        for i in range(relations.Count):
            try:
                rel = relations(i)
                primary_table = self.safe_get(rel, "Table", "")
                foreign_table = self.safe_get(rel, "ForeignTable", "")

                if not primary_table or not foreign_table:
                    continue

                src_id = f"table:{foreign_table}"
                dst_id = f"table:{primary_table}"

                if not self.builder.has_node(src_id) or not self.builder.has_node(dst_id):
                    continue

                attrs = self.safe_get(rel, "Attributes", 0)

                edges.append(Edge(
                    src=src_id,
                    dst=dst_id,
                    kind=EdgeKind.DEPENDS_ON,
                    properties={
                        "name": self.safe_get(rel, "Name", ""),
                        "foreign_table": foreign_table,
                        "primary_table": primary_table,
                        "join_fields": self._extract_join_fields(rel),
                        "enforced": (attrs & _DONT_ENFORCE) == 0,
                        "cascade_update": bool(attrs & _CASCADE_UPDATE),
                        "cascade_delete": bool(attrs & _CASCADE_DELETE),
                    },
                ))
            except pythoncom.com_error:
                continue

        return [], edges

    def _extract_join_fields(self, rel) -> list[dict]:
        join_fields = []
        fields = self.safe_get(rel, "Fields")
        if fields is None:
            return join_fields

        for i in range(self.safe_get(fields, "Count", 0)):
            try:
                f = fields(i)
                join_fields.append({
                    "foreign_field": self.safe_get(f, "Name", ""),
                    "primary_field": self.safe_get(f, "ForeignName", ""),
                })
            except pythoncom.com_error:
                continue

        return join_fields
