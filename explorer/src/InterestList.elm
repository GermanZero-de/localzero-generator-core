module InterestList exposing
    ( InterestList
    , decoder
    , empty
    , encode
    , getLabel
    , getShortPathLabels
    , getShowGraph
    , insert
    , mapLabel
    , member
    , remove
    , toList
    , toggleShowGraph
    )

import Dict exposing (Dict)
import Html exposing (b)
import Json.Decode as Decode
import Json.Encode as Encode
import List.Extra
import Run exposing (Path)
import Set exposing (Set)


type InterestList
    = InterestList
        { label : String
        , paths : Set Path
        , showGraph : Bool
        , guessedShortLabels : Dict Path String
        }


type ShortenerInstruction
    = Skip String
    | Take


shorten : String -> List (List String) -> List String
shorten delim lists =
    let
        makeShortener : List ShortenerInstruction -> List (List String) -> List ShortenerInstruction
        makeShortener res ps =
            if List.any List.isEmpty ps then
                List.reverse res

            else
                case ps of
                    [] ->
                        List.reverse res

                    a :: rest ->
                        if List.all (\p -> List.head p == List.head a) rest then
                            makeShortener (Skip (List.head a |> Maybe.withDefault "") :: res) (List.map (List.drop 1) ps)

                        else
                            makeShortener (Take :: res) (List.map (List.drop 1) ps)

        shortener =
            makeShortener [] lists

        applyShortener : List ShortenerInstruction -> List String -> List String -> String
        applyShortener ins res list =
            case ( ins, list ) of
                ( [], _ ) ->
                    String.join delim (List.reverse res ++ list)

                ( _, [] ) ->
                    "CAN'T HAPPEN BECAUSE OF THE WAY SHORTENER IS CONSTRUCTED"

                ( (Skip s) :: insRest, _ :: listRest ) ->
                    applyShortener insRest res listRest

                ( Take :: insRest, l :: listRest ) ->
                    applyShortener insRest (l :: res) listRest
    in
    lists
        |> List.map (applyShortener shortener [])


mapLast : (a -> a) -> List a -> List a
mapLast f l =
    case List.Extra.unconsLast l of
        Nothing ->
            []

        Just ( x, prefix ) ->
            prefix ++ [ f x ]


{-| Sometimes we want to display shorter labels (e.g. in a chart), when all the labels are have a very similar
structure. This tries to guess short names.
-}
guessShortPathLabels : InterestList -> Dict Path String
guessShortPathLabels (InterestList il) =
    let
        paths =
            Set.toList il.paths

        shortLabels =
            let
                shortenedLastElements =
                    shorten "_"
                        (paths
                            |> List.map (String.split "_" << Maybe.withDefault "" << List.Extra.last)
                        )
            in
            shorten "." (List.map2 (\l e -> mapLast (always e) l) paths shortenedLastElements)
    in
    Dict.fromList (List.map2 Tuple.pair paths shortLabels)


getShortPathLabels : InterestList -> Dict Path String
getShortPathLabels (InterestList il) =
    il.guessedShortLabels


updateShortPathLabels : InterestList -> InterestList
updateShortPathLabels ((InterestList il) as i) =
    InterestList { il | guessedShortLabels = guessShortPathLabels i }


empty : InterestList
empty =
    InterestList { label = "data", paths = Set.empty, showGraph = False, guessedShortLabels = Dict.empty }


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
        |> updateShortPathLabels


insert : Path -> InterestList -> InterestList
insert p (InterestList i) =
    InterestList { i | paths = Set.insert p i.paths }
        |> updateShortPathLabels


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
            InterestList { label = label, showGraph = showGraph, paths = paths, guessedShortLabels = Dict.empty }
                |> updateShortPathLabels
        )
        (Decode.field "label" Decode.string)
        (Decode.field "showGraph" Decode.bool)
        (Decode.field "paths"
            (Decode.list (Decode.list Decode.string)
                |> Decode.map Set.fromList
            )
        )
