module Value exposing
    ( MaybeWithTrace
    , Trace(..)
    , Value(..)
    , BinaryOp(..)
    , UnaryOp(..)
    , decoder
    , defaultTolerance
    , isEqual
    , isValueEqual
    , maybeWithTraceDecoder
    , minimumTolerance
    )

import Json.Decode as Decode


type Value
    = Float Float
    | Null
    | String String


type alias MaybeWithTrace =
    { value : Value, trace : Maybe Trace }


type Trace
    = DataTrace { source : String, key : String, attr : String }
    | FactOrAssTrace { fact_or_ass : String }
    | NameTrace { name : String }
    | BinaryTrace { binary : BinaryOp, a : Trace, b : Trace }
    | UnaryTrace { unary : UnaryOp, a : Trace }
    | LiteralTrace Float


type BinaryOp
    = Plus
    | Minus
    | Divide
    | Times


type UnaryOp
    = UnaryMinus
    | UnaryPlus


traceDecoder : Decode.Decoder Trace
traceDecoder =
    Decode.lazy
        (\() ->
            Decode.oneOf
                [ Decode.float |> Decode.map LiteralTrace
                , dataTraceDecoder
                , factOrAssTraceDecoder
                , binaryTraceDecoder
                , nameTraceDecoder
                , unaryTraceDecoder
                ]
        )


dataTraceDecoder : Decode.Decoder Trace
dataTraceDecoder =
    Decode.map3 (\s k a -> DataTrace { source = s, key = k, attr = a })
        (Decode.field "source" Decode.string)
        (Decode.field "key" (Decode.oneOf [ Decode.string, Decode.int |> Decode.map String.fromInt ]))
        (Decode.field "attr" Decode.string)


factOrAssTraceDecoder : Decode.Decoder Trace
factOrAssTraceDecoder =
    Decode.field "fact_or_ass" Decode.string
        |> Decode.map (\s -> FactOrAssTrace { fact_or_ass = s })


nameTraceDecoder : Decode.Decoder Trace
nameTraceDecoder =
    Decode.field "name" Decode.string
        |> Decode.map (\s -> NameTrace { name = s })


binaryTraceDecoder : Decode.Decoder Trace
binaryTraceDecoder =
    Decode.map3 (\o a b -> BinaryTrace { binary = o, a = a, b = b })
        (Decode.field "binary" binaryOpDecoder)
        (Decode.field "a" traceDecoder)
        (Decode.field "b" traceDecoder)


unaryTraceDecoder : Decode.Decoder Trace
unaryTraceDecoder =
    Decode.map2 (\o a -> UnaryTrace { unary = o, a = a })
        (Decode.field "unary" unaryOpDecoder)
        (Decode.field "a" traceDecoder)


unaryOpDecoder : Decode.Decoder UnaryOp
unaryOpDecoder =
    Decode.string
        |> Decode.andThen
            (\s ->
                case s of
                    "+" ->
                        Decode.succeed UnaryPlus

                    "-" ->
                        Decode.succeed UnaryMinus

                    _ ->
                        Decode.fail "not a valid unary op"
            )


binaryOpDecoder : Decode.Decoder BinaryOp
binaryOpDecoder =
    Decode.string
        |> Decode.andThen
            (\s ->
                case s of
                    "+" ->
                        Decode.succeed Plus

                    "-" ->
                        Decode.succeed Minus

                    "*" ->
                        Decode.succeed Times

                    "/" ->
                        Decode.succeed Divide

                    _ ->
                        Decode.fail "not a valid binary op"
            )


minimumTolerance : Float
minimumTolerance =
    1.0e-2


defaultTolerance : Float
defaultTolerance =
    minimumTolerance


isValueEqual : Float -> MaybeWithTrace -> MaybeWithTrace -> Bool
isValueEqual tolerance a b =
    isEqual tolerance a.value b.value


isEqual : Float -> Value -> Value -> Bool
isEqual tolerance a b =
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
                    let
                        d =
                            abs (fb - fa)
                    in
                    d <= max (tolerance * max (abs fa) (abs fb)) 1.0e-12

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


maybeWithTraceDecoder : Decode.Decoder MaybeWithTrace
maybeWithTraceDecoder =
    Decode.oneOf
        [ decoder
            |> Decode.map (\v -> { value = v, trace = Nothing })
        , Decode.map2 (\v t -> { value = v, trace = Just t })
            (Decode.field "value" decoder)
            (Decode.field "trace" traceDecoder)
        ]
