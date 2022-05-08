module Filter exposing (filter)

import Dict
import Glob
import Html.Attributes exposing (pattern)
import Run exposing (Path)
import Tree exposing (Node(..), Tree)


filterWord : String -> Tree value -> Tree value
filterWord pattern tree =
    Dict.toList tree
        |> List.filterMap
            (\( name, child ) ->
                if Glob.match pattern name then
                    Just ( name, child )

                else
                    case child of
                        Leaf _ ->
                            Nothing

                        Tree childTree ->
                            let
                                newChildTree =
                                    filterWord pattern childTree
                            in
                            if Dict.isEmpty newChildTree then
                                Nothing

                            else
                                Just ( name, Tree newChildTree )
            )
        |> Dict.fromList


filter : String -> Tree value -> Tree value
filter pattern tree =
    let
        words =
            String.words pattern
    in
    if List.isEmpty words then
        Dict.empty

    else
        List.foldl filterWord tree words
