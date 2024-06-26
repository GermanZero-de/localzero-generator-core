module Run exposing
    ( Entries
    , Inputs
    , OverrideHandling(..)
    , Overrides
    , Path
    , Run
    , create
    , encodeOverrides
    , entriesDecoder
    , getInputs
    , getOverrides
    , getTree
    , mapOverrides
    , year_baseline
    )

{-| A run of the generator.
-}

import Dict exposing (Dict)
import Json.Decode as Decode
import Json.Encode as Encode
import Tree exposing (Tree)
import Value


{-| A Path to a value inside a run.
-}
type alias Path =
    List String


type alias Overrides =
    Dict String Float


type alias Entries =
    Dict String Value.MaybeWithTrace


type Run
    = Run
        { result : Tree Value.MaybeWithTrace
        , entries : Entries
        , overrides : Overrides
        , inputs : Inputs
        }


type alias Inputs =
    { ags : String, year_target : Int, year_baseline : Int }


year_baseline : Int
year_baseline =
    2022


create :
    { inputs : Inputs
    , entries : Entries
    , overrides : Overrides
    , result : Tree Value.MaybeWithTrace
    }
    -> Run
create { inputs, entries, result, overrides } =
    Run
        { inputs = inputs
        , entries = entries
        , result = result
        , overrides = overrides
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


type OverrideHandling
    = WithOverrides
    | WithoutOverrides


getTree : OverrideHandling -> Run -> Tree Value.MaybeWithTrace
getTree h (Run r) =
    let
        entries =
            case h of
                WithoutOverrides ->
                    Dict.map (\_ v -> Tree.Leaf v) r.entries

                WithOverrides ->
                    Dict.map
                        (\k v ->
                            case Dict.get k r.overrides of
                                Nothing ->
                                    Tree.Leaf v

                                Just o ->
                                    Tree.Leaf { value = Value.Float o, trace = Nothing }
                        )
                        r.entries
    in
    Tree.merge
        (Tree.wrap "entries" entries)
        (Tree.wrap "result" r.result)


entriesDecoder : Decode.Decoder Entries
entriesDecoder =
    Decode.dict (Value.maybeWithTraceDecoder "entries")


encodeOverrides : Overrides -> Encode.Value
encodeOverrides d =
    Encode.dict
        identity
        Encode.float
        d
