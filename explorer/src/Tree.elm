module Tree exposing (Node(..), Tree, decoder, expand, get, merge, wrap)

import Dict exposing (Dict)
import Json.Decode as Decode
import Value exposing (Value)


type Node value
    = Tree (Tree value)
    | Leaf value


type alias Tree value =
    Dict String (Node value)


wrap : String -> Tree value -> Tree value
wrap name tree =
    Dict.fromList [ ( name, Tree tree ) ]


merge : Tree value -> Tree value -> Tree value
merge t1 t2 =
    Dict.union t1 t2


getHelper : List String -> Node value -> Maybe (Node value)
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


expandHelper : List String -> Tree value -> List (List String)
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


expand : Tree value -> List (List String)
expand =
    expandHelper []


get : List String -> Tree value -> Maybe (Node value)
get p t =
    getHelper p (Tree t)


treeDecoder : Decode.Decoder value -> Decode.Decoder (Tree value)
treeDecoder valueDecoder =
    Decode.dict (nodeDecoder valueDecoder)


nodeDecoder : Decode.Decoder value -> Decode.Decoder (Node value)
nodeDecoder valueDecoder =
    Decode.oneOf
        [ valueDecoder |> Decode.map Leaf
        , Decode.dict (Decode.lazy (\() -> nodeDecoder valueDecoder)) |> Decode.map Tree
        ]


decoder : Decode.Decoder value -> Decode.Decoder (Tree value)
decoder valueDecoder =
    treeDecoder valueDecoder
