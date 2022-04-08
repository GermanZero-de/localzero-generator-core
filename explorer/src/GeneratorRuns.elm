module GeneratorRuns exposing
    ( AbsolutePath
    , GeneratorRuns
    , Inputs
    , Run
    , Path
    , add
    , empty
    , getValue
    , maybeGet
    , remove
    , set
    , size
    , toList
    )

import Array exposing (Array)
import Array.Extra
import GeneratorResult exposing (GeneratorResult)
import Html exposing (a)


{-| A Path to a value inside a given GeneratorResult
-}
type alias Path =
    List String


{-| A Path to a value inside the nth Run
-}
type alias AbsolutePath =
    ( Int, Path )


type alias Run =
    { result : GeneratorResult
    , inputs : Inputs
    }


type alias Inputs =
    { ags : String, year : Int }


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


set : Int -> Run -> GeneratorRuns -> GeneratorRuns
set ndx ir (GeneratorRuns a) =
    Array.set ndx ir a
        |> GeneratorRuns


size : GeneratorRuns -> Int
size (GeneratorRuns a) =
    Array.length a


getValue : AbsolutePath -> GeneratorRuns -> Maybe Float
getValue ( ndx, path ) (GeneratorRuns a) =
    Array.get ndx a
        |> Maybe.andThen
            (\ir ->
                GeneratorResult.get path ir.result
                    |> Maybe.andThen
                        (\node ->
                            case node of
                                GeneratorResult.Tree _ ->
                                    Nothing

                                GeneratorResult.Leaf n ->
                                    n
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
