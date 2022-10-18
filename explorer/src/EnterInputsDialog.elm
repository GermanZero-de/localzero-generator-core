module EnterInputsDialog exposing (State, init, view)

import AgsIndex exposing (AgsIndex)
import Element
    exposing
        ( Element
        , column
        , el
        , fill
        , height
        , minimum
        , padding
        , px
        , row
        , scrollbarY
        , shrink
        , spacing
        , text
        , width
        )
import Element.Background as Background
import Element.Border as Border
import Element.Events as Events
import Element.Font as Font
import Element.Input as Input
import FeatherIcons
import GeneratorRpc
import Run
import Styling exposing (black, iconButton, size32, sizes)


type alias State =
    { agsFilter : String
    , year : Int
    , filteredAgs : List GeneratorRpc.AgsData
    , agsIndex : AgsIndex
    }


init : Int -> String -> AgsIndex -> State
init year agsFilter agsIndex =
    { agsFilter = agsFilter
    , year = year
    , filteredAgs = AgsIndex.lookup agsFilter agsIndex
    , agsIndex = agsIndex
    }


view : (State -> a) -> (Run.Inputs -> a) -> State -> Element a
view updateStateMsg okClickedMsg state =
    let
        labelStyle =
            [ Font.alignRight, width (minimum 100 shrink) ]
    in
    column
        [ width fill
        , height fill
        , spacing sizes.medium
        ]
        [ Input.text []
            { label = Input.labelLeft labelStyle (text "AGS")
            , text = state.agsFilter
            , onChange =
                \newFilter ->
                    updateStateMsg (init state.year newFilter state.agsIndex)
            , placeholder = Nothing
            }
        , el
            [ width fill
            , height (minimum 0 fill)
            , Border.solid
            , Border.width 1
            , Border.color black
            , padding sizes.medium
            ]
          <|
            if List.length state.filteredAgs > 2000 then
                text "Enter a AGS (e.g. 08416041) or City name (e.g. Tübingen)"

            else
                column
                    [ width fill
                    , height fill
                    , padding sizes.medium
                    , spacing sizes.medium
                    , scrollbarY
                    ]
                    (state.filteredAgs
                        |> List.map
                            (\a ->
                                row
                                    ([ width fill
                                     , spacing sizes.medium
                                     , Events.onClick (updateStateMsg (init state.year a.ags state.agsIndex))
                                     ]
                                        ++ (case state.filteredAgs of
                                                [ _ ] ->
                                                    [ Border.rounded 4
                                                    , Background.color Styling.germanZeroYellow
                                                    , Font.color Styling.white
                                                    , padding sizes.small
                                                    ]

                                                _ ->
                                                    []
                                           )
                                    )
                                    [ text a.ags
                                    , text a.desc
                                    ]
                            )
                    )
        , Input.slider
            [ height (px 20)
            , Element.behindContent
                (el
                    [ width fill
                    , height (px 2)
                    , Element.centerY
                    , Background.color Styling.germanZeroGreen
                    , Border.rounded 2
                    ]
                    Element.none
                )
            ]
            { label = Input.labelLeft labelStyle (text (String.fromInt state.year))
            , min = 2025
            , max = 2050
            , step = Just 1.0
            , onChange = \year -> updateStateMsg { state | year = round year }
            , value = toFloat state.year
            , thumb = Input.defaultThumb
            }
        , case state.filteredAgs of
            [ exactlyOne ] ->
                iconButton (size32 FeatherIcons.check) (okClickedMsg { year = state.year, ags = exactlyOne.ags })

            _ ->
                text "Enter a valid AGS first!"
        ]
