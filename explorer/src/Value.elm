module Value exposing
    ( BinaryOp(..)
    , MaybeWithTrace
    , Trace(..)
    , UnaryOp(..)
    , Value(..)
    , binaryTraceToList
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
    = DataTrace { source : String, key : String, attr : String, value : Float }
    | FactOrAssTrace { fact_or_ass : String, value : Float }
    | NameTrace { name : String }
    | BinaryTrace { value : Float, binary : BinaryOp, a : Trace, b : Trace }
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


binaryTraceToList : { binary : BinaryOp, a : Trace, b : Trace, value : Float } -> List Trace
binaryTraceToList { binary, a, b } =
    let
        helper leftChild acc =
            case leftChild of
                BinaryTrace bNested ->
                    if bNested.binary == binary then
                        helper bNested.a (bNested.b :: acc)

                    else
                        leftChild :: acc

                _ ->
                    leftChild :: acc
    in
    helper a [ b ]


traceDecoder : String -> Decode.Decoder Trace
traceDecoder namePrefix =
    Decode.lazy
        (\() ->
            Decode.oneOf
                [ Decode.float |> Decode.map LiteralTrace
                , dataTraceDecoder
                , factOrAssTraceDecoder
                , binaryTraceDecoder namePrefix
                , nameTraceDecoder namePrefix
                , unaryTraceDecoder namePrefix
                ]
        )


dataTraceDecoder : Decode.Decoder Trace
dataTraceDecoder =
    Decode.map4 (\s k a v -> DataTrace { source = s, key = k, attr = a, value = v })
        (Decode.field "source" Decode.string)
        (Decode.field "key" (Decode.oneOf [ Decode.string, Decode.int |> Decode.map String.fromInt ]))
        (Decode.field "attr" Decode.string)
        (Decode.field "value" Decode.float)


factOrAssTraceDecoder : Decode.Decoder Trace
factOrAssTraceDecoder =
    Decode.map2 (\s v -> FactOrAssTrace { fact_or_ass = s, value = v })
        (Decode.field "fact_or_ass" Decode.string)
        (Decode.field "value" Decode.float)


nameTraceDecoder : String -> Decode.Decoder Trace
nameTraceDecoder namePrefix =
    Decode.field "name" Decode.string
        |> Decode.map (\s -> NameTrace { name = namePrefix ++ "." ++ s })


binaryTraceDecoder : String -> Decode.Decoder Trace
binaryTraceDecoder namePrefix =
    Decode.map4 (\o a b v -> BinaryTrace { value = v, binary = o, a = a, b = b })
        (Decode.field "binary" binaryOpDecoder)
        (Decode.field "a" <| traceDecoder namePrefix)
        (Decode.field "b" <| traceDecoder namePrefix)
        (Decode.field "value" Decode.float)


unaryTraceDecoder : String -> Decode.Decoder Trace
unaryTraceDecoder namePrefix =
    Decode.map2 (\o a -> UnaryTrace { unary = o, a = a })
        (Decode.field "unary" unaryOpDecoder)
        (Decode.field "a" <| traceDecoder namePrefix)


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


maybeWithTraceDecoder : String -> Decode.Decoder MaybeWithTrace
maybeWithTraceDecoder namePrefix =
    Decode.oneOf
        [ decoder
            |> Decode.map (\v -> { value = v, trace = Nothing })
        , Decode.map2 (\v t -> { value = v, trace = Just t })
            (Decode.field "value" decoder)
            (Decode.field "trace" <| traceDecoder namePrefix)
        ]
