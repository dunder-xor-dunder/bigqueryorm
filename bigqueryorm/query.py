from enum import Enum
from typing import Dict, Any


class Operator(Enum):
    EQ = "="
    NE = "!="
    GTE = ">="
    LTE = "<="
    GT = ">"
    LT = "<"
    IN = "IN"
    LIKE = "LIKE"


class Table:

    def __init__(self, name: str):
        split = name.split(".")
        if len(split) == 2:
            self.project, self.dataset, self.table = None, *split
        elif len(split) == 3:
            self.project, self.dataset, self.table = split


class Row:

    @classmethod
    def _columns(cls) -> Dict[str, Any]:
        return cls.__annotations__
