module GeneratorRuns exposing
    ( AbsolutePath
    , GeneratorRuns
    , Inputs
    , Overrides
    , Path
    , Run
    , add
    , createRun
    , empty
    , getInputs
    , getOverrides
    , getTree
    , getValue
    , mapOverrides
    , maybeGet
    , remove
    , set
    , size
    , toList
    , update
    )

import Array exposing (Array)
import Array.Extra
import Dict exposing (Dict)
import Html exposing (a)
import ValueTree exposing (Tree, Value)


{-| A Path to a value inside a given GeneratorResult
-}
type alias Path =
    List String


type alias AbsolutePath =
    ( Int, Path )


type alias Overrides =
    Dict String Float


{-| One run of the generator
-}
type Run
    = Run
        { result : Tree
        , entries : Tree
        , overrides : Overrides
        , inputs : Inputs
        }


type alias Inputs =
    { ags : String, year : Int }


type GeneratorRuns
    = GeneratorRuns (Array Run)


createRun : { inputs : Inputs, entries : Tree, result : Tree } -> Run
createRun { inputs, entries, result } =
    Run
        { inputs = inputs
        , entries = entries
        , result = result
        , overrides = Dict.empty
        }


mapOverrides : (Overrides -> Overrides) -> Run -> Run
mapOverrides f (Run r) =
    Run { r | overrides = f r.overrides }


getOverrides : Run -> Overrides
getOverrides (Run r) =
    r.overrides


getInputs : Run -> Inputs
getInputs (Run r) =
    r.inputs


empty : GeneratorRuns
empty =
    GeneratorRuns Array.empty


add : Run -> GeneratorRuns -> GeneratorRuns
add ir (GeneratorRuns a) =
    let
        new =
            Array.push ir a
    in
    GeneratorRuns new


remove : Int -> GeneratorRuns -> GeneratorRuns
remove ndx (GeneratorRuns a) =
    let
        new =
            Array.Extra.removeAt ndx a
    in
    GeneratorRuns new


update : Int -> (Run -> Run) -> GeneratorRuns -> GeneratorRuns
update ndx f (GeneratorRuns a) =
    case Array.get ndx a of
        Nothing ->
            GeneratorRuns a

        Just r ->
            GeneratorRuns (Array.set ndx (f r) a)


set : Int -> Run -> GeneratorRuns -> GeneratorRuns
set ndx ir (GeneratorRuns a) =
    Array.set ndx ir a
        |> GeneratorRuns


size : GeneratorRuns -> Int
size (GeneratorRuns a) =
    Array.length a


getTree : Run -> Tree
getTree (Run r) =
    ValueTree.merge
        (ValueTree.wrap "entries" r.entries)
        (ValueTree.wrap "result" r.result)


getValue : Int -> Path -> GeneratorRuns -> Maybe Value
getValue ndx path (GeneratorRuns a) =
    Array.get ndx a
        |> Maybe.andThen
            (\r ->
                ValueTree.get path (getTree r)
                    |> Maybe.andThen
                        (\node ->
                            case node of
                                ValueTree.Tree _ ->
                                    Nothing

                                ValueTree.Leaf n ->
                                    Just n
                        )
            )


maybeGet : Maybe Int -> GeneratorRuns -> Maybe Run
maybeGet maybeNdx (GeneratorRuns a) =
    case maybeNdx of
        Nothing ->
            Nothing

        Just ndx ->
            Array.get ndx a


toList : GeneratorRuns -> List ( Int, Run )
toList (GeneratorRuns a) =
    Array.toIndexedList a
