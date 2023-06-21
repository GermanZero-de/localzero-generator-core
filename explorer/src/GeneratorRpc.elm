module GeneratorRpc exposing (AgsData, Info, calculate, info, listAgs, makeEntries)

import Json.Decode as Decode
import Json.Encode as Encode
import JsonRpc
import Run
import Tree exposing (Tree)
import Value


type alias AgsData =
    { ags : String, desc : String, short : String }

type alias Info =
    {
        label: String,
        group: String,
        description: String,
        value: Float,
        unit: String,
        rationale: String,
        reference: String,
        link: String
    }

infoDecoder : Decode.Decoder Info
infoDecoder =
    Decode.map8 Info
        (Decode.field "label" Decode.string)
        (Decode.field "group" Decode.string)
        (Decode.field "description" Decode.string)
        (Decode.field "value" Decode.float)
        (Decode.field "unit" Decode.string)
        (Decode.field "rationale" Decode.string)
        (Decode.field "reference" Decode.string)
        (Decode.field "link" Decode.string)

apiUrl : String
apiUrl =
    "/localzero/api/v0/"


agsDataDecoder : Decode.Decoder AgsData
agsDataDecoder =
    Decode.map3 (\ags desc short -> { ags = ags, desc = desc, short = short })
        (Decode.field "ags" Decode.string)
        (Decode.field "desc" Decode.string)
        (Decode.field "short" Decode.string)


listAgs : { toMsg : JsonRpc.RpcData (List AgsData) -> msg } -> Cmd msg
listAgs { toMsg } =
    JsonRpc.call
        { url = apiUrl
        , token = Nothing
        , method = "list-ags"
        , params =
            []
        }
        (Decode.list agsDataDecoder)
        toMsg


makeEntries : { inputs : Run.Inputs, toMsg : JsonRpc.RpcData Run.Entries -> msg } -> Cmd msg
makeEntries { inputs, toMsg } =
    JsonRpc.call
        { url = apiUrl
        , token = Nothing
        , method = "make-entries"
        , params =
            [ ( "ags", Encode.string inputs.ags )
            , ( "year", Encode.int inputs.year )
            , ( "trace", Encode.bool True )
            ]
        }
        Run.entriesDecoder
        toMsg


calculate : { inputs : Run.Inputs, overrides : Run.Overrides, toMsg : JsonRpc.RpcData (Tree Value.MaybeWithTrace) -> msg } -> Cmd msg
calculate { inputs, overrides, toMsg } =
    JsonRpc.call
        { url = apiUrl
        , token = Nothing
        , method = "calculate"
        , params =
            [ ( "ags", Encode.string inputs.ags )
            , ( "year", Encode.int inputs.year )
            , ( "overrides", Run.encodeOverrides overrides )
            , ( "trace", Encode.bool True )
            ]
        }
        (Tree.decoder (Value.maybeWithTraceDecoder "result"))
        toMsg

info : { name: String, toMsg : JsonRpc.RpcData Info -> msg } -> Cmd msg
info { name, toMsg } =
    JsonRpc.call
        { url = apiUrl
        , token = Nothing
        , method = "info"
        , params =
            [ ( "key", Encode.string name)]
        }
        infoDecoder
        toMsg
