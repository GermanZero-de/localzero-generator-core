from dataclasses import fields, is_dataclass
from typing import Any, Callable
from lzcv.generator import Result
from lzcv.generator.refdata import Row


def identity(x: Any):
    return x


def maybe_enable_tracing(args: Any) -> Callable[[Any], Any]:
    """Enable tracing if trace was given on the commandline.  Should be called before any computation is done!
    Makes the generatorcore use tracednumber to do all calculations.
    Call the returned function on the result of Result.result_dict or asdict(entries) to
    finalize the traces for output to JSON.  The returned function is a no-op if tracing
    wasn't enabled.
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

    # Now make sure that whenever a value stored in a component of the final
    # result type is used, the trace contains a def_name and that the same
    # def_name is used when the same component is used multiple times.
    def traced_getattribute(self: Any, name: str):
        value = object.__getattribute__(self, name)
        if isinstance(value, (float, int, tracednumber.TracedNumber)):
            traced_value = tracednumber.TracedNumber.lift(value)
            if not hasattr(self, "__name_defs"):
                self.__name_defs = {}
            if name not in self.__name_defs:
                name_def = tracednumber.def_name("?." + name, traced_value.trace)
                self.__name_defs[name] = name_def

            return tracednumber.TracedNumber(
                traced_value.value, trace=self.__name_defs[name]
            )
        else:
            return value

    def prepare_tracing_of_fields(t: type):
        if is_dataclass(t):
            setattr(t, "__getattribute__", traced_getattribute)
            for fld in fields(t):
                prepare_tracing_of_fields(fld.type)

    prepare_tracing_of_fields(Result)

    def convert(x):
        tracednumber.finalize_traces_in_result(x)
        return x

    return convert
