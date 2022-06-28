module ValueSet exposing (ValueSet, create)

{-| A ValueSet is the result of applying a Lens to all the runs.
-}

import AllRuns exposing (AllRuns, RunId)
import Dict exposing (Dict)
import Lens exposing (Lens)
import Run
import Set
import Tree
import Value exposing (Value(..))


type alias ValueSet =
    { paths : List Run.Path
    , runs : List RunId
    , values : Dict ( RunId, Run.Path ) Value
    }


create : Lens -> AllRuns -> ValueSet
create lens allRuns =
    -- The withDefault handles the case if we somehow managed to get two
    -- differently structured result values into the explorer, this can only
    -- really happen when two different versions of the python code are
    -- explored at the same time.
    -- Otherwise you can't add a path to the interest list that ends
    -- at a TREE
    let
        runsAndPaths =
            Lens.toList allRuns lens

        paths =
            List.map Tuple.second runsAndPaths
                |> Set.fromList
                |> Set.toList

        runList =
            AllRuns.toList allRuns

        runs =
            List.map Tuple.first runList

        values =
            runsAndPaths
                |> List.map
                    (\( runId, path ) ->
                        case AllRuns.get runId allRuns of
                            Nothing ->
                                -- TODO: Represent missing run
                                ( ( runId, path ), String "" )

                            Just run ->
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
                |> Dict.fromList
    in
    { runs = runs, paths = paths, values = values }
