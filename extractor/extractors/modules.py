import pythoncom

from extractor.extractors.base import BaseExtractor
from extractor.graph.edges import Edge
from extractor.graph.nodes import Node, NodeKind

# Access module type constants
_AC_STANDARD_MODULE = 0
_AC_CLASS_MODULE    = 1


class ModuleExtractor(BaseExtractor):
    def extract(self) -> tuple[list[Node], list[Edge]]:
        nodes = []
        all_modules = self.app.CurrentProject.AllModules

        for i in range(all_modules.Count):
            access_obj = all_modules(i)
            name = self.safe_get(access_obj, "Name", "")
            if not name:
                continue

            raw_type = self.safe_get(access_obj, "Type", _AC_STANDARD_MODULE)
            module_type = "class" if raw_type == _AC_CLASS_MODULE else "standard"

            source, line_count = self._read_source(name)

            nodes.append(Node(
                id=f"module:{name}",
                kind=NodeKind.Module,
                name=name,
                properties={
                    "module_type": module_type,
                    "line_count": line_count,
                    "source": source,
                },
            ))

        return nodes, []

    def _read_source(self, name: str) -> tuple[str, int]:
        try:
            mod = self.app.Modules(name)
            line_count = self.safe_get(mod, "CountOfLines", 0)
            source = mod.Lines(1, line_count) if line_count > 0 else ""
            return source, line_count
        except pythoncom.com_error:
            return "", 0
