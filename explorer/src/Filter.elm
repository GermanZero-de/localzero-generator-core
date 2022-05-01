module Filter exposing (filter)

import Dict
import Run exposing (Path)
import ValueTree exposing (Node(..), Tree)


filter : String -> Tree -> Tree
filter pattern tree =
    Dict.toList tree
        |> List.filterMap
            (\( name, child ) ->
                if String.contains pattern name then
                    Just ( name, child )

                else
                    case child of
                        Leaf _ ->
                            Nothing

                        Tree childTree ->
                            let
                                newChildTree =
                                    filter pattern childTree
                            in
                            if Dict.isEmpty newChildTree then
                                Nothing

                            else
                                Just ( name, Tree newChildTree )
            )
        |> Dict.fromList


expand : Path -> Tree -> List Path
expand path t =
    Dict.toList t
        |> List.concatMap
            (\( name, child ) ->
                case child of
                    Leaf _ ->
                        [ path ++ [ name ] ]

                    Tree childTree ->
                        expand (path ++ [ name ]) childTree
            )


search : String -> Tree -> List Path
search pattern tree =
    expand [] tree
        |> List.filter
            (\p ->
                String.contains pattern (String.join "." p)
            )
