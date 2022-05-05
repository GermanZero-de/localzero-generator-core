module Value exposing (Value(..), decoder)

import Json.Decode as Decode


type Value
    = Float Float
    | Null
    | String String


decoder : Decode.Decoder Value
decoder =
    Decode.oneOf
        [ Decode.float |> Decode.map Float
        , Decode.string |> Decode.map String
        , Decode.null Null
        ]
