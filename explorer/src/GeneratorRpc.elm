module GeneratorRpc exposing (calculate, makeEntries)

import Json.Encode as Encode
import JsonRpc
import Run
import Tree exposing (Tree)
import Value


apiUrl : String
apiUrl =
    "http://localhost:4070/api/v0"


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
