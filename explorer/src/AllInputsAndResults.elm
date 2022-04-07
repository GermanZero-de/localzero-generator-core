module AllInputsAndResults exposing
    ( AbsolutePath
    , AllInputsAndResults
    , Inputs
    , InputsAndResult
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


{-| A Path to a result inside a given GeneratorResult
-}
type alias Path =
    List String


{-| A Path to a result inside the nth ExplorerResult
-}
type alias AbsolutePath =
    ( Int, Path )


type alias InputsAndResult =
    { result : GeneratorResult
    , inputs : Inputs
    }


type alias Inputs =
    { ags : String, year : Int }


type AllInputsAndResults
    = AllInputsAndResults (Array InputsAndResult)


empty : AllInputsAndResults
empty =
    AllInputsAndResults Array.empty


add : InputsAndResult -> AllInputsAndResults -> AllInputsAndResults
add ir (AllInputsAndResults a) =
    let
        new =
            Array.push ir a
    in
    AllInputsAndResults new


remove : Int -> AllInputsAndResults -> AllInputsAndResults
remove ndx (AllInputsAndResults a) =
    let
        new =
            Array.Extra.removeAt ndx a
    in
    AllInputsAndResults new


set : Int -> InputsAndResult -> AllInputsAndResults -> AllInputsAndResults
set ndx ir (AllInputsAndResults a) =
    Array.set ndx ir a
        |> AllInputsAndResults


size : AllInputsAndResults -> Int
size (AllInputsAndResults a) =
    Array.length a


getValue : AbsolutePath -> AllInputsAndResults -> Maybe Float
getValue ( ndx, path ) (AllInputsAndResults a) =
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


maybeGet : Maybe Int -> AllInputsAndResults -> Maybe InputsAndResult
maybeGet maybeNdx (AllInputsAndResults a) =
    case maybeNdx of
        Nothing ->
            Nothing

        Just ndx ->
            Array.get ndx a


toList : AllInputsAndResults -> List ( Int, InputsAndResult )
toList (AllInputsAndResults a) =
    Array.toIndexedList a
