module AgsIndex exposing (AgsIndex, init, lookup)

import Dict exposing (Dict)
import GeneratorRpc exposing (AgsData)
import Html exposing (a)


type AgsIndex
    = AgsIndex
        { byFirstChar : Dict Char (List { lower : AgsData, normal : AgsData })
        , all : List AgsData
        }


init : List AgsData -> AgsIndex
init agsDataList =
    let
        add get agsRecord acc =
            case String.uncons (get agsRecord.lower) of
                Nothing ->
                    acc

                Just ( ch, _ ) ->
                    acc
                        |> Dict.update ch
                            (\existing ->
                                Just (agsRecord :: Maybe.withDefault [] existing)
                            )

        byFirstChar =
            List.foldl
                (\agsData acc ->
                    let
                        agsRecord =
                            { normal = agsData
                            , lower =
                                { ags = agsData.ags
                                , short = String.toLower agsData.short
                                , desc = String.toLower agsData.desc
                                }
                            }
                    in
                    acc
                        |> add .ags agsRecord
                        |> add .desc agsRecord
                )
                Dict.empty
                agsDataList
                |> Dict.map (\_ l -> List.sortBy (.lower >> .desc) l)
    in
    AgsIndex
        { byFirstChar = byFirstChar
        , all = agsDataList |> List.sortBy .desc
        }


lookup : String -> AgsIndex -> List AgsData
lookup filter (AgsIndex { byFirstChar, all }) =
    let
        lFilter =
            String.toLower filter
    in
    case String.uncons lFilter of
        Nothing ->
            all

        Just ( firstChar, _ ) ->
            case Dict.get firstChar byFirstChar of
                Nothing ->
                    []

                Just candidates ->
                    candidates
                        |> List.filterMap
                            (\a ->
                                if String.startsWith lFilter a.normal.ags || String.startsWith lFilter a.lower.desc then
                                    Just a.normal

                                else
                                    Nothing
                            )
