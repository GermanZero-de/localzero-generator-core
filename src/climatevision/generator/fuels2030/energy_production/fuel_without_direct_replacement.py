# pyright: strict

from dataclasses import dataclass

from ...common.co2e_change import CO2eChangeEnergy


@dataclass(kw_only=True)
class FuelWithoutDirectReplacement(CO2eChangeEnergy):
    """This computes the effect on our CO2e and energy budget of us totally stopping
    to produce some fuels without a direct replacement."""

    CO2e_total_2021_estimated: float
    change_CO2e_t: float
    cost_climate_saved: float

    @classmethod
    def calc(cls, energy2018: float) -> "FuelWithoutDirectReplacement":
        # Possible future work marker:
        # We simplified bio{ethonal,diesel,gas} to have 0 emission at
        # production and when burned.  This is not fully correct. But
        # if we didn't do that we would also have to account for growth
        # of the bio component in lulucf.
        return cls(
            change_energy_MWh=-energy2018,
            change_energy_pct=-1,
            CO2e_total_2021_estimated=0,
            change_CO2e_t=0,
            cost_climate_saved=0,
        )
