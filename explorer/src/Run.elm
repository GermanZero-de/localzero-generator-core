module Run exposing
    ( Entries
    , Inputs
    , OverrideHandling(..)
    , Overrides
    , Path
    , Run
    , create
    , entriesDecoder
    , getInputs
    , getOverrides
    , getTree
    , mapOverrides
    )

{-| A run of the generator.
-}

import Dict exposing (Dict)
import Json.Decode as Decode
import ValueTree exposing (Tree)


{-| A Path to a value inside a run.
-}
type alias Path =
    List String


type alias Overrides =
    Dict String Float


type alias Entries =
    Dict String ValueTree.Value


type Run
    = Run
        { result : Tree
        , entries : Entries
        , overrides : Overrides
        , inputs : Inputs
        }


type alias Inputs =
    { ags : String, year : Int }


create : { inputs : Inputs, entries : Entries, overrides : Overrides, result : Tree } -> Run
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


getTree : OverrideHandling -> Run -> Tree
getTree h (Run r) =
    let
        entries =
            case h of
                WithoutOverrides ->
                    Dict.map (\_ v -> ValueTree.Leaf v) r.entries

                WithOverrides ->
                    Dict.map
                        (\k v ->
                            case Dict.get k r.overrides of
                                Nothing ->
                                    ValueTree.Leaf v

                                Just o ->
                                    ValueTree.Leaf (ValueTree.Float o)
                        )
                        r.entries
    in
    ValueTree.merge
        (ValueTree.wrap "entries" entries)
        (ValueTree.wrap "result" r.result)


entriesDecoder : Decode.Decoder Entries
entriesDecoder =
    Decode.dict ValueTree.valueDecoder
