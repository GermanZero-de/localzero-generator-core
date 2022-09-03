from dataclasses import fields, is_dataclass
from typing import Any, Callable
from generatorcore.generator import Result
from generatorcore.refdata import Row


def identity(x: Any):
    return x


def maybe_enable_tracing(args: Any):
    """Enable tracing if trace was given on the commandline.  Should be called before any computation is done!
    Makes the generatorcore use tracednumber to do all calculations.
    Returns a function suitable to convert the resulting "values" to
    json.
    """
    if args.trace:
        return enable_tracing()
    else:
        return identity


def enable_tracing() -> Callable[[Any], Any]:
    # We do this monkey-patching dance here, because we do not want
    # the somewhat hacky tracing code to be part of the normal production
    # calculations.  It's only supposed to be a quick tool for developers
    # the generator core -- who hopefully understand the tools limitations.

    from . import tracednumber

    def traced_max(*args, **kwargs):
        return tracednumber.TracedNumber.max(__builtins__.max(*args, **kwargs), *args)

    global max
    max = traced_max

    # First patch the lookup of inputs
    original_float = Row.float  # type: ignore

    def traced_float(self: Row[str], attr: str):
        v = original_float(self, attr)
        # make facts and assumptions prettier
        if self.dataset in ["facts", "assumptions"] and attr == "value":
            return tracednumber.TracedNumber.fact_or_ass(str(self.key_value), v)
        else:
            return tracednumber.TracedNumber.data(v, self.dataset, self.key_value, attr)

    Row.float = traced_float  # type: ignore

    # Now also replace already computed and stored values from previous sectors by their value
    def make_traced_getattribute(path: str):
        def traced_getattribute(self: Any, name: str):
            value = object.__getattribute__(self, name)
            if isinstance(value, (float, int, tracednumber.TracedNumber)):
                return tracednumber.TracedNumber.def_name(f"{path}.{name}", value)
            else:
                return value

        return traced_getattribute

    def add_tracing(path: list[str], t: type):
        for fld in fields(t):
            if is_dataclass(fld.type):
                add_tracing(path + [fld.name], fld.type)
                fld.type.__getattribute__ = make_traced_getattribute(
                    ".".join(path + [fld.name])
                )

    add_tracing([], Result)

    return tracednumber.TracedNumber.to_json
