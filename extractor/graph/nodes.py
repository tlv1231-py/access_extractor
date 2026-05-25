from dataclasses import dataclass, field
from enum import Enum, auto


class NodeKind(Enum):
    Form = auto()
    Subform = auto()
    Control = auto()
    Query = auto()
    Table = auto()
    Module = auto()
    Macro = auto()
    Event = auto()
    Procedure = auto()


@dataclass
class Node:
    id: str
    kind: NodeKind
    name: str
    properties: dict = field(default_factory=dict)
