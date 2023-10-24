# pyright: strict
import json
import dataclasses
import datetime


@dataclasses.dataclass
class Change:
    """A change to a commune"""

    effective_date: datetime.date
    ags: str
    name: str

    def __str__(self):
        return f"{self.effective_date}: {self.ags} ({self.name})"

    def mentions_ags(self, ags: str) -> bool:
        return self.ags == ags


@dataclasses.dataclass
class AgsOrNameChange(Change):
    new_ags: str
    new_name: str

    def __str__(self):
        a = "" if self.new_ags == self.ags else f" NEW AGS {self.new_ags}"
        n = "" if self.new_name == self.name else f" NEW NAME {self.new_name}"
        return f"{super().__str__()}{a}{n}"

    def mentions_ags(self, ags: str) -> bool:
        return super().mentions_ags(ags) or self.new_ags == ags


@dataclasses.dataclass
class Dissolution(Change):
    """A dissolution is a change where a commune ceases to exist.

    new_ags: The ags of the commune that incorporates the area of the dissolved commune.
    new_name: is the name of the commune that incorporates the area of the dissolved commune.
    """

    ags: str
    name: str
    new_ags: str
    new_name: str

    def __str__(self) -> str:
        return f"{super().__str__()} DISSOLVED (AREA JOINED {self.new_ags} ({self.new_name}))"

    def mentions_ags(self, ags: str) -> bool:
        return super().mentions_ags(ags) or self.new_ags == ags


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
class PartialSpinOff(Change):
    """A partial spin off is a change where a commune loses some of its area to other communes."""

    ags: str
    name: str
    parts: list[Part]

    remaining_area: int
    remaining_population: int

    def __str__(self) -> str:
        return (
            super().__str__()
            + " SPINNED OFF "
            + ", ".join(str(p) for p in self.parts)
            + f" LEFTOVER {self.remaining_area} {self.remaining_population}"
        )

    def mentions_ags(self, ags: str) -> bool:
        return super().mentions_ags(ags) or any(p.ags == ags for p in self.parts)


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
