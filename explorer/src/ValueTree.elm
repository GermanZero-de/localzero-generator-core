module ValueTree exposing (Node(..), Tree, Value(..), decoder, get, merge, wrap)

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


get : List String -> Tree -> Maybe Node
get p t =
    getHelper p (Tree t)


treeDecoder : Decode.Decoder Tree
treeDecoder =
    Decode.dict nodeDecoder


nodeDecoder : Decode.Decoder Node
nodeDecoder =
    Decode.oneOf
        [ Decode.float |> Decode.map (Leaf << Float)
        , Decode.string |> Decode.map (Leaf << String)
        , Decode.null (Leaf Null)
        , Decode.dict (Decode.lazy (\() -> nodeDecoder)) |> Decode.map Tree
        ]


decoder : Decode.Decoder Tree
decoder =
    treeDecoder
