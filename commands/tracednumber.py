# pyright: strict

# A tracednumber is a number that also stores a trace of the computation that
# created the number.  Done by overriding all the math operations.
# For the generator core this leads to surprisingly good traces as
# we largely do not use for loops or ifs to decide how to do the computation.
# Or to say it differently all we really have is just a collection of formulas
from typing import Literal, Union, Callable, TypedDict


# Traces will be returned as values that python's json module
# can immediately convert.
TRACE = Union[
    int,
    float,
    "DataTrace",
    "FactOrAss",
    "NameTrace",
    "DefTrace",
    "BinaryTrace",
    "UnaryTrace",
]


class ValueWithTrace(TypedDict):
    value: float | int
    trace: TRACE


class DataTrace(TypedDict):
    source: str
    key: str | int
    attr: str


class FactOrAss(TypedDict):
    fact_or_ass: str


class NameTrace(TypedDict):
    name: str


class DefTrace(TypedDict):
    def_name: str
    trace: TRACE


class BinaryTrace(TypedDict):
    binary: Literal["+", "-", "*", "/"]
    a: TRACE
    b: TRACE


class UnaryTrace(TypedDict):
    unary: Literal["+", "-"]
    a: TRACE


def literal(v: int | float) -> TRACE:
    return v


def data(source: str, key: str, attr: str) -> TRACE:
    return {"source": source, "key": key, "attr": attr}


def fact_or_ass(n: str) -> TRACE:
    return {"fact_or_ass": n}


def name(n: str) -> TRACE:
    return {"name": n}


def use_trace(trace: TRACE) -> TRACE:
    """Everywhere a trace is used we want to convert definitions into names.
    So that in the end only the toplevel assignments are definitions.
    """
    match trace:
        case {"def_name": n, "trace": _}:
            return name(n)
        case _:
            return trace


def unpack_def(trace: TRACE) -> TRACE:
    match trace:
        case {"def_name": _, "trace": t}:
            return t
        case _:
            return trace


def def_name(n: str, trace: TRACE) -> TRACE:
    return {"def_name": n, "trace": use_trace(trace)}


def binary(op: Literal["+", "-", "*", "/"], a: TRACE, b: TRACE) -> TRACE:
    return {"binary": op, "a": use_trace(a), "b": use_trace(b)}


def unary(op: Literal["+", "-"], a: TRACE) -> TRACE:
    return {"unary": op, "a": use_trace(a)}


class TracedNumber:
    trace: TRACE
    value: float | int

    def __init__(
        self,
        v: Union[float, int],
        trace: TRACE,
    ):
        self.value = v
        self.trace = trace

    @classmethod
    def lift(cls, v: Union["TracedNumber", float, int]) -> "TracedNumber":
        if isinstance(v, (float, int)):
            return cls(v, literal(v))
        else:
            return v

    @classmethod
    def data(
        cls, v: Union["TracedNumber", float, int], source: str, key: str, attr: str
    ):
        if isinstance(v, (float, int)):
            return cls(v, data(source, key, attr))
        else:
            return cls(v.value, data(source, key, attr))

    @classmethod
    def fact_or_ass(cls, n: str, v: float | int):
        return cls(v, fact_or_ass(n))

    @classmethod
    def def_name(cls, n: str, v: Union["TracedNumber", float, int]):
        if isinstance(v, (float, int)):
            return cls(v, def_name(n, literal(v)))
        else:
            return cls(v.value, def_name(n, v.trace))

    def binop(
        self,
        op: Literal["+", "-", "*", "/"],
        other: Union["TracedNumber", float, int],
        f: Callable[[int | float, int | float], int | float],
    ) -> "TracedNumber":
        other = self.lift(other)
        return TracedNumber(
            f(self.value, other.value),
            trace=binary(op=op, a=self.trace, b=other.trace),
        )

    def is_integer(self) -> bool:
        if isinstance(self.value, int):
            return True
        else:
            return self.value.is_integer()

    def __float__(self) -> float:
        return float(self.value)

    def __add__(self, other: Union["TracedNumber", float, int]) -> "TracedNumber":
        return self.binop("+", other, lambda a, b: a + b)

    def __radd__(self, other: Union["TracedNumber", float, int]) -> "TracedNumber":
        return self.lift(other) + self

    def __sub__(self, other: Union["TracedNumber", float, int]) -> "TracedNumber":
        return self.binop("-", other, lambda a, b: a - b)

    def __rsub__(self, other: Union["TracedNumber", float, int]) -> "TracedNumber":
        return self.lift(other) - self

    def __mul__(self, other: Union["TracedNumber", float, int]) -> "TracedNumber":
        return self.binop("*", other, lambda a, b: a * b)

    def __rmul__(self, other: Union["TracedNumber", float, int]) -> "TracedNumber":
        return self.lift(other) * self

    def __truediv__(self, other: Union["TracedNumber", float, int]) -> "TracedNumber":
        return self.binop("/", other, lambda a, b: a / b)

    def __rtruediv__(self, other: Union["TracedNumber", float, int]) -> "TracedNumber":
        return self.lift(other) / self

    def __gt__(self, other: Union["TracedNumber", float, int]) -> bool:
        if isinstance(other, self.__class__):
            return self.value > other.value
        else:
            return self.value > other

    def __lt__(self, other: Union["TracedNumber", float, int]) -> bool:
        if isinstance(other, self.__class__):
            return self.value < other.value
        else:
            return self.value < other  # type: ignore TODO: Figure out why the type checker does not like this but likes the above

    def __le__(self, other: Union["TracedNumber", float, int]) -> bool:
        if isinstance(other, self.__class__):
            return self.value <= other.value
        else:
            return self.value <= other

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.value == other.value
        else:
            return self.value == other

    def __ne__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.value != other.value
        else:
            return self.value != other

    def __str__(self) -> str:
        return f"{self.value} : {self.trace}"

    def __neg__(self) -> "TracedNumber":
        return self.__class__(-self.value, trace=unary("-", self.trace))

    def to_json(self) -> ValueWithTrace:
        return {"value": self.value, "trace": unpack_def(self.trace)}
