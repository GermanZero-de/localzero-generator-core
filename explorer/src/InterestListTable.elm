module InterestListTable exposing (InterestListTable, create)

import AllRuns exposing (AllRuns, RunId)
import Dict exposing (Dict)
import InterestList exposing (InterestList)
import Run
import ValueTree exposing (Value(..))


type alias InterestListTable =
    { paths : List Run.Path
    , runs : List RunId
    , values : Dict ( RunId, Run.Path ) Value
    }


create : InterestList -> AllRuns -> InterestListTable
create interestList allRuns =
    -- The withDefault handles the case if we somehow managed to get two
    -- differently structured result values into the explorer, this can only
    -- really happen when two different versions of the python code are
    -- explored at the same time.
    -- Otherwise you can't add a path to the interest list that ends
    -- at a TREE
    let
        paths =
            InterestList.toList interestList

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
                                            |> ValueTree.get path
                                    of
                                        Nothing ->
                                            ( ( runId, path ), String "NOTHING" )

                                        Just (ValueTree.Tree _) ->
                                            ( ( runId, path ), String "TREE" )

                                        Just (ValueTree.Leaf v) ->
                                            ( ( runId, path ), v )
                                )
                    )
                |> Dict.fromList
    in
    { runs = runs, paths = paths, values = values }
