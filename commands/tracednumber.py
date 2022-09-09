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
    value: float | int


class FactOrAss(TypedDict):
    fact_or_ass: str
    value: float | int


class NameTrace(TypedDict):
    name: str


class DefTrace(TypedDict):
    def_name: NameTrace
    trace: TRACE


class BinaryTrace(TypedDict):
    binary: Literal["+", "-", "*", "/"]
    a: TRACE
    b: TRACE
    value: float | int


class UnaryTrace(TypedDict):
    unary: Literal["+", "-"]
    a: TRACE


def literal(v: int | float) -> TRACE:
    return v


def data(source: str, key: str, attr: str, value: float | int) -> TRACE:
    return {"source": source, "key": key, "attr": attr, "value": value}


def fact_or_ass(n: str, value: float | int) -> TRACE:
    return {"fact_or_ass": n, "value": value}


def _replace_name_defs_by_names(trace: TRACE) -> TRACE:
    match trace:
        case {"binary": op, "a": a, "b": b, "value": v}:
            return {
                "binary": op,
                "a": _replace_name_defs_by_names(a),
                "b": _replace_name_defs_by_names(b),
                "value": v,
            }
        case {"unary": op, "a": a}:
            return {"unary": op, "a": _replace_name_defs_by_names(a)}
        case int() | float():
            return trace
        case {"def_name": ({"name": n} as name), "trace": t}:
            # Names we could not resolve we replace by their expression
            if n.startswith("?"):
                return _replace_name_defs_by_names(t)
            else:
                return name
        case {"source": _, "key": _, "attr": _, "value": _}:
            return trace
        case {"fact_or_ass": _, "value": _}:
            return trace
        case _:
            return trace


def def_name(n: str, trace: TRACE) -> DefTrace:
    return {"def_name": {"name": n}, "trace": trace}


def binary(
    value: float | int, op: Literal["+", "-", "*", "/"], a: TRACE, b: TRACE
) -> TRACE:
    return {"binary": op, "a": a, "b": b, "value": value}


def unary(op: Literal["+", "-"], a: TRACE) -> TRACE:
    return {"unary": op, "a": a}


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
        if isinstance(v, TracedNumber):
            return v
        else:
            return cls(v, literal(v))

    @classmethod
    def data(
        cls, v: Union["TracedNumber", float, int], source: str, key: str, attr: str
    ):
        if isinstance(v, TracedNumber):
            return cls(v.value, data(source, key, attr, v.value))
        else:
            return cls(v, data(source, key, attr, v))

    @classmethod
    def fact_or_ass(cls, n: str, v: float | int):
        return cls(v, fact_or_ass(n, v))

    def binop(
        self,
        op: Literal["+", "-", "*", "/"],
        other: Union["TracedNumber", float, int],
        f: Callable[[int | float, int | float], int | float],
    ) -> "TracedNumber":
        other = self.lift(other)
        value = f(self.value, other.value)
        return TracedNumber(
            value,
            trace=binary(value=value, op=op, a=self.trace, b=other.trace),
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


RESULT_DICTIONARY = dict[
    str, Union[int, None, float, TracedNumber, "RESULT_DICTIONARY"]
]

JSON_RESULT_DICTIONARY = dict[
    str, Union[int, float, None, TracedNumber, ValueWithTrace, "JSON_RESULT_DICTIONARY"]
]


def set_names(r: RESULT_DICTIONARY, path: list[str] = []) -> None:
    """For all name definitions at the toplevel of a tracednumber, set their name to
    the path to that traced number in the tree.  Unless the name is already set.
    This is done by side effect and relies on sharing for the proper effect.
    """

    def helper(
        path: list[str],
        node: Union[int, float, None, "TracedNumber", "RESULT_DICTIONARY"],
    ) -> None:
        match node:
            case TracedNumber():
                match node.trace:
                    case {"def_name": ({"name": str(n)} as name), "trace": _}:
                        if n.startswith("?"):
                            name["name"] = ".".join(path)
                    case _:
                        pass
            case int() | float() | None:
                pass
            case dict():
                return set_names(node, path)

    for k, v in r.items():
        helper(path + [k], v)


def finalize_traces_in_result(r: RESULT_DICTIONARY, path: list[str] = []) -> None:
    """Finalize the traces.  This does several things:
    1. We set the names in name definitions for things reachable by following the result tree. (e.g. r18.r.CO2e_combustion_based)
    2. We replace all traced numbers by a TracedValue
    3. We replace the toplevel name definitions by their trace
    4. We replace all other name definitions by either
        4.1 their name if the name was resolved in 1
        4.2 the trace if it wasn't (this can for example happen for intermediate result dictionaries like
            the sum of several Transport).
    """
    set_names(r)

    def replace_definitions(r: JSON_RESULT_DICTIONARY, path: list[str] = []) -> None:
        for k, v in r.items():
            match v:
                case TracedNumber() as tn:
                    match tn.trace:
                        case {"def_name": _, "trace": t}:
                            r[k] = {
                                "value": tn.value,
                                "trace": _replace_name_defs_by_names(t),
                            }

                        case _:
                            r[k] = {
                                "value": tn.value,
                                "trace": _replace_name_defs_by_names(tn.trace),
                            }
                    assert not isinstance(r[k], TracedNumber)
                case int() | float() | None:
                    pass
                case {"value": _, "trace": _}:
                    pass
                case dict():
                    replace_definitions(v, path + [k])
                case _:

                    # Already replaced
                    pass

    replace_definitions(r)  # type: ignore (We are converting RESULT_DICTIONARY into JSON_RESULT_DICTIONARY in place here)
