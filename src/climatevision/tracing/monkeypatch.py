from dataclasses import fields, is_dataclass
from typing import Any, Callable, TypeVar

from ..generator import Result
from ..generator.refdata import Row

original_row_float = Row.float


def identity(x: Any):
    return x


T = TypeVar("T")


def with_tracing_enabled(f: Callable[[], T]) -> T:
    """Enable tracing and run f.  f should return a json ready object, that is
    the return value of Result.result_dict, or asdict(entries)
    """
    patch_result = enable_tracing()
    try:
        return patch_result(f())
    finally:
        disable_tracing()


def with_tracing(enabled: bool, f: Callable[[], T]) -> T:
    if enabled:
        return with_tracing_enabled(f)
    else:
        return f()


def maybe_enable_tracing(args: Any) -> Callable[[Any], Any]:
    """Enable tracing if trace was given on the commandline.  Should be called before any computation is done!
    Makes the generatorcore use tracing.number to do all calculations.
    Call the returned function on the result of Result.result_dict or asdict(entries) to
    finalize the traces for output to JSON.  The returned function is a no-op if tracing
    wasn't enabled.
    """
    if args.trace:
        return enable_tracing()
    else:
        return identity


def recursively_patch_getattribute_on_dataclasses(
    t: type, new_getattribute: Callable[[object, str], object] | None
) -> None:
    tracing_enabled_marker = "_has_tracing_enabled"
    if is_dataclass(t):
        if new_getattribute is not None:
            setattr(t, tracing_enabled_marker, True)
            setattr(t, "__getattribute__", new_getattribute)
        else:
            if getattr(t, tracing_enabled_marker, False):
                setattr(t, tracing_enabled_marker, False)
                delattr(t, "__getattribute__")

        for fld in fields(t):
            recursively_patch_getattribute_on_dataclasses(fld.type, new_getattribute)


def disable_tracing() -> None:
    recursively_patch_getattribute_on_dataclasses(Result, None)
    Row.float = original_row_float


def enable_tracing() -> Callable[[Any], Any]:
    # We do this monkey-patching dance here, because we do not want
    # the somewhat hacky tracing code to be part of the normal production
    # calculations.  It's only supposed to be a quick tool for developers
    # the generator core -- who hopefully understand the tools limitations.
    from . import number

    def traced_float(self: Row[str], attr: str):
        v = original_row_float(self, attr)
        # make facts and assumptions prettier
        if self.dataset in ["facts", "assumptions"] and attr == "value":
            return number.TracedNumber.fact_or_ass(str(self.key_value), v)
        else:
            return number.TracedNumber.data(v, self.dataset, self.key_value, attr)

    Row.float = traced_float  # type: ignore (pyright does not know that tracednumber can be used instead of float)

    # Now make sure that whenever a value stored in a component of the final
    # result type is used, the trace contains a def_name and that the same
    # def_name is used when the same component is used multiple times.
    def traced_getattribute(self: Any, name: str):
        value = object.__getattribute__(self, name)
        if isinstance(value, (float, int, number.TracedNumber)):
            traced_value = number.TracedNumber.lift(value)
            if not hasattr(self, "__name_defs"):
                self.__name_defs = {}
            if name not in self.__name_defs:
                name_def = number.def_name("?." + name, traced_value.trace)
                self.__name_defs[name] = name_def

            return number.TracedNumber(traced_value.value, trace=self.__name_defs[name])
        else:
            return value

    recursively_patch_getattribute_on_dataclasses(Result, traced_getattribute)

    def convert(x):
        number.finalize_traces_in_result(x)
        return x

    return convert
