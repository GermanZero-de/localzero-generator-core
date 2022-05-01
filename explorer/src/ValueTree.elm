module ValueTree exposing (Node(..), Tree, Value(..), decoder, expand, get, merge, valueDecoder, wrap)

import Dict exposing (Dict)
import Json.Decode as Decode


type Node
    = Tree Tree
    | Leaf Value


type Value
    = Float Float
    | Null
    | String String


type alias Tree =
    Dict String Node


wrap : String -> Tree -> Tree
wrap name tree =
    Dict.fromList [ ( name, Tree tree ) ]


merge : Tree -> Tree -> Tree
merge t1 t2 =
    Dict.union t1 t2


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


expandHelper : List String -> Tree -> List (List String)
expandHelper path t =
    Dict.toList t
        |> List.concatMap
            (\( name, child ) ->
                case child of
                    Leaf _ ->
                        [ path ++ [ name ] ]

                    Tree childTree ->
                        expandHelper (path ++ [ name ]) childTree
            )


expand : Tree -> List (List String)
expand =
    expandHelper []


get : List String -> Tree -> Maybe Node
get p t =
    getHelper p (Tree t)


treeDecoder : Decode.Decoder Tree
treeDecoder =
    Decode.dict nodeDecoder


valueDecoder : Decode.Decoder Value
valueDecoder =
    Decode.oneOf
        [ Decode.float |> Decode.map Float
        , Decode.string |> Decode.map String
        , Decode.null Null
        ]


nodeDecoder : Decode.Decoder Node
nodeDecoder =
    Decode.oneOf
        [ valueDecoder |> Decode.map Leaf
        , Decode.dict (Decode.lazy (\() -> nodeDecoder)) |> Decode.map Tree
        ]


decoder : Decode.Decoder Tree
decoder =
    treeDecoder
