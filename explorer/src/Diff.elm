module Diff exposing (Diff(..), diff)

import Dict
import Tree exposing (Node(..), Tree)


type Diff value
    = Left (Node value)
    | Right (Node value)
    | Unequal (Node value) (Node value)


diff : (v -> v -> Bool) -> Tree v -> Tree v -> Tree (Diff v)
diff valueIsEqual a b =
    Dict.merge
        (\key value acc -> Dict.insert key (Leaf (Left value)) acc)
        (\key value1 value2 acc ->
            case ( value1, value2 ) of
                ( Tree t1, Tree t2 ) ->
                    let
                        t =
                            diff valueIsEqual t1 t2
                    in
                    if Dict.isEmpty t then
                        acc

                    else
                        Dict.insert key (Tree t) acc

                ( Tree _, Leaf _ ) ->
                    Dict.insert key (Leaf (Unequal value1 value2)) acc

                ( Leaf _, Tree _ ) ->
                    Dict.insert key (Leaf (Unequal value1 value2)) acc

                ( Leaf l1, Leaf l2 ) ->
                    if valueIsEqual l1 l2 then
                        acc

                    else
                        Dict.insert key (Leaf (Unequal value1 value2)) acc
        )
        (\key value acc -> Dict.insert key (Leaf (Right value)) acc)
        a
        b
        Dict.empty
