from extractor.graph.edges import Edge, EdgeKind
from extractor.graph.nodes import Node, NodeKind


class GraphBuilder:
    def __init__(self) -> None:
        self.nodes: dict[str, Node] = {}
        self.edges: list[Edge] = []

    # ------------------------------------------------------------------
    # Mutation

    def add_node(self, node: Node) -> None:
        if node.id not in self.nodes:
            self.nodes[node.id] = node

    def add_edge(self, edge: Edge) -> None:
        self.edges.append(edge)

    def add(self, nodes: list[Node], edges: list[Edge]) -> None:
        for node in nodes:
            self.add_node(node)
        for edge in edges:
            self.add_edge(edge)

    # ------------------------------------------------------------------
    # Lookup

    def has_node(self, node_id: str) -> bool:
        return node_id in self.nodes

    # ------------------------------------------------------------------
    # Derived views

    def get_module_sources(self) -> dict[str, list[str]]:
        return {
            node.name: node.properties.get("source", "").splitlines()
            for node in self.nodes.values()
            if node.kind == NodeKind.Module
        }

    def build_hierarchy(self) -> dict:
        embedded: set[str] = {
            e.dst for e in self.edges if e.kind == EdgeKind.EMBEDS_SUBFORM
        }

        children_map: dict[str, list[dict]] = {}
        for e in self.edges:
            if e.kind == EdgeKind.EMBEDS_SUBFORM:
                children_map.setdefault(e.src, []).append({
                    "dst": e.dst,
                    "control_name": e.properties.get("control_name"),
                    "depth": e.properties.get("depth", 0),
                })

        def _subtree(form_id: str, depth: int, embedding_control) -> dict:
            return {
                "depth": depth,
                "embedding_control": embedding_control,
                "children": {
                    c["dst"]: _subtree(c["dst"], c["depth"], c["control_name"])
                    for c in children_map.get(form_id, [])
                },
            }

        return {
            node_id: _subtree(node_id, 0, None)
            for node_id, node in self.nodes.items()
            if node.kind == NodeKind.Form and node_id not in embedded
        }

    # ------------------------------------------------------------------
    # Serialization

    def to_dict(self) -> dict:
        return {
            "nodes": [
                {
                    "id": n.id,
                    "kind": n.kind.name,
                    "name": n.name,
                    "properties": n.properties,
                }
                for n in self.nodes.values()
            ],
            "edges": [
                {
                    "src": e.src,
                    "dst": e.dst,
                    "kind": e.kind.name,
                    "properties": e.properties,
                }
                for e in self.edges
            ],
            "hierarchy": self.build_hierarchy(),
        }
