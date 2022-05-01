module Filter exposing (filter)

import Dict
import Html.Attributes exposing (pattern)
import Run exposing (Path)
import ValueTree exposing (Node(..), Tree)


filterWord : String -> Tree -> Tree
filterWord pattern tree =
    Dict.toList tree
        |> List.filterMap
            (\( name, child ) ->
                if String.toLower pattern == String.toLower name then
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


filter : String -> Tree -> Tree
filter pattern tree =
    let
        words =
            String.words pattern
    in
    if List.isEmpty words then
        Dict.empty

    else
        List.foldl filterWord tree words
