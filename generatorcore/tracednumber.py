# pyright: strict

from dataclasses import dataclass
from typing import Literal, Union, Callable


@dataclass
class Trace:
    pass

    def level(self) -> int:
        return 0

    def as_op(self, level: int) -> str:
        if self.level() > level:
            return "(" + str(self) + ")"
        else:
            return str(self)


@dataclass
class NumberTrace(Trace):
    num: float | int

    def __str__(self) -> str:
        return str(self.num)


@dataclass
class NamedTrace(Trace):
    name: str

    def __str__(self) -> str:
        return self.name


@dataclass
class BinOpTrace(Trace):
    op: Literal["+", "-", "*", "/"]
    a: Trace
    b: Trace

    def level(self) -> int:
        if self.op == "*" or self.op == "/":
            return 1
        else:
            return 2

    def __str__(self) -> str:
        return (
            self.a.as_op(self.level())
            + " "
            + self.op
            + " "
            + self.b.as_op(self.level())
        )


@dataclass
class UnaryTrace(Trace):
    op: Literal["-", "+"]
    a: Trace

    def level(self):
        return 0

    def __str__(self) -> str:
        return self.op + self.a.as_op(self.level())


class TracedNumber:
    trace: Trace
    value: float | int

    def __init__(self, v: float | int, trace: Trace | str | None = None):
        if trace == None:
            self.trace = NumberTrace(v)
        elif isinstance(trace, str):
            self.trace = NamedTrace(trace)
        else:
            self.trace = trace
        self.value = v

    @classmethod
    def lift(cls, v: Union["TracedNumber", float, int]):
        if isinstance(v, (float, int)):
            return cls(v)
        else:
            return v

    def binop(
        self,
        op: Literal["+", "-", "*", "/"],
        other: Union["TracedNumber", float, int],
        f: Callable[[int | float, int | float], int | float],
    ) -> "TracedNumber":
        if isinstance(other, (float, int)):
            other = TracedNumber(other)
        return TracedNumber(
            f(self.value, other.value),
            trace=BinOpTrace(op=op, a=self.trace, b=other.trace),
        )

    def is_integer(self) -> bool:
        if isinstance(self.value, int):
            return True
        else:
            return self.value.is_integer()

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
            return self.value < other

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
        return TracedNumber(-self.value, trace=UnaryTrace("-", self.trace))

    def to_json(self):
        return {"value": self.value, "trace": str(self.trace)}
