# pyright: strict reportMissingTypeStubs=true
import dataclasses
from typing import Callable, Any

import jsonrpcserver

from climatevision import generator
from climatevision.generator import Inputs, RefData


class GeneratorRpcs:
    rd: RefData
    finalize_traces_if_enabled: Callable[[Any], Any]

    def __init__(self, rd: RefData, finalize_traces_if_enabled: Callable[[Any], Any]):
        self.rd = rd
        self.finalize_traces_if_enabled = finalize_traces_if_enabled

    def list_ags(self) -> jsonrpcserver.Result:
        def guess_short_name_from_description(d: str) -> str:
            return d.split(",", maxsplit=1)[0].split("(", maxsplit=1)[0]

        # TODO: Add Federal State
        all_ags = self.rd.ags_master()
        result = [
            {
                "ags": ags,
                "desc": description,
                "short": guess_short_name_from_description(description),
            }
            for (ags, description) in all_ags.items()
        ]
        return jsonrpcserver.Success(result)

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
        inputs = Inputs(
            facts_and_assumptions=self.rd.facts_and_assumptions(), entries=entries
        )
        g = generator.calculate(inputs)
        return jsonrpcserver.Success(self.finalize_traces_if_enabled(g.result_dict()))

    def methods(self) -> jsonrpcserver.methods.Methods:
        return {
            "make-entries": self.make_entries,
            "list-ags": self.list_ags,
            "calculate": self.calculate,
        }
