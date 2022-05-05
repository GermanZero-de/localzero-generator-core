module AllRuns exposing
    ( AbsolutePath
    , AllRuns
    , RunId
    , add
    , empty
    , get
    , getValue
    , remove
    , set
    , size
    , stringFromRunId
    , toList
    , update
    )

import Dict exposing (Dict)
import Run exposing (Path, Run)
import Tree exposing (Value)


type alias RunId =
    Int


stringFromRunId : RunId -> String
stringFromRunId runId =
    String.fromInt runId


{-| A Path to a value inside a given GeneratorResult
-}
type alias AbsolutePath =
    ( Int, Path )


{-| One run of the generator.
Uses a dictionary so that ids still refer to the same generator run after deletion of
another run.
-}
type AllRuns
    = AllRuns { runs : Dict Int Run, nextId : Int }


empty : AllRuns
empty =
    AllRuns { runs = Dict.empty, nextId = 0 }


add : Run -> AllRuns -> AllRuns
add ir (AllRuns a) =
    let
        newNextId =
            a.nextId + 1

        new =
            Dict.insert a.nextId ir a.runs
    in
    AllRuns { runs = new, nextId = newNextId }


remove : RunId -> AllRuns -> AllRuns
remove id (AllRuns a) =
    AllRuns { a | runs = Dict.remove id a.runs }


update : RunId -> (Run -> Run) -> AllRuns -> AllRuns
update id f (AllRuns a) =
    case Dict.get id a.runs of
        Nothing ->
            AllRuns a

        Just r ->
            AllRuns { a | runs = Dict.insert id (f r) a.runs }


set : RunId -> Run -> AllRuns -> AllRuns
set id ir (AllRuns a) =
    AllRuns
        { a
            | runs = Dict.insert id ir a.runs
        }


size : AllRuns -> Int
size (AllRuns a) =
    Dict.size a.runs


getValue : Run.OverrideHandling -> RunId -> Path -> AllRuns -> Maybe Value
getValue handling ndx path (AllRuns a) =
    Dict.get ndx a.runs
        |> Maybe.andThen
            (\r ->
                Tree.get path (Run.getTree handling r)
                    |> Maybe.andThen
                        (\node ->
                            case node of
                                Tree.Tree _ ->
                                    Nothing

                                Tree.Leaf n ->
                                    Just n
                        )
            )


get : RunId -> AllRuns -> Maybe Run
get id (AllRuns a) =
    Dict.get id a.runs


toList : AllRuns -> List ( RunId, Run )
toList (AllRuns a) =
    Dict.toList a.runs
