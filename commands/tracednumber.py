# pyright: strict

# A tracednumber is a number that also stores a trace of the computation that
# created the number.  Done by overriding all the math operations.
# For the generator core this leads to surprisingly good traces as
# we largely do not use for loops or ifs to decide how to do the computation.
# Or to say it differently all we really have is just a collection of formulas
from typing import Literal, Union, Callable


# A trace is either, one of the atoms:
# a literal number that occurred as is in the source
# int|float
# or named expression
# { name: "name", trace: <trace> }
# or a binary operation
# { op: "+"|"-"|"/"|"*", a: <trace>, b: <trace> }
# or a unary operation
# { op: "+"|"-"|"/"|"*", a: <trace>}

TRACE = Union[int, float, dict[str, Union[str, "TRACE"]]]


def literal(v: int | float) -> TRACE:
    return v


def named(name: str, t: TRACE) -> TRACE:
    return {"name": name, "trace": t}


def binary(op: Literal["+", "-", "*", "/"], a: TRACE, b: TRACE) -> TRACE:
    return {"op": op, "a": a, "b": b}


def unary(op: Literal["+", "-"], a: TRACE) -> TRACE:
    return {"op": op, "a": a}


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
    def named(cls, v: Union["TracedNumber", float, int], name: str):
        if isinstance(v, (float, int)):
            return cls(v, named(name, literal(v)))
        else:
            return cls(v.value, named(name, v.trace))

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

    def to_json(self) -> TRACE:
        return {"value": self.value, "trace": self.trace}
