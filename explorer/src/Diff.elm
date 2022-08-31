module Diff exposing (Diff(..), diff)

import Dict
import Tree exposing (Node(..), Tree)


type Diff value
    = LeftOnly value
    | RightOnly value
    | Unequal value value


{-| This compares two trees and returns a new tree that contains
only the differences. Concretely a leaf can then be either a value
that exists only on the left, only on the right or both values if they
were not equal.

Note: If the two trees at the same place contain a leaf on one side and
another tree on the other side, the leaf will not be reported at all.
Instead all the values in the tree will be reported as usual (e.g. as only
on one side).

This is clearly not optimal, but it strongly simplifies the type of the diffs
and in our uses cases this should not matter (as we normally do not change
the structure of the result type in that way). And either way a diff is still
reported even if the diff does not contain all the values one would like to see.

-}
diff : (v -> v -> Bool) -> Tree v -> Tree v -> Tree (Diff v)
diff valueIsEqual a b =
    let
        insertLeftOnlyTree key leftOnlyTree acc =
            acc
                |> Dict.insert key (Tree (diff valueIsEqual leftOnlyTree Tree.empty))

        insertRightOnlyTree key rightOnlyTree acc =
            acc
                |> Dict.insert key (Tree (diff valueIsEqual Tree.empty rightOnlyTree))
    in
    Dict.merge
        (\key value acc ->
            case value of
                Tree leftOnlyTree ->
                    acc
                        |> insertLeftOnlyTree key leftOnlyTree

                Leaf leaf ->
                    acc
                        |> Dict.insert key (Leaf (LeftOnly leaf))
        )
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

                ( Tree leftOnlyTree, Leaf _ ) ->
                    acc
                        |> insertLeftOnlyTree key leftOnlyTree

                ( Leaf _, Tree rightOnlyTree ) ->
                    acc
                        |> insertRightOnlyTree key rightOnlyTree

                ( Leaf l1, Leaf l2 ) ->
                    if valueIsEqual l1 l2 then
                        acc

                    else
                        Dict.insert key (Leaf (Unequal l1 l2)) acc
        )
        (\key value acc ->
            case value of
                Tree rightOnlyTree ->
                    acc
                        |> Dict.insert key (Tree (diff valueIsEqual Tree.empty rightOnlyTree))

                Leaf leaf ->
                    acc
                        |> Dict.insert key (Leaf (RightOnly leaf))
        )
        a
        b
        Dict.empty
