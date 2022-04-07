module GeneratorResult exposing (GeneratorResult, Node(..), Tree, decoder, get)

import Dict exposing (Dict)
import Json.Decode as Decode


type Node
    = Tree Tree
    | Leaf (Maybe Float)


type alias Tree =
    Dict String Node


type alias GeneratorResult =
    Tree


getHelper : List String -> Node -> Maybe Node
getHelper path node =
    case path of
        [] ->
            Just node

        name :: pathRest ->
            case node of
                Leaf _ ->
                    Nothing

                Tree t ->
                    Dict.get name t
                        |> Maybe.andThen (getHelper pathRest)


get : List String -> Tree -> Maybe Node
get p t =
    getHelper p (Tree t)


treeDecoder : Decode.Decoder Tree
treeDecoder =
    Decode.dict nodeDecoder


nodeDecoder : Decode.Decoder Node
nodeDecoder =
    Decode.oneOf
        [ Decode.float |> Decode.map (Leaf << Just)
        , Decode.null (Leaf Nothing)
        , Decode.dict (Decode.lazy (\() -> nodeDecoder)) |> Decode.map Tree
        ]


decoder : Decode.Decoder GeneratorResult
decoder =
    treeDecoder
