import json
from enum import Enum
from typing import Dict, Any, Tuple, List


class Operator(Enum):
    EQ = "="
    NE = "!="
    GTE = ">="
    LTE = "<="
    GT = ">"
    LT = "<"
    IN = "IN"
    LIKE = "LIKE"


def _split_op(key: str) -> Tuple[str, Operator]:
    *column_names, op = key.split("__")
    if not column_names:
        # like foo="bar", assume EQ
        return [op], Operator.EQ
    try:
        op = Operator[op.upper()]
    except KeyError:
        raise ValueError(f"{op} does not appear to be a valid comparison operator")
    return column_names, op


class _Value:

    def __init__(self, value: Any):
        self.value = value

    def sql(self):
        if isinstance(self.value, (int, float)):
            return str(self.value)
        elif isinstance(self.value, str):
            return json.dumps(self.value)
            """
            val = self.value.replace('"', '\\"')
            return f'"{val}"'
            """
        elif self.value is None:
            return "NULL"
        elif isinstance(self.value, Enum):
            return json.dumps(self.value.value)
        elif isinstance(self.value, (tuple, list, set)):
            json_dump = json.dumps(self.value)[1, -1]
            return f"({json_dump})"
        else:
            return json.dumps(self.value)


class _Comparison:

    def __init__(self, lhs: str, op: Operator, rhs: Any):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    @classmethod
    def _parse(cls, key: str, val: Any):
        column_names, op = _split_op(key)
        return cls(column_names, op, _Value(val))

    def sql(self) -> str:
        col_names = ".".join(self.lhs)
        if self.rhs.value is None:
            if self.op.value is Operator.EQ:
                return f"({col_names} IS NULL"
            elif self.op.value is Operator.NE:
                return f"({col_names} IS NOT NULL"
            else:
                raise ValueError(f"cannot use {self.op.name} with NULL comparison")
        rhs = self.rhs.sql()
        return f"({col_names} {self.op.value} {rhs})"


class Count:
    pass


class _Selection:

    def __init__(self, selection: List[str]):
        self.selection = selection

    def sql(self):
        query = ""
        for sel in self.selection:
            query = f"{query}{sel}"
            if sel is not self.selection[-1]:
                query = f"{query}, "
        return query


class _Query:

    def __init__(
        self,
        limit_=None,
        *,
        table,
        selection,
        filters: List[List[_Comparison]],
    ):
        self.table = table
        self.selection = selection
        self.filters = filters
        self.limit_ = limit_

    def filter(self, **kwargs):
        comparisons = [
            _Comparison._parse(key, val)
            for key, val in kwargs.items()
        ]
        return _Query(
            table=self.table,
            selection=self.selection,
            filters=self.filters + [comparisons],
            limit_=self.limit_,
        )

    def limit(self, value: int):
        if value < 0:
            raise ValueError(f"limit cannot be negative: {value!r}")
        self.limit_ = value
        return self

    def sql(self):
        query = f"SELECT {self.selection.sql()}\n"
        query = f"{query}FROM {self.table.name}\n"
        if self.filters:
            query = f"{query}WHERE ("
        for filter_set in self.filters:
            query = f"{query}("
            for comp in filter_set:
                query = f"{query}{comp.sql()}"
                if comp is not filter_set[-1]:
                    query = f"{query} AND "
            query = f"{query})"
            if filter_set is not self.filters[-1]:
                query = f"{query} AND "
        if self.filters:
            query = f"{query})\n"
        if self.limit:
            query = f"{query}LIMIT {self.limit_}"
        return query


class _Table:

    def __init__(self, name: str, *, row_cls):
        self.selection = _Selection(["*"])
        split = name.split(".")
        if len(split) == 2:
            self.project, self.dataset, self.table = None, *split
        elif len(split) == 3:
            self.project, self.dataset, self.table = split
        else:
            raise ValueError(f"name {name!r} did not describe project.dataset.table")

    def filter(self, **kwargs):
        comparisons = [
            _Comparison._parse(key, val)
            for key, val in kwargs.items()
        ]
        return _Query(
            table=self,
            selection=self.selection,
            filters=[comparisons],
        )

    @property
    def name(self):
        return f"{self.project}.{self.dataset}.{self.table}"


def declare_row(klass) -> type:

    @classmethod
    def _columns(cls) -> Dict[str, Any]:
        return cls.__annotations__

    @classmethod
    def table(cls, name: str) -> _Table:
        return _Table(name, row_cls=cls)

    klass._columns = _columns
    klass.table = table

    return klass
