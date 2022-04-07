"""Module inputs -- the inputs that are available to every calculation.

In a first step the generator computes various stats for the municipality we are interested in.
We call those values entries. These are all derived from the reference data (see refdata).

Then those values can be overriden by the user (as the municipality might have more up to date
data available).

To make that work the subsequent calculations do not have access to all of the refdata.
Concretely they only use the facts and assumptions from refdata and the entries as mentioned
above.  We call that triple the `Inputs`.

Note: Of course some of the calculation use results from previous steps of the
calculation (most famously electricity basically depends on everything else).
"""
from . import refdata
from .makeentries import Entries


class Inputs:
    def __init__(
        self,
        facts_and_assumptions: refdata.FactsAndAssumptions,
        entries: Entries,
    ):
        self._facts_and_assumptions = facts_and_assumptions
        self.entries = entries

    def fact(self, keyname: str) -> float:
        """Statistics about the past. Must be able to give a source for each fact."""
        return self._facts_and_assumptions.fact(keyname)

    def ass(self, keyname: str) -> float:
        """Similar to fact, but these try to describe the future. And are therefore based on various assumptions."""
        return self._facts_and_assumptions.ass(keyname)

    #Leon-Function
    def return_facts(self):
        return self._facts_and_assumptions