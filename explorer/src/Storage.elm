module Storage exposing (Storage, decoder, encode)

import Json.Decode as Decode
import Json.Encode as Encode
import Lens exposing (Lens)


type alias Storage =
    { interestLists : List Lens
    }


encodeV1 : Storage -> Encode.Value
encodeV1 { interestLists } =
    Encode.object
        [ ( "version", Encode.int 1 )
        , ( "interestLists", Encode.list Lens.encode interestLists )
        ]


encode : Storage -> Encode.Value
encode s =
    encodeV1 s


v1Decoder : Decode.Decoder Storage
v1Decoder =
    Decode.field "interestLists" (Decode.list Lens.decoder)
        |> Decode.map (\l -> { interestLists = l })


decoder : Decode.Decoder Storage
decoder =
    Decode.field "version" Decode.int
        |> Decode.andThen
            (\v ->
                case v of
                    1 ->
                        v1Decoder

                    _ ->
                        Decode.fail ("unknown version number " ++ String.fromInt v ++ " encountered ")
            )
