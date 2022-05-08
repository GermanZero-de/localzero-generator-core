module Explorable exposing (Comparable, Id(..), toComparable)

{-| There are two kinds of things explorable as Trees in the left panel of
the UI. Run's and Diffs of runs.
-}

import AllRuns
import Bitwise


type Id
    = Run AllRuns.RunId
    | Diff AllRuns.RunId AllRuns.RunId


type alias Comparable =
    Int


{-| For comparison
-}
toComparable : Id -> Comparable
toComparable e =
    case e of
        Run r ->
            r

        Diff r1 r2 ->
            Bitwise.or (Bitwise.shiftLeftBy 16 r1) r2
