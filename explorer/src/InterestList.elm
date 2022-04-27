module InterestList exposing
    ( InterestList
    , decoder
    , empty
    , encode
    , getLabel
    , getShowGraph
    , insert
    , mapLabel
    , member
    , remove
    , toList
    , toggleShowGraph
    )

import Json.Decode as Decode
import Json.Encode as Encode
import Run exposing (Path)
import Set exposing (Set)


type InterestList
    = InterestList { label : String, paths : Set Path, showGraph : Bool }


empty : InterestList
empty =
    InterestList { label = "data", paths = Set.empty, showGraph = True }


toggleShowGraph : InterestList -> InterestList
toggleShowGraph (InterestList il) =
    InterestList { il | showGraph = not il.showGraph }


getShowGraph : InterestList -> Bool
getShowGraph (InterestList il) =
    il.showGraph


getLabel : InterestList -> String
getLabel (InterestList l) =
    l.label


mapLabel : (String -> String) -> InterestList -> InterestList
mapLabel f (InterestList l) =
    InterestList { l | label = f l.label }


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


encode : InterestList -> Encode.Value
encode (InterestList i) =
    Encode.object
        [ ( "label", Encode.string i.label )
        , ( "showGraph", Encode.bool i.showGraph )
        , ( "paths", Encode.set (Encode.list Encode.string) i.paths )
        ]


decoder : Decode.Decoder InterestList
decoder =
    Decode.map3
        (\label showGraph paths ->
            InterestList { label = label, showGraph = showGraph, paths = paths }
        )
        (Decode.field "label" Decode.string)
        (Decode.field "showGraph" Decode.bool)
        (Decode.field "paths"
            (Decode.list (Decode.list Decode.string)
                |> Decode.map Set.fromList
            )
        )
