module Main exposing (Model, Msg(..), init, main, subscriptions, update, view)

--import Element.Background as Background

import AllRuns
    exposing
        ( AbsolutePath
        , AllRuns
        , RunId
        )
import Array exposing (Array)
import Browser
import Browser.Dom
import Chart as C
import Chart.Attributes as CA
import CollapseStatus exposing (CollapseStatus, allCollapsed, isCollapsed)
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
import Element.Events as Events
import Element.Font as Font
import Element.Input as Input
import Element.Keyed
import FeatherIcons
import FormatNumber exposing (format)
import FormatNumber.Locales exposing (spanishLocale)
import Html exposing (Html)
import Html.Attributes
import Html.Events
import Http
import InterestList exposing (InterestList)
import Json.Decode as Decode
import Json.Encode as Encode
import Maybe.Extra
import Run exposing (Run)
import Set exposing (Set)
import Task
import ValueTree exposing (Node(..), Tree, Value(..))


germanLocale =
    { spanishLocale | decimals = 2 }


parseGermanNumber : String -> Maybe Float
parseGermanNumber s =
    s
        |> String.replace "." ""
        -- ignore . (thousands separator)
        |> String.replace "," "."
        -- make it look like an english number
        |> String.toFloat



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


size16 : FeatherIcons.Icon -> FeatherIcons.Icon
size16 =
    FeatherIcons.withSize 16


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


type alias ActiveOverrideEditor =
    { runNdx : RunId, name : String, value : String, asFloat : Maybe Float }


type alias Model =
    { runs : AllRuns
    , collapseStatus : CollapseStatus
    , interestList : InterestList
    , showModal : Maybe ModalState
    , activeOverrideEditor : Maybe ActiveOverrideEditor
    }


type ModalState
    = PrepareCalculate (Maybe RunId) Run.Inputs Run.Overrides
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


encodeOverrides : Run.Overrides -> Encode.Value
encodeOverrides d =
    Encode.dict
        identity
        Encode.float
        d


initiateCalculate : Maybe RunId -> Run.Inputs -> Run.Entries -> Run.Overrides -> Model -> ( Model, Cmd Msg )
initiateCalculate maybeNdx inputs entries overrides model =
    ( { model | showModal = Just Loading }
    , Http.post
        { url = "http://localhost:4070/calculate/" ++ inputs.ags ++ "/" ++ String.fromInt inputs.year
        , expect = Http.expectJson (GotGeneratorResult maybeNdx inputs entries overrides) ValueTree.decoder
        , body = Http.jsonBody (encodeOverrides overrides)
        }
    )


initiateMakeEntries : Maybe RunId -> Run.Inputs -> Run.Overrides -> Model -> ( Model, Cmd Msg )
initiateMakeEntries maybeNdx inputs overrides model =
    ( { model | showModal = Just Loading }
    , Http.get
        { url = "http://localhost:4070/make-entries/" ++ inputs.ags ++ "/" ++ String.fromInt inputs.year
        , expect = Http.expectJson (GotEntries maybeNdx inputs overrides) Run.entriesDecoder
        }
    )


init : () -> ( Model, Cmd Msg )
init _ =
    ( { runs = AllRuns.empty
      , showModal = Nothing
      , interestList = InterestList.empty
      , collapseStatus = allCollapsed
      , activeOverrideEditor = Nothing
      }
    , Cmd.none
    )



-- UPDATE


type Msg
    = GotGeneratorResult (Maybe RunId) Run.Inputs Run.Entries Run.Overrides (Result Http.Error Tree)
    | GotEntries (Maybe RunId) Run.Inputs Run.Overrides (Result Http.Error Run.Entries)
      --| AddItemToChartClicked { path : Path, value : Float }
    | AddToInterestList Run.Path
    | AddOrUpdateOverride RunId String Float
    | RemoveOverride RunId String
    | OverrideEdited RunId String String
    | OverrideEditFinished
    | RemoveFromInterestList Run.Path
    | CollapseToggleRequested AbsolutePath
    | UpdateModal ModalMsg
    | DisplayCalculateModalPressed (Maybe RunId) Run.Inputs Run.Overrides
    | CalculateModalOkPressed (Maybe RunId) Run.Inputs
    | RemoveResult RunId
    | Noop


type ModalMsg
    = CalculateModalTargetYearUpdated Int
    | CalculateModalAgsUpdated String


type alias InterestListTable =
    List ( Run.Path, Array Value )


getInterestList : Model -> InterestListTable
getInterestList model =
    -- The withDefault handles the case if we somehow managed to get two
    -- differently structured result values into the explorer, this can only
    -- really happen when two different versions of the python code are
    -- explored at the same time.
    -- Otherwise you can't add a path to the interest list that ends
    -- at a TREE
    InterestList.toList model.interestList
        |> List.map
            (\path ->
                ( path
                , Array.initialize (AllRuns.size model.runs)
                    (\n ->
                        AllRuns.getValue Run.WithOverrides n path model.runs
                            |> Maybe.withDefault (String "TREE")
                    )
                )
            )


withLoadFailure : String -> Model -> ( Model, Cmd Msg )
withLoadFailure msg model =
    ( { model | showModal = Just (LoadFailure msg) }, Cmd.none )


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Noop ->
            ( model, Cmd.none )

        GotEntries maybeNdx inputs overrides (Ok entries) ->
            model
                |> initiateCalculate maybeNdx inputs entries overrides

        GotEntries _ _ _ (Err e) ->
            ( model, Cmd.none )

        GotGeneratorResult maybeNdx inputs entries overrides resultOrError ->
            case resultOrError of
                Ok result ->
                    let
                        run =
                            Run.create
                                { inputs = inputs
                                , entries = entries
                                , result = result
                                , overrides = overrides
                                }

                        newResults =
                            case maybeNdx of
                                Nothing ->
                                    AllRuns.add run model.runs

                                Just ndx ->
                                    AllRuns.set ndx run model.runs
                    in
                    ( { model
                        | runs = newResults
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

        DisplayCalculateModalPressed maybeNdx inputs overrides ->
            let
                modal =
                    PrepareCalculate maybeNdx inputs overrides
            in
            ( { model | showModal = Just modal }
            , Cmd.none
            )

        CalculateModalOkPressed maybeNdx inputs ->
            -- TODO: Actually lookup any existing overrides
            model
                |> initiateMakeEntries maybeNdx inputs Dict.empty

        AddToInterestList path ->
            ( { model | interestList = InterestList.insert path model.interestList }
            , Cmd.none
            )

        AddOrUpdateOverride ndx name f ->
            ( { model
                | runs =
                    model.runs
                        |> AllRuns.update ndx (Run.mapOverrides (Dict.insert name f))
              }
            , Cmd.none
            )

        OverrideEdited ndx name newText ->
            let
                isFocusChanged =
                    case model.activeOverrideEditor of
                        Nothing ->
                            True

                        Just e ->
                            e.runNdx /= ndx || e.name /= name
            in
            ( { model
                | activeOverrideEditor =
                    Just
                        { runNdx = ndx
                        , name = name
                        , value = newText
                        , asFloat = parseGermanNumber newText
                        }
              }
            , if isFocusChanged then
                Task.attempt (\_ -> Noop) (Browser.Dom.focus "overrideEditor")

              else
                Cmd.none
            )

        OverrideEditFinished ->
            case model.activeOverrideEditor of
                Nothing ->
                    ( model, Cmd.none )

                Just editor ->
                    let
                        modelEditorClosed =
                            { model | activeOverrideEditor = Nothing }
                    in
                    case editor.asFloat of
                        Nothing ->
                            -- Throw the edit away it wasn't valid
                            ( modelEditorClosed, Cmd.none )

                        Just f ->
                            case AllRuns.get editor.runNdx model.runs of
                                Nothing ->
                                    ( modelEditorClosed, Cmd.none )

                                Just run ->
                                    modelEditorClosed
                                        |> initiateMakeEntries (Just editor.runNdx)
                                            (Run.getInputs run)
                                            (Run.getOverrides run
                                                |> Dict.insert editor.name f
                                            )

        RemoveOverride ndx name ->
            ( { model
                | runs =
                    model.runs
                        |> AllRuns.update ndx (Run.mapOverrides (Dict.remove name))
                , activeOverrideEditor =
                    model.activeOverrideEditor
                        |> Maybe.Extra.filter (\e -> e.runNdx /= ndx || e.name /= name)
              }
            , Cmd.none
            )

        RemoveFromInterestList path ->
            ( { model | interestList = InterestList.remove path model.interestList }
            , Cmd.none
            )

        RemoveResult ndx ->
            ( { model | runs = AllRuns.remove ndx model.runs }
            , Cmd.none
            )


updateModal : ModalMsg -> Maybe ModalState -> ( Maybe ModalState, Cmd ModalMsg )
updateModal msg model =
    case model of
        Nothing ->
            ( Nothing, Cmd.none )

        Just (PrepareCalculate ndx inputs overrides) ->
            case msg of
                CalculateModalAgsUpdated a ->
                    ( Just (PrepareCalculate ndx { inputs | ags = a } overrides), Cmd.none )

                CalculateModalTargetYearUpdated y ->
                    ( Just (PrepareCalculate ndx { inputs | year = y } overrides), Cmd.none )

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
                                        case Array.get ndx a of
                                            Just (Float f) ->
                                                f

                                            Just (String _) ->
                                                0.0

                                            Just Null ->
                                                0.0

                                            Nothing ->
                                                0.0
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
    el iconButtonStyle (icon (size16 i))


onEnter : msg -> Element.Attribute msg
onEnter msg =
    Element.htmlAttribute
        (Html.Events.on "keyup"
            (Decode.field "key" Decode.string
                |> Decode.andThen
                    (\key ->
                        if key == "Enter" then
                            Decode.succeed msg

                        else
                            Decode.fail "Not the enter key"
                    )
            )
        )


viewTree :
    Int
    -> Run.Path
    -> CollapseStatus
    -> InterestList
    -> Run.Overrides
    -> Maybe ActiveOverrideEditor
    -> Tree
    -> Element Msg
viewTree resultNdx path collapseStatus interestList overrides activeOverrideEditor tree =
    if isCollapsed ( resultNdx, path ) collapseStatus then
        Element.none

    else
        Dict.toList tree
            |> List.map
                (\( name, val ) ->
                    let
                        isEntry =
                            path == [ "entries" ]

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
                                        , viewTree resultNdx childPath collapseStatus interestList overrides activeOverrideEditor child
                                        ]

                                Leaf Null ->
                                    itemRow
                                        [ el [ width fill ] (text name)
                                        , el (Font.alignRight :: Font.bold :: fonts.explorerValues) <| text "null"
                                        ]

                                Leaf (String s) ->
                                    itemRow
                                        [ el [ width fill ] (text name)
                                        , el (Font.alignRight :: fonts.explorerValues) <| text s
                                        ]

                                Leaf (Float f) ->
                                    let
                                        formattedF : String
                                        formattedF =
                                            format germanLocale f

                                        button =
                                            if InterestList.member childPath interestList then
                                                dangerousIconButton (size16 FeatherIcons.trash2) (RemoveFromInterestList childPath)

                                            else
                                                iconButton (size16 FeatherIcons.plus) (AddToInterestList childPath)

                                        ( originalValue, maybeOverride ) =
                                            -- Clicking on original value should start or revert
                                            -- an override
                                            if isEntry then
                                                let
                                                    override =
                                                        Dict.get name overrides

                                                    thisOverrideEditor =
                                                        activeOverrideEditor
                                                            |> Maybe.Extra.filter (\e -> e.runNdx == resultNdx && e.name == name)

                                                    ( originalStyle, action, o ) =
                                                        case thisOverrideEditor of
                                                            Nothing ->
                                                                case override of
                                                                    Nothing ->
                                                                        ( [ Font.color germanZeroGreen
                                                                          , Element.mouseOver [ Font.color germanZeroYellow ]
                                                                          ]
                                                                        , OverrideEdited resultNdx name formattedF
                                                                        , Element.none
                                                                        )

                                                                    Just newF ->
                                                                        let
                                                                            newFormattedF =
                                                                                format germanLocale newF
                                                                        in
                                                                        ( [ Font.strike
                                                                          , Font.color red
                                                                          , Element.mouseOver [ Font.color germanZeroYellow ]
                                                                          ]
                                                                        , RemoveOverride resultNdx name
                                                                        , Input.button (Font.alignRight :: fonts.explorerValues)
                                                                            { label = text newFormattedF
                                                                            , onPress = Just (OverrideEdited resultNdx name newFormattedF)
                                                                            }
                                                                        )

                                                            Just editor ->
                                                                let
                                                                    textStyle =
                                                                        case editor.asFloat of
                                                                            Nothing ->
                                                                                [ Border.color red, Border.width 1 ]

                                                                            Just _ ->
                                                                                [ onEnter OverrideEditFinished
                                                                                ]

                                                                    textAttributes =
                                                                        Events.onLoseFocus OverrideEditFinished
                                                                            :: Element.htmlAttribute (Html.Attributes.id "overrideEditor")
                                                                            :: textStyle
                                                                in
                                                                ( [ Font.strike
                                                                  , Font.color red
                                                                  , Element.mouseOver [ Font.color germanZeroYellow ]
                                                                  ]
                                                                , RemoveOverride resultNdx name
                                                                , Input.text textAttributes
                                                                    { text = editor.value
                                                                    , onChange = OverrideEdited resultNdx name
                                                                    , placeholder = Nothing
                                                                    , label = Input.labelHidden "override"
                                                                    }
                                                                )
                                                in
                                                ( Input.button (Font.alignRight :: fonts.explorerValues ++ originalStyle)
                                                    { label = text formattedF
                                                    , onPress = Just action
                                                    }
                                                , o
                                                )

                                            else
                                                ( el (Font.alignRight :: fonts.explorerValues) <|
                                                    text
                                                        (format germanLocale f)
                                                , Element.none
                                                )
                                    in
                                    itemRow
                                        [ button
                                        , el [ width fill ] (text name)
                                        , originalValue
                                        , maybeOverride
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


viewInputsAndResult : Int -> CollapseStatus -> InterestList -> Maybe ActiveOverrideEditor -> Run -> Element Msg
viewInputsAndResult resultNdx collapseStatus interestList activeOverrideEditor run =
    let
        inputs =
            Run.getInputs run

        overrides =
            Run.getOverrides run
    in
    column
        [ width fill
        , spacing sizes.medium
        , padding sizes.small
        , Border.width 1
        , Border.color black
        , Border.rounded 4
        ]
        [ row [ width fill ]
            [ Input.button (width fill :: treeElementStyle)
                { label =
                    row [ width fill, spacing sizes.medium ]
                        [ collapsedStatusIcon ( resultNdx, [] ) collapseStatus
                        , el [ Font.bold ] (text (String.fromInt resultNdx ++ ":"))
                        , text (inputs.ags ++ " " ++ String.fromInt inputs.year)
                        ]
                , onPress = Just (CollapseToggleRequested ( resultNdx, [] ))
                }
            , iconButton FeatherIcons.edit (DisplayCalculateModalPressed (Just resultNdx) inputs overrides)
            , iconButton FeatherIcons.copy (DisplayCalculateModalPressed Nothing inputs overrides)
            , dangerousIconButton FeatherIcons.trash2 (RemoveResult resultNdx)
            ]
        , viewTree resultNdx
            []
            collapseStatus
            interestList
            overrides
            activeOverrideEditor
            (Run.getTree Run.WithoutOverrides run)
        ]


{-| The pane on the left hand side containing the results
-}
viewResultsPane : Model -> Element Msg
viewResultsPane model =
    let
        defaultInputs =
            { ags = ""
            , year = 2035
            }

        topBar =
            row (width fill :: fonts.explorer)
                [ text "LocalZero Explorer"
                , el [ width fill ] Element.none
                , iconButton FeatherIcons.plus (DisplayCalculateModalPressed Nothing defaultInputs Dict.empty)
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
                (AllRuns.toList model.runs
                    |> List.map
                        (\( resultNdx, ir ) ->
                            viewInputsAndResult resultNdx
                                model.collapseStatus
                                model.interestList
                                model.activeOverrideEditor
                                ir
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
                                    \( _, values ) ->
                                        let
                                            value =
                                                case Array.get resultNdx values of
                                                    Just (Float f) ->
                                                        el (Font.alignRight :: fonts.explorerValues) <|
                                                            text
                                                                (format germanLocale f)

                                                    Just (String s) ->
                                                        el (Font.alignRight :: fonts.explorerValues) <|
                                                            text s

                                                    Just Null ->
                                                        el (Font.alignRight :: Font.bold :: fonts.explorerValues) <|
                                                            text "bold"

                                                    Nothing ->
                                                        -- make compiler happy
                                                        Element.none
                                        in
                                        value
                                }
                            )

                pathColumn =
                    { header = Element.none, width = shrink, view = \( p, _ ) -> text (String.join "." p) }

                deleteColumn =
                    { header = Element.none
                    , width = shrink
                    , view =
                        \( p, _ ) ->
                            dangerousIconButton (size16 FeatherIcons.trash2) (RemoveFromInterestList p)
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


viewCalculateModal : Maybe Int -> Run.Inputs -> Run.Overrides -> Element Msg
viewCalculateModal maybeNdx inputs overrides =
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
        dialog =
            case model.showModal of
                Nothing ->
                    Element.none

                Just modalState ->
                    viewModalDialogBox
                        (case modalState of
                            PrepareCalculate maybeNdx inputs overrides ->
                                viewCalculateModal maybeNdx inputs overrides

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
