module Run exposing
    ( Inputs
    , Overrides
    , Path
    , Run
    , create
    , getInputs
    , getOverrides
    , getTree
    , mapOverrides
    )

{-| A run of the generator.
-}

import Dict exposing (Dict)
import ValueTree exposing (Tree)


{-| A Path to a value inside a run.
-}
type alias Path =
    List String


type alias Overrides =
    Dict String Float


type Run
    = Run
        { result : Tree
        , entries : Tree
        , overrides : Overrides
        , inputs : Inputs
        }


type alias Inputs =
    { ags : String, year : Int }


create : { inputs : Inputs, entries : Tree, overrides : Overrides, result : Tree } -> Run
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


getTree : Run -> Tree
getTree (Run r) =
    ValueTree.merge
        (ValueTree.wrap "entries" r.entries)
        (ValueTree.wrap "result" r.result)
