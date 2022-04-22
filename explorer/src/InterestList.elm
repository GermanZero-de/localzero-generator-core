module InterestList exposing
    ( InterestList
    , empty
    , insert
    , member
    , remove
    , toList
    )

import Run exposing (Path)
import Set exposing (Set)


type InterestList
    = InterestList { paths : Set Path }


empty : InterestList
empty =
    InterestList { paths = Set.empty }


remove : Path -> InterestList -> InterestList
remove p (InterestList i) =
    InterestList { i | paths = Set.remove p i.paths }


insert : Path -> InterestList -> InterestList
insert p (InterestList i) =
    InterestList { i | paths = Set.insert p i.paths }


member : Path -> InterestList -> Bool
member p (InterestList i) =
    Set.member p i.paths


toList : InterestList -> List Path
toList (InterestList i) =
    Set.toList i.paths
