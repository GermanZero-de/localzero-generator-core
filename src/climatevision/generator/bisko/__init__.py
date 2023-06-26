# pyright: strict

from dataclasses import dataclass

from ..refdata import Facts, Assumptions
from ..utils import div
from ..agri2018.a18 import A18
from ..electricity2018.e18 import E18
from ..business2018.b18 import B18
from ..fuels2018.f18 import F18
from ..heat2018.h18 import H18
from ..industry2018.i18 import I18
from ..lulucf2018.l18 import L18
from ..residences2018.r18 import R18
from ..transport2018.t18 import T18

from .dataclasses import (
    BiskoPrivResidences,
    BiskoBusiness,
    BiskoTransport,
    BiskoIndustry,
    BiskoAgriculture,
    BiskoLULUCF,
    EnergyAndEmissions,
)


@dataclass(kw_only=True)
class Bisko:
    priv_residences: BiskoPrivResidences
    business: BiskoBusiness
    transport: BiskoTransport
    industry: BiskoIndustry

    agri: BiskoAgriculture
    lulucf: BiskoLULUCF

    total: EnergyAndEmissions
    communal_facilities: EnergyAndEmissions

    bisko_quality: float

    @classmethod
    def calc(
        cls,
        facts: Facts,
        assumptions: Assumptions,
        *,
        a18: A18,
        b18: B18,
        e18: E18,
        f18: F18,
        h18: H18,
        i18: I18,
        l18: L18,
        r18: R18,
        t18: T18,
    ) -> "Bisko":

        priv_residences_bisko = BiskoPrivResidences.calc_priv_residences_bisko(
            facts, r18=r18, h18=h18, f18=f18, e18=e18
        )
        business_bisko = BiskoBusiness.calc_business_bisko(
            facts, b18=b18, e18=e18, a18=a18
        )
        transport_bisko = BiskoTransport.calc_transport_bisko(
            facts, assumptions, t18=t18, e18=e18
        )
        industry_bisko = BiskoIndustry.calc_industry_bisko(facts, i18=i18, e18=e18)
        agri_bisko = BiskoAgriculture.calc_bisko_agri(a18=a18)
        lulucf_bisko = BiskoLULUCF.calc_bisko_lulucf(l18=l18)

        total = EnergyAndEmissions.sum(
            priv_residences_bisko.total,
            business_bisko.total,
            transport_bisko.total,
            industry_bisko.total,
        )

        total.add_production_based_emission(agri_bisko.total, lulucf_bisko.total)
        total.add_combustion_based_emission(lulucf_bisko.total)

        total.update_CO2e_total()

        communal_facilities = EnergyAndEmissions.sum(
            priv_residences_bisko.communal_facilities,
            business_bisko.communal_facilities,
        )
        bisko_quality = transport_bisko.total.energy * div(0.5, total.energy)

        return cls(
            priv_residences=priv_residences_bisko,
            business=business_bisko,
            transport=transport_bisko,
            industry=industry_bisko,
            agri=agri_bisko,
            lulucf=lulucf_bisko,
            total=total,
            communal_facilities=communal_facilities,
            bisko_quality=bisko_quality,
        )
