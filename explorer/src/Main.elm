module Main exposing (Model, Msg(..), init, main, subscriptions, update, view)

--import Element.Background as Background

import GeneratorRuns
    exposing
        ( AbsolutePath
        , GeneratorRuns
        , Inputs
        , InputsAndResult
        , Path
        )
import Array exposing (Array)
import Browser
import Chart as C
import Chart.Attributes as CA
import CollapseStatus exposing (CollapseStatus, allCollapsed, isCollapsed, toggle)
import Dict
import Element
    exposing
        ( Element
        , alignTop
        , centerX
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
import Element.Font as Font
import Element.Input as Input
import Element.Keyed
import FeatherIcons
import FormatNumber exposing (format)
import FormatNumber.Locales exposing (spanishLocale)
import GeneratorResult exposing (GeneratorResult, Node(..), Tree)
import Html exposing (Html)
import Http
import Set exposing (Set)


germanLocale =
    { spanishLocale | decimals = 2 }



-- MAIN


main =
    Browser.element
        { init = init
        , update = update
        , subscriptions = subscriptions
        , view = view
        }


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


icon : FeatherIcons.Icon -> Element msg
icon i =
    i
        |> FeatherIcons.toHtml []
        |> Element.html


iconButtonStyle : List (Element.Attribute msg)
iconButtonStyle =
    [ padding sizes.small
    , Font.color germanZeroGreen
    , Element.mouseOver [ Font.color germanZeroYellow ]
    , Element.focused [ Border.color germanZeroYellow ]
    ]


iconButtonWithStyle : List (Element.Attribute Msg) -> FeatherIcons.Icon -> Msg -> Element Msg
iconButtonWithStyle style i onPress =
    Input.button style
        { label = icon i
        , onPress = Just onPress
        }


iconButton : FeatherIcons.Icon -> Msg -> Element Msg
iconButton i onPress =
    iconButtonWithStyle iconButtonStyle i onPress


dangerousIconButtonStyle : List (Element.Attribute Msg)
dangerousIconButtonStyle =
    [ padding sizes.small
    , Font.color red
    , Element.mouseOver [ Font.color germanZeroYellow ]
    , Element.focused [ Border.color germanZeroYellow ]
    ]


dangerousIconButton : FeatherIcons.Icon -> Msg -> Element Msg
dangerousIconButton i op =
    iconButtonWithStyle
        dangerousIconButtonStyle
        i
        op



-- MODEL


type alias Model =
    { results : GeneratorRuns
    , collapseStatus : CollapseStatus
    , interestList : Set Path
    , showModal : Maybe ModalState
    }


type ModalState
    = PrepareCalculate (Maybe Int) Inputs
    | Loading
    | LoadFailure String




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


initiateLoad : Maybe Int -> Inputs -> Model -> ( Model, Cmd Msg )
initiateLoad maybeNdx inputs model =
    ( { model | showModal = Just Loading }
    , Http.get
        { url = "http://localhost:4070/calculate/" ++ inputs.ags ++ "/" ++ String.fromInt inputs.year
        , expect = Http.expectJson (GotGeneratorResult maybeNdx inputs) GeneratorResult.decoder
        }
    )


init : () -> ( Model, Cmd Msg )
init _ =
    ( { results = GeneratorRuns.empty
      , showModal = Nothing
      , interestList = Set.empty
      , collapseStatus = allCollapsed
      }
    , Cmd.none
    )



-- UPDATE


type Msg
    = GotGeneratorResult (Maybe Int) Inputs (Result Http.Error GeneratorResult)
      --| AddItemToChartClicked { path : Path, value : Float }
    | AddToInterestList Path
    | RemoveFromInterestList Path
    | CollapseToggleRequested AbsolutePath
    | UpdateModal ModalMsg
    | DisplayCalculateModalPressed (Maybe Int) (Maybe Inputs)
    | CalculateModalOkPressed (Maybe Int) Inputs
    | RemoveResult Int


type ModalMsg
    = CalculateModalTargetYearUpdated Int
    | CalculateModalAgsUpdated String


type alias InterestListTable =
    List ( Path, Array (Maybe Float) )


getInterestList : Model -> InterestListTable
getInterestList model =
    Set.toList model.interestList
        |> List.map
            (\path ->
                ( path
                , Array.initialize (GeneratorRuns.size model.results)
                    (\n ->
                        GeneratorRuns.getValue ( n, path ) model.results
                    )
                )
            )


withLoadFailure : String -> Model -> ( Model, Cmd Msg )
withLoadFailure msg model =
    ( { model | showModal = Just (LoadFailure msg) }, Cmd.none )


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        GotGeneratorResult maybeNdx inputs resultOrError ->
            case resultOrError of
                Ok result ->
                    let
                        inputsAndResult =
                            { inputs = inputs, result = result }

                        newResults =
                            case maybeNdx of
                                Nothing ->
                                    GeneratorRuns.add inputsAndResult model.results

                                Just ndx ->
                                    GeneratorRuns.set ndx inputsAndResult model.results
                    in
                    ( { model
                        | results = newResults
                        , showModal = Nothing
                      }
                    , Cmd.none
                    )

                Err (Http.BadUrl s) ->
                    model
                        |> withLoadFailure ("BAD URL: " ++ s)

                Err Http.Timeout ->
                    model
                        |> withLoadFailure "TIMEOUT"

                Err Http.NetworkError ->
                    model
                        |> withLoadFailure "NETWORK ERROR"

                Err (Http.BadStatus code) ->
                    model
                        |> withLoadFailure ("BAD STATUS CODE" ++ String.fromInt code)

                Err (Http.BadBody error) ->
                    model
                        |> withLoadFailure ("Failed to decode: " ++ error)

        CollapseToggleRequested path ->
            ( { model | collapseStatus = CollapseStatus.toggle path model.collapseStatus }
            , Cmd.none
            )

        UpdateModal modalMsg ->
            updateModal modalMsg model.showModal
                |> Tuple.mapFirst (\md -> { model | showModal = md })
                |> Tuple.mapSecond (Cmd.map UpdateModal)

        DisplayCalculateModalPressed maybeNdx maybeInputs ->
            let
                inputs =
                    case maybeInputs of
                        Nothing ->
                            { ags = "", year = 2035 }

                        Just i ->
                            i

                modal =
                    PrepareCalculate maybeNdx inputs
            in
            ( { model | showModal = Just modal }
            , Cmd.none
            )

        CalculateModalOkPressed maybeNdx inputs ->
            model
                |> initiateLoad maybeNdx inputs

        AddToInterestList path ->
            ( { model | interestList = Set.insert path model.interestList }
            , Cmd.none
            )

        RemoveFromInterestList path ->
            ( { model | interestList = Set.remove path model.interestList }
            , Cmd.none
            )

        RemoveResult ndx ->
            ( { model | results = GeneratorRuns.remove ndx model.results }
            , Cmd.none
            )


updateModal : ModalMsg -> Maybe ModalState -> ( Maybe ModalState, Cmd ModalMsg )
updateModal msg model =
    case model of
        Nothing ->
            ( Nothing, Cmd.none )

        Just (PrepareCalculate ndx inputs) ->
            case msg of
                CalculateModalAgsUpdated a ->
                    ( Just (PrepareCalculate ndx { inputs | ags = a }), Cmd.none )

                CalculateModalTargetYearUpdated y ->
                    ( Just (PrepareCalculate ndx { inputs | year = y }), Cmd.none )

        Just Loading ->
            ( Just Loading, Cmd.none )

        Just (LoadFailure f) ->
            ( Just <| LoadFailure f, Cmd.none )



-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none



-- VIEW


viewChart : InterestListTable -> Element Msg
viewChart interestList =
    let
        widthChart =
            800

        heightChart =
            600

        bars =
            case interestList of
                [] ->
                    []

                ( _, row ) :: _ ->
                    List.range 0 (Array.length row - 1)
                        |> List.map
                            (\ndx ->
                                let
                                    get ( _, a ) =
                                        Array.get ndx a
                                            |> Maybe.andThen identity
                                            |> Maybe.withDefault 0.0
                                in
                                C.bar get []
                                    |> C.named (String.fromInt ndx)
                            )

        chart =
            C.chart
                [ CA.height heightChart
                , CA.width widthChart
                ]
                [ C.xTicks []
                , C.yTicks []
                , C.yLabels []
                , C.xAxis []
                , C.yAxis []
                , C.bars [] bars interestList
                , C.binLabels (String.join "." << Tuple.first) [ CA.moveDown 40 ]
                , C.legendsAt .max
                    .max
                    [ CA.column
                    , CA.moveLeft 5
                    , CA.alignRight
                    , CA.spacing 5
                    ]
                    []
                ]
    in
    el
        [ width (px widthChart)
        , height (px heightChart)
        , padding (2 * sizes.large)
        , alignTop
        , centerX
        ]
        (Element.html chart)


collapsedStatusIcon : AbsolutePath -> CollapseStatus -> Element Msg
collapsedStatusIcon path collapsed =
    let
        i =
            if isCollapsed path collapsed then
                FeatherIcons.chevronRight

            else
                FeatherIcons.chevronDown
    in
    el iconButtonStyle (icon i)


viewTree : Int -> Path -> CollapseStatus -> Set Path -> Tree -> Element Msg
viewTree resultNdx path collapseStatus interestList tree =
    if isCollapsed ( resultNdx, path ) collapseStatus then
        Element.none

    else
        Dict.toList tree
            |> List.map
                (\( name, val ) ->
                    let
                        itemRow content =
                            row
                                ([ spacing sizes.large, width fill ] ++ treeElementStyle)
                                content

                        childPath =
                            path ++ [ name ]

                        element =
                            case val of
                                Tree child ->
                                    column [ width fill ]
                                        [ Input.button [ width fill, Element.focused [] ]
                                            { label =
                                                itemRow
                                                    [ collapsedStatusIcon ( resultNdx, childPath ) collapseStatus
                                                    , el [ width fill ] (text name)
                                                    , el (Font.alignRight :: fonts.explorerNodeSize) <|
                                                        text (String.fromInt (Dict.size child))
                                                    ]
                                            , onPress = Just (CollapseToggleRequested ( resultNdx, path ++ [ name ] ))
                                            }
                                        , viewTree resultNdx childPath collapseStatus interestList child
                                        ]

                                Leaf Nothing ->
                                    itemRow
                                        [ el [ width fill ] (text name)
                                        , el (Font.alignRight :: fonts.explorerValues) <| text "null"
                                        ]

                                Leaf (Just f) ->
                                    let
                                        button =
                                            if Set.member childPath interestList then
                                                dangerousIconButton FeatherIcons.trash2 (RemoveFromInterestList childPath)

                                            else
                                                iconButton FeatherIcons.plus (AddToInterestList childPath)
                                    in
                                    itemRow
                                        [ button
                                        , el [ width fill ] (text name)
                                        , el (Font.alignRight :: fonts.explorerValues) <|
                                            text
                                                (format germanLocale f)
                                        ]
                    in
                    ( name, element )
                )
            |> Element.Keyed.column
                ([ padding sizes.medium
                 , spacing sizes.small
                 , width fill
                 ]
                    ++ fonts.explorerItems
                )


viewInputsAndResult : Int -> CollapseStatus -> Set Path -> InputsAndResult -> Element Msg
viewInputsAndResult resultNdx collapseStatus interestList inputsAndResult =
    column
        [ width fill
        , spacing sizes.medium
        , padding sizes.small
        , Border.width 1
        , Border.color black
        , Border.rounded 4
        ]
        [ row [ width fill ]
            [ Input.button ([ width fill ] ++ treeElementStyle)
                { label =
                    row [ width fill, spacing sizes.medium ]
                        [ collapsedStatusIcon ( resultNdx, [] ) collapseStatus
                        , el [ Font.bold ] (text (String.fromInt resultNdx ++ ":"))
                        , text (inputsAndResult.inputs.ags ++ " " ++ String.fromInt inputsAndResult.inputs.year)
                        ]
                , onPress = Just (CollapseToggleRequested ( resultNdx, [] ))
                }
            , iconButton FeatherIcons.edit (DisplayCalculateModalPressed (Just resultNdx) (Just inputsAndResult.inputs))
            , iconButton FeatherIcons.copy (DisplayCalculateModalPressed Nothing (Just inputsAndResult.inputs))
            , dangerousIconButton FeatherIcons.trash2 (RemoveResult resultNdx)
            ]
        , viewTree resultNdx [] collapseStatus interestList inputsAndResult.result
        ]


{-| The pane on the left hand side containing the results
-}
viewResultsPane : Model -> Element Msg
viewResultsPane model =
    let
        topBar =
            row ([ width fill ] ++ fonts.explorer)
                [ text "LocalZero Explorer"
                , el [ width fill ] Element.none
                , iconButton FeatherIcons.plus (DisplayCalculateModalPressed Nothing Nothing)
                ]
    in
    column
        [ height fill
        , spacing sizes.large
        , padding sizes.large
        , height (minimum 0 fill)
        , width (minimum 500 shrink)
        ]
        [ topBar
        , el
            [ scrollbarY
            , width fill
            , height fill
            ]
            (column
                [ spacing sizes.large
                , width fill
                , height fill
                ]
                (GeneratorRuns.toList model.results
                    |> List.map
                        (\( resultNdx, ir ) ->
                            viewInputsAndResult resultNdx model.collapseStatus model.interestList ir
                        )
                )
            )
        ]


viewInterestList : InterestListTable -> Element Msg
viewInterestList interestList =
    case interestList of
        [] ->
            Element.none

        ( _, row ) :: _ ->
            let
                resultCount =
                    Array.length row

                dataColumns =
                    List.range 0 (resultCount - 1)
                        |> List.map
                            (\resultNdx ->
                                { header = el [ Font.bold, Font.alignRight ] (Element.text (String.fromInt resultNdx))
                                , width = shrink
                                , view =
                                    \( path, values ) ->
                                        Array.get resultNdx values
                                            |> Maybe.andThen identity
                                            |> Maybe.map
                                                (\f ->
                                                    el (Font.alignRight :: fonts.explorerValues) <|
                                                        text
                                                            (format germanLocale f)
                                                )
                                            |> Maybe.withDefault Element.none
                                }
                            )

                pathColumn =
                    { header = Element.none, width = shrink, view = \( p, _ ) -> text (String.join "." p) }

                deleteColumn =
                    { header = Element.none
                    , width = shrink
                    , view =
                        \( p, _ ) ->
                            dangerousIconButton FeatherIcons.trash2 (RemoveFromInterestList p)
                    }
            in
            Element.table
                [ width fill
                , height fill
                , scrollbarY
                , spacing sizes.large
                , padding sizes.large
                ]
                { data = interestList
                , columns = pathColumn :: dataColumns ++ [ deleteColumn ]
                }


viewModel : Model -> Element Msg
viewModel model =
    let
        interestList =
            getInterestList model
    in
    row [ width fill, height fill ]
        [ viewResultsPane model
        , column [ width fill, height fill, spacing 40, padding sizes.large ]
            [ viewChart interestList
            , viewInterestList interestList
            ]
        ]


viewModalDialogBox : Element Msg -> Element Msg
viewModalDialogBox content =
    let
        filler =
            el [ width fill, height fill ] Element.none
    in
    column
        [ width fill
        , height fill
        , Background.color modalDim
        ]
        [ filler
        , row [ width fill, height fill ]
            [ filler
            , el
                [ width (minimum 600 fill)
                , height (minimum 400 fill)
                , Background.color germanZeroYellow
                , Border.rounded 4
                , padding sizes.large
                ]
                content
            , filler
            ]
        , filler
        ]


viewCalculateModal : Maybe Int -> Inputs -> Element Msg
viewCalculateModal maybeNdx inputs =
    let
        labelStyle =
            [ Font.alignRight, width (minimum 100 shrink) ]
    in
    column
        [ width fill
        , height fill
        , Background.color white
        , spacing sizes.medium
        , padding sizes.medium
        ]
        [ Input.text []
            { label = Input.labelLeft labelStyle (text "AGS")
            , text = inputs.ags
            , onChange = UpdateModal << CalculateModalAgsUpdated
            , placeholder = Nothing
            }
        , Input.slider
            [ height (px 20)
            , Element.behindContent
                (el
                    [ width fill
                    , height (px 2)
                    , Element.centerY
                    , Background.color germanZeroGreen
                    , Border.rounded 2
                    ]
                    Element.none
                )
            ]
            { label = Input.labelLeft labelStyle (text (String.fromInt inputs.year))
            , min = 2025
            , max = 2050
            , step = Just 1.0
            , onChange = UpdateModal << CalculateModalTargetYearUpdated << round
            , value = toFloat inputs.year
            , thumb = Input.defaultThumb
            }
        , iconButton FeatherIcons.check (CalculateModalOkPressed maybeNdx inputs)
        ]


view : Model -> Html Msg
view model =
    let
        filler =
            el [ width fill, height fill ] Element.none

        dialog =
            case model.showModal of
                Nothing ->
                    Element.none

                Just modalState ->
                    viewModalDialogBox
                        (case modalState of
                            PrepareCalculate maybeNdx inputs ->
                                viewCalculateModal maybeNdx inputs

                            Loading ->
                                text "Loading..."

                            LoadFailure msg ->
                                text ("FAILURE: " ++ msg)
                        )
    in
    Element.layout
        [ width fill
        , height fill
        , Element.inFront dialog
        ]
        (viewModel model)
