module Lens exposing
    ( Lens
    , decoder
    , empty
    , emptyTable
    , encode
    , getLabel
    , getShortPathLabels
    , getShowGraph
    , insert
    , isTable
    , mapLabel
    , member
    , remove
    , toList
    , toggleShowGraph
    )

{-| Lenses are ways to visualise a subset of the data in a explorer run.
A Lens tells you how to see the data, it does not contain the data itself.
-}

import Dict exposing (Dict)
import Grid exposing (Grid)
import Json.Decode as Decode
import Json.Encode as Encode
import List.Extra
import Maybe.Extra
import Run exposing (Path)
import Set exposing (Set)


type alias ClassicData =
    { paths : Set Path
    , showGraph : Bool
    , guessedShortLabels : Dict Path String
    }


type VisualisationKind
    = Classic ClassicData
    | Table (Grid (Maybe Path))


type Lens
    = Lens
        { label : String
        , vkind : VisualisationKind
        }


type ShortenerInstruction
    = Skip String
    | Take


shorten : String -> List (List String) -> List String
shorten delim lists =
    let
        makeShortener : List ShortenerInstruction -> List (List String) -> List ShortenerInstruction
        makeShortener res ps =
            if List.any List.isEmpty ps then
                List.reverse res

            else
                case ps of
                    [] ->
                        List.reverse res

                    a :: rest ->
                        if List.all (\p -> List.head p == List.head a) rest then
                            makeShortener (Skip (List.head a |> Maybe.withDefault "") :: res) (List.map (List.drop 1) ps)

                        else
                            makeShortener (Take :: res) (List.map (List.drop 1) ps)

        shortener =
            makeShortener [] lists

        applyShortener : List ShortenerInstruction -> List String -> List String -> String
        applyShortener ins res list =
            case ( ins, list ) of
                ( [], _ ) ->
                    String.join delim (List.reverse res ++ list)

                ( _, [] ) ->
                    "CAN'T HAPPEN BECAUSE OF THE WAY SHORTENER IS CONSTRUCTED"

                ( (Skip s) :: insRest, _ :: listRest ) ->
                    applyShortener insRest res listRest

                ( Take :: insRest, l :: listRest ) ->
                    applyShortener insRest (l :: res) listRest
    in
    lists
        |> List.map (applyShortener shortener [])


mapLast : (a -> a) -> List a -> List a
mapLast f l =
    case List.Extra.unconsLast l of
        Nothing ->
            []

        Just ( x, prefix ) ->
            prefix ++ [ f x ]


{-| Sometimes we want to display shorter labels (e.g. in a chart), when all the labels are have a very similar
structure. This tries to guess short names.
-}
guessShortPathLabels : Set Path -> Dict Path String
guessShortPathLabels paths =
    case Set.toList paths of
        [ onlyOne ] ->
            -- If there is only one string, shorten would construct the empty string as
            -- the unambigous short version...
            Dict.singleton onlyOne (List.Extra.last onlyOne |> Maybe.withDefault "")

        pathList ->
            let
                shortLabels =
                    let
                        shortenedLastElements =
                            shorten "_"
                                (pathList
                                    |> List.map (String.split "_" << Maybe.withDefault "" << List.Extra.last)
                                )
                    in
                    shorten "."
                        (List.map2 (\l e -> mapLast (always e) l)
                            pathList
                            shortenedLastElements
                        )
            in
            Dict.fromList (List.map2 Tuple.pair pathList shortLabels)


getShortPathLabels : Lens -> Dict Path String
getShortPathLabels (Lens il) =
    case il.vkind of
        Classic { guessedShortLabels } ->
            guessedShortLabels

        Table _ ->
            -- TODO: Does this work?
            Dict.empty


mapClassic : (ClassicData -> ClassicData) -> Lens -> Lens
mapClassic fn (Lens i) =
    case i.vkind of
        Table _ ->
            Lens i

        Classic c ->
            Lens { i | vkind = Classic (fn c) }


mapKind :
    (ClassicData -> ClassicData)
    -> (Grid (Maybe Path) -> Grid (Maybe Path))
    -> Lens
    -> Lens
mapKind fnClassic fnTable (Lens i) =
    case i.vkind of
        Table t ->
            Lens { i | vkind = Table (fnTable t) }

        Classic c ->
            Lens { i | vkind = Classic (fnClassic c) }


updateShortPathLabels : Lens -> Lens
updateShortPathLabels =
    mapClassic
        (\c ->
            { c
                | guessedShortLabels = guessShortPathLabels c.paths
            }
        )


empty : Lens
empty =
    Lens
        { label = "data"
        , vkind =
            Classic
                { paths = Set.empty
                , showGraph = False
                , guessedShortLabels = Dict.empty
                }
        }


emptyTable : Lens
emptyTable =
    Lens
        { label = "data"
        , vkind =
            Table
                (Grid.repeat 2 2 Nothing)
        }


toggleShowGraph : Lens -> Lens
toggleShowGraph =
    mapClassic (\c -> { c | showGraph = not c.showGraph })


getShowGraph : Lens -> Bool
getShowGraph (Lens il) =
    case il.vkind of
        Classic c ->
            c.showGraph

        Table _ ->
            False


getLabel : Lens -> String
getLabel (Lens l) =
    l.label


mapLabel : (String -> String) -> Lens -> Lens
mapLabel f (Lens l) =
    Lens { l | label = f l.label }


remove : Path -> Lens -> Lens
remove p il =
    il
        |> mapKind
            (\c ->
                { c | paths = Set.remove p c.paths }
            )
            (Grid.map
                (\cell ->
                    if cell == Just p then
                        Nothing

                    else
                        cell
                )
            )
        |> updateShortPathLabels


addExtraRow : Grid (Maybe Path) -> Grid (Maybe Path)
addExtraRow g =
    let
        h =
            Grid.height g

        w =
            Grid.height g
    in
    Grid.initialize w
        (h + 1)
        (\x y ->
            Grid.get ( x, y ) g
                |> Maybe.Extra.join
        )


findInGrid : (Int -> Int -> Maybe Path -> Maybe x) -> Grid (Maybe Path) -> Maybe x
findInGrid fn g =
    findInGridHelper 0 0 fn g


findInGridHelper x y fn g =
    if y >= Grid.height g then
        Nothing

    else if x >= Grid.width g then
        findInGridHelper 0 (y + 1) fn g

    else
        case Grid.get ( x, y ) g of
            Nothing ->
                Nothing

            -- compiler happyness
            Just cell ->
                case fn x y cell of
                    Nothing ->
                        findInGridHelper (x + 1) y fn g

                    Just res ->
                        Just res


findEmptySpot : Grid (Maybe Path) -> Maybe ( Int, Int )
findEmptySpot g =
    findInGrid
        (\x y mp ->
            if mp == Nothing then
                Just ( x, y )

            else
                Nothing
        )
        g


insert : Path -> Lens -> Lens
insert p il =
    il
        |> mapKind
            (\c ->
                { c | paths = Set.insert p c.paths }
            )
            (\g ->
                case findEmptySpot g of
                    Nothing ->
                        let
                            h =
                                Grid.height g
                        in
                        Grid.set ( 0, h ) (Just p) (addExtraRow g)

                    Just spot ->
                        Grid.set spot (Just p) g
            )
        |> updateShortPathLabels


member : Path -> Lens -> Bool
member p (Lens i) =
    case i.vkind of
        Classic c ->
            Set.member p c.paths

        Table g ->
            findInGrid
                (\_ _ mp ->
                    if mp == Just p then
                        Just ()

                    else
                        Nothing
                )
                g
                /= Nothing


toList : Lens -> List Path
toList (Lens i) =
    case i.vkind of
        Classic c ->
            Set.toList c.paths

        Table g ->
            Grid.foldl
                (\cell l ->
                    case cell of
                        Nothing ->
                            l

                        Just c ->
                            c :: l
                )
                []
                g


encode : Lens -> Encode.Value
encode (Lens i) =
    let
        kindFields =
            case i.vkind of
                Classic c ->
                    [ ( "kind", Encode.string "classic" )
                    , ( "showGraph", Encode.bool c.showGraph )
                    , ( "paths", Encode.set (Encode.list Encode.string) c.paths )
                    ]

                Table g ->
                    let
                        encodeCell mp =
                            case mp of
                                Nothing ->
                                    Encode.null

                                Just p ->
                                    Encode.list Encode.string p
                    in
                    [ ( "kind", Encode.string "table" )
                    , ( "table"
                      , Grid.rows g
                            |> Encode.array (Encode.array encodeCell)
                      )
                    ]
    in
    Encode.object
        (( "label", Encode.string i.label ) :: kindFields)


isTable : Lens -> Maybe (Grid (Maybe Path))
isTable (Lens l) =
    case l.vkind of
        Classic _ ->
            Nothing

        Table g ->
            Just g


classicDecoder : Decode.Decoder ClassicData
classicDecoder =
    Decode.map2
        (\showGraph paths ->
            { paths = paths
            , showGraph = showGraph
            , guessedShortLabels = Dict.empty
            }
        )
        (Decode.field "showGraph" Decode.bool)
        (Decode.field "paths"
            (Decode.list (Decode.list Decode.string)
                |> Decode.map Set.fromList
            )
        )


tableDecoder : Decode.Decoder (Grid (Maybe Path))
tableDecoder =
    Decode.list (Decode.list (Decode.nullable (Decode.list Decode.string)))
        |> Decode.andThen
            (\l ->
                case Grid.fromList l of
                    Nothing ->
                        Decode.fail "invalid grid"

                    Just g ->
                        Decode.succeed g
            )


decoder : Decode.Decoder Lens
decoder =
    Decode.map2
        (\label vkind ->
            Lens { label = label, vkind = vkind }
                |> updateShortPathLabels
        )
        (Decode.field "label" Decode.string)
        (Decode.maybe (Decode.field "kind" Decode.string)
            |> Decode.map (Maybe.withDefault "table")
            |> Decode.andThen
                (\kind ->
                    case kind of
                        "classic" ->
                            classicDecoder
                                |> Decode.map Classic

                        "table" ->
                            tableDecoder
                                |> Decode.map Table

                        _ ->
                            Decode.fail "Invalid kind"
                )
        )
