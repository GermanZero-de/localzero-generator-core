module AllRuns exposing
    ( AbsolutePath
    , GeneratorRuns
    , add
    , empty
    , get
    , getValue
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
import Run exposing (Path, Run)
import ValueTree exposing (Value)


{-| A Path to a value inside a given GeneratorResult
-}
type alias AbsolutePath =
    ( Int, Path )


{-| One run of the generator
-}
type GeneratorRuns
    = GeneratorRuns (Array Run)


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


getValue : Int -> Path -> GeneratorRuns -> Maybe Value
getValue ndx path (GeneratorRuns a) =
    Array.get ndx a
        |> Maybe.andThen
            (\r ->
                ValueTree.get path (Run.getTree r)
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


get : Int -> GeneratorRuns -> Maybe Run
get ndx (GeneratorRuns a) =
    Array.get ndx a


toList : GeneratorRuns -> List ( Int, Run )
toList (GeneratorRuns a) =
    Array.toIndexedList a
