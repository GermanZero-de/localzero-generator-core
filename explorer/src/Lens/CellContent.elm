module Lens.CellContent exposing (CellContent(..), getLabel, getValueAt)

import Run exposing (Path)


type CellContent
    = ValueAt Path
    | Label String


getValueAt : CellContent -> Maybe Path
getValueAt cc =
    case cc of
        ValueAt p ->
            Just p

        Label _ ->
            Nothing


getLabel : CellContent -> Maybe String
getLabel cc =
    case cc of
        ValueAt _ ->
            Nothing

        Label l ->
            Just l
