module GeneratorRpc exposing (AgsData, calculate, listAgs, makeEntries)

import Json.Decode as Decode
import Json.Encode as Encode
import JsonRpc
import Run
import Tree exposing (Tree)
import Value


type alias AgsData =
    { ags : String, desc : String, short : String }


apiUrl : String
apiUrl =
    "http://localhost:4070/api/v0"


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
            ]
        }
        (Tree.decoder (Value.maybeWithTraceDecoder "result"))
        toMsg
