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
    , values : Dict ( RunId, Run.Path ) Value.MaybeWithTrace
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

        runs =
            List.map Tuple.first runsAndPaths
                -- Dedup
                |> Set.fromList
                |> Set.toList

        values =
            runsAndPaths
                |> List.map
                    (\( runId, path ) ->
                        case AllRuns.get runId allRuns of
                            Nothing ->
                                -- TODO: Represent missing run
                                ( ( runId, path ), { value = String "", trace = Nothing } )

                            Just run ->
                                case
                                    Run.getTree Run.WithOverrides run
                                        |> Tree.get path
                                of
                                    Nothing ->
                                        ( ( runId, path ), { value = String "", trace = Nothing } )

                                    Just (Tree.Tree _) ->
                                        ( ( runId, path ), { value = String "TREE", trace = Nothing} )

                                    Just (Tree.Leaf v) ->
                                        ( ( runId, path ), v )
                    )
                |> Dict.fromList
    in
    { runs = runs, paths = paths, values = values }
