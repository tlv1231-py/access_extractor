from dataclasses import dataclass, field
from enum import Enum, auto


class EdgeKind(Enum):
    CONTAINS = auto()
    EMBEDS_SUBFORM = auto()
    EVENT_TRIGGERS = auto()
    EVENT_MODIFIES = auto()
    EVENT_OPENS_FORM = auto()
    EVENT_RUNS_QUERY = auto()
    REFERENCES = auto()
    CALLS = auto()
    DEPENDS_ON = auto()


@dataclass
class Edge:
    src: str
    dst: str
    kind: EdgeKind
    properties: dict = field(default_factory=dict)
