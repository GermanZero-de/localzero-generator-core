module Styling exposing
    ( black
    , dangerousIconButton
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
    , size16
    , size32
    , sizes
    , treeElementStyle
    , white
    )

import Element exposing (Element, padding)
import Element.Background as Background
import Element.Border as Border
import Element.Font as Font
import Element.Input as Input
import FeatherIcons
import FormatNumber exposing (format)
import FormatNumber.Locales exposing (spanishLocale)


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


sizes : { small : Int, medium : Int, large : Int }
sizes =
    { small = 4
    , medium = 8
    , large = 12
    }


fonts =
    { explorer = [ Font.size 24 ]
    , explorerItems = [ Font.size 16 ]
    , explorerValues = [ Font.size 16, Font.family [ Font.monospace ] ]
    , explorerNodeSize = [ Font.size 16 ]
    }


modalDim : Element.Color
modalDim =
    Element.rgba255 128 128 128 0.8


shadowColor : Element.Color
shadowColor =
    Element.rgba255 100 100 100 0.6


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
    ]


dangerousIconButton : FeatherIcons.Icon -> msg -> Element msg
dangerousIconButton i op =
    iconButtonWithStyle
        dangerousIconButtonStyle
        i
        op
