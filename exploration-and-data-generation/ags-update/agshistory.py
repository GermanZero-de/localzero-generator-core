# pyright: strict
import json
import dataclasses
import datetime


@dataclasses.dataclass
class Change:
    """All changes to a commune include the AGS and the name and
    happen as of a particular date."""

    effective_date: datetime.date
    ags: str
    name: str

    def __str__(self):
        return f"{self.effective_date}: {self.ags} ({self.name})"

    def mentions_ags(self, ags: str) -> bool:
        return self.ags == ags or ags in self.all_new_ags()

    def all_new_ags(self) -> list[str]:
        assert False, "This needs to be implemented in each child"


@dataclasses.dataclass
class AgsOrNameChange(Change):
    """Either the AGS or the name or both of commune is changed."""

    new_ags: str
    new_name: str

    def __str__(self):
        a = "" if self.new_ags == self.ags else f" NEW AGS {self.new_ags}"
        n = "" if self.new_name == self.name else f" NEW NAME {self.new_name}"
        return f"{super().__str__()}{a}{n}"

    def all_new_ags(self) -> list[str]:
        return [self.new_ags]


@dataclasses.dataclass
class Part:
    ags: str
    name: str
    area_in_sqm: int
    population: int

    def __str__(self) -> str:
        return (
            f"{self.area_in_sqm} SQM {self.population} POP to {self.ags} ({self.name})"
        )


@dataclasses.dataclass
class ChangeWithParts(Change):
    parts: list[Part]

    def all_new_ags(self) -> list[str]:
        return [p.ags for p in self.parts]

    def total_area_of_parts_in_sqm(self) -> int:
        return sum(p.area_in_sqm for p in self.parts)

    def total_population_of_parts(self) -> int:
        return sum(p.population for p in self.parts)

    def total_area_in_sqm(self) -> int:
        assert False, "this needs to be overriden in the child classes"

    def parts_with_ratios_by_area(self) -> list[tuple[Part, float]]:
        total_area = self.total_area_in_sqm()
        return [(p, p.area_in_sqm / total_area) for p in self.parts]


@dataclasses.dataclass
class Dissolution(ChangeWithParts):
    """A dissolution is a change where a commune ceases to exist.
    And the area joins other communes.
    """

    def total_area_in_sqm(self) -> int:
        return self.total_area_of_parts_in_sqm()

    def __str__(self) -> str:
        parts_desc = ", ".join(str(p) for p in self.parts)
        return f"{super().__str__()} DISSOLVED (AREA JOINED {parts_desc})"


@dataclasses.dataclass
class PartialSpinOff(ChangeWithParts):
    """A partial spin off is a change where a commune loses some of its area to other communes."""

    remaining_area: int
    remaining_population: int

    def total_area_in_sqm(self) -> int:
        return self.total_area_of_parts_in_sqm() + self.remaining_area

    def __str__(self) -> str:
        return (
            super().__str__()
            + " SPINNED OFF "
            + ", ".join(str(p) for p in self.parts)
            + f" LEFTOVER {self.remaining_area} {self.remaining_population}"
        )


FIRST_DATE_OF_INTEREST = datetime.date(2019, 1, 1)
LAST_DATE_OF_INTEREST = datetime.date(2022, 12, 31)


def is_date_of_interest(d: datetime.date) -> bool:
    return FIRST_DATE_OF_INTEREST <= d <= LAST_DATE_OF_INTEREST


class JsonEncoder(json.JSONEncoder):
    def default(self, o: object):
        if dataclasses.is_dataclass(o):
            dict = dataclasses.asdict(o)
            dict["kind"] = o.__class__.__name__
            return dict
        if isinstance(o, datetime.date):
            return o.isoformat()
        return super().default(o)


class JsonDecoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.convert_dict)

    @staticmethod
    def convert_dict(dct: dict[str, object]):
        if "kind" in dct:
            if "effective_date" in dct:
                dct["effective_date"] = datetime.date.fromisoformat(dct["effective_date"])  # type: ignore
            kind = dct["kind"]
            del dct["kind"]
            match kind:
                case "AgsOrNameChange":
                    return AgsOrNameChange(**dct)  # type: ignore
                case "Dissolution":
                    assert "parts" in dct
                    dct["parts"] = [Part(**p) for p in dct["parts"]]  # type: ignore
                    return Dissolution(**dct)  # type: ignore
                case "PartialSpinOff":
                    assert "parts" in dct
                    dct["parts"] = [Part(**p) for p in dct["parts"]]  # type: ignore
                    return PartialSpinOff(**dct)  # type: ignore
                case _:
                    raise ValueError(f"Unknown kind {kind}")  # type: ignore
        return dct


def load() -> list[Change]:
    with open("ags-history.json") as f:
        data = json.load(f, cls=JsonDecoder)
    return data


def show(ags: str):
    changes = load()
    for ch in changes:
        if ch.mentions_ags(ags):
            print(ch)
