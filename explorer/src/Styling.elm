module Styling exposing
    ( black
    , dangerousIconButton
    , emptyCellColor
    , floatingActionButton
    , fonts
    , formatGermanNumber
    , germanZeroGreen
    , germanZeroYellow
    , icon
    , iconButton
    , iconButtonStyle
    , modalDim
    , parseGermanNumber
    , red
    , runColorForChart
    , runColorForUI
    , scrollableText
    , size16
    , size32
    , sizes
    , treeElementStyle
    , white
    )

import AllRuns exposing (RunId)
import Array
import Element
    exposing
        ( Element
        , centerY
        , fill
        , height
        , padding
        , paragraph
        , scrollbarY
        , text
        , width
        )
import Element.Background as Background
import Element.Border as Border
import Element.Font as Font
import Element.Input as Input
import FeatherIcons
import FormatNumber exposing (format)
import FormatNumber.Locales exposing (spanishLocale)
import Hex


scrollableText : String -> Element msg
scrollableText s =
    -- Here we recover the line information and put each line into
    -- a separate paragraph
    -- Also error messages are sometimes formatted so we replace
    -- consecutive spaces by spaces followed by nbsp spaces
    Element.column [ width fill, height fill, scrollbarY ]
        (String.lines s
            |> List.map
                (\l ->
                    paragraph [ width fill ]
                        [ text (String.replace "  " " \u{00A0}" l) ]
                )
        )


germanLocale =
    { spanishLocale | decimals = 2 }


formatGermanNumber : Float -> String
formatGermanNumber f =
    format germanLocale f


parseGermanNumber : String -> Maybe Float
parseGermanNumber s =
    s
        |> String.replace "." ""
        -- ignore . (thousands separator)
        |> String.replace "," "."
        -- make it look like an english number
        |> String.toFloat


sizes : { small : Int, tableGap : Int, medium : Int, large : Int, tableFontSize : Int, fontSize : Int }
sizes =
    { small = 4
    , tableGap = 5
    , medium = 8
    , large = 12
    , tableFontSize = 14
    , fontSize = 24
    }


fonts =
    { explorer = [ Font.size sizes.fontSize ]
    , explorerItems = [ Font.size 16 ]
    , explorerValues = [ Font.size 16, Font.family [ Font.monospace ] ]
    , explorerNodeSize = [ Font.size 16 ]
    , table = [ Font.size sizes.tableFontSize ]
    , smallTextButton = [ Font.size 12 ]
    }


modalDim : Element.Color
modalDim =
    Element.rgba255 128 128 128 0.8


shadowColor : Element.Color
shadowColor =
    Element.rgba255 100 100 100 0.6


emptyCellColor : Element.Color
emptyCellColor =
    Element.rgb255 240 240 240


germanZeroYellow : Element.Color
germanZeroYellow =
    Element.rgb255 254 189 17


germanZeroGreen : Element.Color
germanZeroGreen =
    Element.rgb255 148 211 86


red : Element.Color
red =
    Element.rgb255 197 40 61


black : Element.Color
black =
    Element.rgb255 0 0 0


white : Element.Color
white =
    Element.rgb255 255 255 255


buttonStyle : List (Element.Attribute msg)
buttonStyle =
    [ padding sizes.small
    , Border.width 1
    , Border.rounded 4
    , Border.color germanZeroGreen
    , Element.mouseOver
        [ Border.color germanZeroYellow
        ]
    , Element.focused [ Border.color germanZeroYellow ]
    ]


treeElementStyle : List (Element.Attribute msg)
treeElementStyle =
    [ padding sizes.small
    , Element.focused []
    , Element.mouseOver []
    ]


size16 : FeatherIcons.Icon -> FeatherIcons.Icon
size16 =
    FeatherIcons.withSize 16


size32 : FeatherIcons.Icon -> FeatherIcons.Icon
size32 =
    FeatherIcons.withSize 32


icon : FeatherIcons.Icon -> Element msg
icon i =
    i
        |> FeatherIcons.toHtml []
        |> Element.html


iconButtonStyle : List (Element.Attribute msg)
iconButtonStyle =
    [ Font.color germanZeroGreen
    , Element.mouseOver [ Font.color germanZeroYellow ]
    , Element.focused [ Border.color germanZeroYellow ]
    , centerY
    ]


iconButtonWithStyle : List (Element.Attribute msg) -> FeatherIcons.Icon -> msg -> Element msg
iconButtonWithStyle style i onPress =
    Input.button style
        { label = icon i
        , onPress = Just onPress
        }


floatingActionButton : FeatherIcons.Icon -> msg -> Element msg
floatingActionButton i onPress =
    let
        size =
            40

        paddingSize =
            size // 8

        iconSize =
            size - 2 * paddingSize
    in
    iconButtonWithStyle
        [ Font.color white
        , Background.color germanZeroGreen
        , Element.mouseOver [ Background.color germanZeroYellow ]
        , Element.focused [ Background.color germanZeroYellow ]
        , Border.rounded (size // 2)
        , Border.shadow { offset = ( 1, 1 ), size = 2, blur = 1, color = shadowColor }
        , Element.alignBottom
        , Element.alignRight
        , Element.moveUp 10
        , Element.moveLeft 10
        , padding paddingSize
        ]
        (FeatherIcons.withSize (toFloat iconSize) i)
        onPress


iconButton : FeatherIcons.Icon -> msg -> Element msg
iconButton i onPress =
    iconButtonWithStyle iconButtonStyle i onPress


dangerousIconButtonStyle : List (Element.Attribute msg)
dangerousIconButtonStyle =
    [ Font.color red
    , Element.mouseOver [ Font.color germanZeroYellow ]
    , Element.focused [ Border.color germanZeroYellow ]
    , centerY
    ]


dangerousIconButton : FeatherIcons.Icon -> msg -> Element msg
dangerousIconButton i op =
    iconButtonWithStyle
        dangerousIconButtonStyle
        i
        op


runColor : RunId -> ( Int, Int, Int )
runColor =
    let
        -- I'm basically assuming that we never compare more
        -- than the below number of runs simultaneously
        -- and even that you don't add and remove runs
        -- a lot (because than you would run into the same
        -- colors again).
        -- But then if they do happen again, it's still very
        -- unlikely they will end up next to each other
        -- so this should be fine
        colors =
            Array.fromList
                [ -- pink
                  ( 0xEA, 0x60, 0xDF )
                , -- purple
                  ( 0x7B, 0x4D, 0xFF )
                , -- blue
                  ( 0x12, 0xA5, 0xED )
                , -- moss
                  ( 0x92, 0xB4, 0x2C )
                , -- brown
                  ( 0x87, 0x1C, 0x1C )
                , -- mint
                  ( 0x6D, 0xF0, 0xD2 )
                , -- coral
                  ( 0xEA, 0x73, 0x69 )
                , -- turquoise
                  ( 0x22, 0xD2, 0xBA )
                , -- magenta
                  ( 0xDB, 0x4C, 0xB2 )
                ]

        numColors =
            Array.length colors
    in
    \runId ->
        Array.get (remainderBy numColors (runId - 1)) colors
            -- can't happen because of the remainderBy
            |> Maybe.withDefault ( 0, 0, 0 )


runColorForChart : RunId -> String
runColorForChart ri =
    let
        ( r, g, b ) =
            runColor ri
    in
    String.concat
        [ "#", Hex.toString r, Hex.toString g, Hex.toString b ]


runColorForUI : RunId -> Element.Color
runColorForUI ri =
    let
        ( r, g, b ) =
            runColor ri
    in
    Element.rgb255 r g b
