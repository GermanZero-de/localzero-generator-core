module InterestListTable exposing (ValueSet, create)

{-| A InterestListTable is the result of applying an InterestList
to all the runs.
-}

import AllRuns exposing (AllRuns, RunId)
import Dict exposing (Dict)
import Lens exposing (Lens)
import Run
import Tree
import Value exposing (Value(..))


type alias ValueSet =
    { paths : List Run.Path
    , runs : List RunId
    , values : Dict ( RunId, Run.Path ) Value
    }


create : Lens -> AllRuns -> ValueSet
create interestList allRuns =
    -- The withDefault handles the case if we somehow managed to get two
    -- differently structured result values into the explorer, this can only
    -- really happen when two different versions of the python code are
    -- explored at the same time.
    -- Otherwise you can't add a path to the interest list that ends
    -- at a TREE
    let
        paths =
            Lens.toList interestList

        runList =
            AllRuns.toList allRuns

        runs =
            List.map Tuple.first runList

        values =
            runList
                |> List.concatMap
                    (\( runId, run ) ->
                        paths
                            |> List.map
                                (\path ->
                                    case
                                        Run.getTree Run.WithOverrides run
                                            |> Tree.get path
                                    of
                                        Nothing ->
                                            ( ( runId, path ), String "" )

                                        Just (Tree.Tree _) ->
                                            ( ( runId, path ), String "TREE" )

                                        Just (Tree.Leaf v) ->
                                            ( ( runId, path ), v )
                                )
                    )
                |> Dict.fromList
    in
    { runs = runs, paths = paths, values = values }
