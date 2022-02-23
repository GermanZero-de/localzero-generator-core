"""
AGS - Allgemeiner Gemeinde Schlüssel (Official Municipality Key)

In Germany the Official Municipality Key serves statistical purposes
and is issued by the statistics offices of individual German states.

The municipality key is to be indicated in instances such as changing
residence on the notice of departure or registration documents.
This is done at the registration office in every town's city hall.
Structure The municipality key consists of eight digits, which are
generated as follows:
    -The first two numbers designate the individual German state.

    - The third digit designates the government district (in areas
      without government districts a zero is used instead).

    - The fourth and fifth digits designate the number of the urban
      area (in a district-free city) or the district (in a city with districts).

    - The sixth, seventh, and eighth digits indicate the municipality or
      the number of the unincorporated area.
"""


def is_valid(ags: str) -> bool:
    """Is the given string a valid ags?"""
    try:
        return ags == "DG000000" or (
            len(ags) == 8
            and all("0" <= c <= "9" for c in ags)
            and 1 <= int(ags[:2]) <= 16
        )
    except:
        return False
