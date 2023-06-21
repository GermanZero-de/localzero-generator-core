# pyright: basic
import dataclasses
from typing import Callable

import jsonrpcserver

from .. import generator
from ..tracing import with_tracing
from . import overridables


RPC_FAILED_ERROR_CODE = 42


class GeneratorRpcs:
    rd: generator.RefData

    def __init__(self, rd: generator.RefData):
        self.rd = rd

    def wrap_result(self, f: Callable[[], object]) -> jsonrpcserver.Result:
        try:
            result = jsonrpcserver.Success(f())
        except Exception as e:
            result = jsonrpcserver.Error(RPC_FAILED_ERROR_CODE, str(e))
        return result

    def do_list_ags(self):
        def guess_short_name_from_description(d: str) -> str:
            return d.split(",", maxsplit=1)[0].split("(", maxsplit=1)[0]

        # TODO: Add Federal State
        all_ags = self.rd.ags_master()
        return [
            {
                "ags": ags,
                "desc": description,
                "short": guess_short_name_from_description(description),
            }
            for (ags, description) in all_ags.items()
        ]

    def list_ags(self) -> jsonrpcserver.Result:
        return self.wrap_result(self.do_list_ags)

    def make_entries(self, ags: str, year: int, trace: bool) -> jsonrpcserver.Result:
        return self.wrap_result(
            lambda: with_tracing(
                enabled=trace,
                f=lambda: dataclasses.asdict(
                    generator.make_entries(self.rd, ags, year)
                ),
            )
        )

    def calculate(
        self, ags: str, year: int, overrides: dict[str, int | float | str], trace: bool
    ) -> jsonrpcserver.Result:
        def calculate():
            defaults = dataclasses.asdict(generator.make_entries(self.rd, ags, year))
            defaults.update(overrides)
            entries = generator.Entries(**defaults)

            if ags == "DG000000":
                entries_germany = entries
            else:
                entries_germany = generator.make_entries(
                    self.rd, ags="DG000000", year=year
                )

            inputs = generator.Inputs(
                facts=self.rd.facts(),
                assumptions=self.rd.assumptions(),
                entries=entries,
            )
            inputs_germany = generator.Inputs(
                facts=self.rd.facts(),
                assumptions=self.rd.assumptions(),
                entries=entries_germany,
            )
            g = generator.calculate(inputs, inputs_germany)
            return g.result_dict()

        return self.wrap_result(lambda: with_tracing(enabled=trace, f=calculate))

    def get_overridables(self, ags: str, year: int) -> jsonrpcserver.Result:
        return self.wrap_result(
            lambda: overridables.sections_with_defaults(self.rd, ags, year)
        )

    def info(self, key: str) -> jsonrpcserver.Result:
        if key.startswith("Fact_"):
            return self.wrap_result(
                lambda: dataclasses.asdict(self.rd.facts().complete_fact(key))
            )
        elif key.startswith("Ass_"):
            return self.wrap_result(
                lambda: dataclasses.asdict(self.rd.assumptions().complete_ass(key))
            )
        else:
            return self.wrap_result(lambda: None)

    def methods(self) -> jsonrpcserver.methods.Methods:
        return {
            "make-entries": self.make_entries,
            "get-overridables": self.get_overridables,
            "list-ags": self.list_ags,
            "calculate": self.calculate,
            "info": self.info,
        }
