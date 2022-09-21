# pyright: strict reportMissingTypeStubs=true
import dataclasses
from typing import Callable, Any

import jsonrpcserver

from .. import generator
from . import overridables


class GeneratorRpcs:
    rd: generator.RefData
    finalize_traces_if_enabled: Callable[[Any], Any]

    def __init__(
        self, rd: generator.RefData, finalize_traces_if_enabled: Callable[[Any], Any]
    ):
        self.rd = rd
        self.finalize_traces_if_enabled = finalize_traces_if_enabled

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
        return jsonrpcserver.Success(self.do_list_ags())

    def make_entries(self, ags: str, year: int) -> jsonrpcserver.Result:
        return jsonrpcserver.Success(
            self.finalize_traces_if_enabled(
                dataclasses.asdict(generator.make_entries(self.rd, ags, year))
            )
        )

    def calculate(
        self, ags: str, year: int, overrides: dict[str, int | float | str]
    ) -> jsonrpcserver.Result:
        defaults = dataclasses.asdict(generator.make_entries(self.rd, ags, year))
        defaults.update(overrides)
        entries = generator.Entries(**defaults)
        inputs = generator.Inputs(
            facts_and_assumptions=self.rd.facts_and_assumptions(), entries=entries
        )
        g = generator.calculate(inputs)
        return jsonrpcserver.Success(self.finalize_traces_if_enabled(g.result_dict()))

    def get_overridables(self, ags: str, year: int) -> jsonrpcserver.Result:
        return jsonrpcserver.Success(
            overridables.sections_with_defaults(self.rd, ags, year)
        )

    def methods(self) -> jsonrpcserver.methods.Methods:
        return {
            "make-entries": self.make_entries,
            "get-overridables": self.get_overridables,
            "list-ags": self.list_ags,
            "calculate": self.calculate,
        }
