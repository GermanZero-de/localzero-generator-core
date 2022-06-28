module Lens.CellContent exposing (CellContent(..), getLabel, getValueAt)

import AllRuns exposing (RunId)
import Run exposing (Path)


type CellContent
    = ValueAt RunId Path
    | Label String


getValueAt : CellContent -> Maybe ( RunId, Path )
getValueAt cc =
    case cc of
        ValueAt ri p ->
            Just ( ri, p )

        Label _ ->
            Nothing


getLabel : CellContent -> Maybe String
getLabel cc =
    case cc of
        ValueAt _ _ ->
            Nothing

        Label l ->
            Just l
