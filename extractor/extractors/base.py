from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import pythoncom

from extractor.graph.nodes import Node
from extractor.graph.edges import Edge

if TYPE_CHECKING:
    from extractor.graph.builder import GraphBuilder


class BaseExtractor(ABC):
    def __init__(self, app, builder: "GraphBuilder") -> None:
        self.app = app
        self.builder = builder

    @abstractmethod
    def extract(self) -> tuple[list[Node], list[Edge]]:
        ...

    def safe_get(self, obj, attr: str, default=None):
        try:
            return getattr(obj, attr)
        except pythoncom.com_error:
            return default
