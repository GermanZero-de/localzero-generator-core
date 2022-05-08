module Value exposing (Value(..), decoder, isEqual)

import Json.Decode as Decode


type Value
    = Float Float
    | Null
    | String String


isEqual : Value -> Value -> Bool
isEqual a b =
    case ( a, b ) of
        ( Null, Null ) ->
            True

        ( String sa, String sb ) ->
            sa == sb

        ( Float fa, Float fb ) ->
            case ( isNaN fa, isNaN fb ) of
                ( True, True ) ->
                    True

                ( False, True ) ->
                    False

                ( True, False ) ->
                    False

                ( False, False ) ->
                    abs (fb - fa) <= 1.0e-2

        ( Float _, Null ) ->
            False

        ( Float _, String _ ) ->
            False

        ( String _, Float _ ) ->
            False

        ( String _, Null ) ->
            False

        ( Null, Float _ ) ->
            False

        ( Null, String _ ) ->
            False


decoder : Decode.Decoder Value
decoder =
    Decode.oneOf
        [ Decode.float |> Decode.map Float
        , Decode.string |> Decode.map String
        , Decode.null Null
        ]
