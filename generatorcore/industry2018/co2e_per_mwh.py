# pyright: strict
from dataclasses import InitVar, dataclass
from ..inputs import Inputs
from .co2e import CO2e


@dataclass
class CO2e_per_MWh(CO2e):
    # Used by p_other_further
    CO2e_production_based_per_MWh: float = 0
    CO2e_combustion_based_per_MWh: float = 0
    pct_energy: float = 0

    inputs: InitVar[Inputs] = None  # type: ignore
    category_energy: InitVar[float] = 0
    fact_pct_energy: InitVar[str] = ""
    fact_prod_volume: InitVar[str] = ""
    fact_CO2e_production_based_per_MWh: InitVar[str] = ""
    fact_CO2e_combustion_based_per_MWh: InitVar[str] = ""

    def __post_init__(  # type: ignore
        self,
        inputs: Inputs,
        category_energy: float,
        fact_pct_energy: str,
        fact_prod_volume: str,
        fact_CO2e_production_based_per_MWh: str,
        fact_CO2e_combustion_based_per_MWh: str,
    ):
        self.pct_energy = inputs.fact(fact_pct_energy)
        self.energy = self.pct_energy * category_energy

        self.prod_volume = inputs.fact(fact_prod_volume)

        self.CO2e_production_based_per_MWh = inputs.fact(
            fact_CO2e_production_based_per_MWh
        )
        self.CO2e_combustion_based_per_MWh = inputs.fact(
            fact_CO2e_combustion_based_per_MWh
        )

        self.CO2e_production_based = self.energy * self.CO2e_production_based_per_MWh
        self.CO2e_combustion_based = self.energy * self.CO2e_combustion_based_per_MWh

        super().__post_init__()

    @classmethod
    def calc_p_other_further(
        cls, inputs: Inputs, category_energy: float
    ) -> "CO2e_per_MWh":

        return cls(
            inputs=inputs,
            category_energy=category_energy,
            fact_pct_energy="Fact_I_P_other_fec_pct_of_further_2018",
            fact_prod_volume="Fact_I_P_other_further_prodvol_2018",
            fact_CO2e_production_based_per_MWh="Fact_I_P_other_2d_ratio_CO2e_pb_to_fec_2018",
            fact_CO2e_combustion_based_per_MWh="Fact_I_P_other_further_ratio_CO2e_cb_to_fec_2018",
        )
