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
import Chart.Events
import Chart.Item
import Cmd.Extra exposing (withCmd, withNoCmd)
import CollapseStatus exposing (CollapseStatus, allCollapsed, isCollapsed)
import Dict exposing (Dict)
import Dropdown
import Element
    exposing
        ( Element
        , alignTop
        , centerX
        , column
        , el
        , fill
        , height
        , maximum
        , minimum
        , padding
        , paragraph
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
import File exposing (File)
import File.Download as Download
import File.Select
import Filter
import Html exposing (Html)
import Html.Attributes
import Html.Events
import Http
import InterestList exposing (InterestList)
import InterestListTable exposing (InterestListTable)
import Json.Decode as Decode
import Json.Encode as Encode
import List.Extra
import Maybe.Extra
import Pivot exposing (Pivot)
import Run exposing (OverrideHandling(..), Run)
import Set exposing (Set)
import Storage exposing (Storage)
import Styling
    exposing
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
import Task
import Tree exposing (Node(..), Tree, Value(..))



-- MAIN


main =
    Browser.element
        { init = init
        , update = update
        , subscriptions = subscriptions
        , view = view
        }



-- MODEL


type alias ActiveOverrideEditor =
    { runId : RunId, name : String, value : String, asFloat : Maybe Float }


type alias ActiveSearch =
    { runId : RunId, pattern : String, result : Tree.Tree }


{-| Position of interestlist in pivot
-}
type alias InterestListId =
    Int


type alias ChartHovering =
    List (Chart.Item.Many (List String) Chart.Item.Any)


type alias Model =
    { runs : AllRuns
    , collapseStatus : CollapseStatus
    , interestLists : Pivot InterestList
    , editingActiveInterestListLabel : Bool
    , showModal : Maybe ModalState
    , activeOverrideEditor : Maybe ActiveOverrideEditor
    , activeSearch : Maybe ActiveSearch
    , chartHovering : ChartHovering
    }


type ModalState
    = PrepareCalculate (Maybe RunId) Run.Inputs Run.Overrides
    | Loading
    | LoadFailure String


filterFieldId : String
filterFieldId =
    "filter"


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
        , expect = Http.expectJson (GotGeneratorResult maybeNdx inputs entries overrides) Tree.decoder
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


activateInterestList : InterestListId -> Model -> Model
activateInterestList id model =
    { model
        | interestLists = Pivot.withRollback (Pivot.goTo id) model.interestLists
    }


init : () -> ( Model, Cmd Msg )
init _ =
    ( { runs = AllRuns.empty
      , showModal = Nothing
      , interestLists = Pivot.singleton InterestList.empty
      , editingActiveInterestListLabel = False
      , collapseStatus = allCollapsed
      , activeOverrideEditor = Nothing
      , activeSearch = Nothing
      , chartHovering = []
      }
    , Cmd.none
    )



-- UPDATE


type Msg
    = GotGeneratorResult (Maybe RunId) Run.Inputs Run.Entries Run.Overrides (Result Http.Error Tree)
    | GotEntries (Maybe RunId) Run.Inputs Run.Overrides (Result Http.Error Run.Entries)
    | AddToInterestListClicked Run.Path
    | RemoveFromInterestListClicked InterestListId Run.Path
    | AddOrUpdateOverrideClicked RunId String Float
    | RemoveOverrideClicked RunId String
    | OverrideEdited RunId String String
    | OverrideEditFinished
    | FilterEdited RunId String
    | FilterFinished
    | FilterQuickAddRequested
    | ToggleCollapseTreeClicked AbsolutePath
    | ModalMsg ModalMsg
    | DisplayCalculateModalClicked (Maybe RunId) Run.Inputs Run.Overrides
    | CalculateModalOkClicked (Maybe RunId) Run.Inputs
    | RemoveRunClicked RunId
    | InterestListLabelEdited InterestListId String
    | InterestListLabelEditFinished
    | ToggleShowGraphClicked InterestListId
    | DuplicateInterestListClicked InterestListId
    | RemoveInterestListClicked InterestListId
    | ActivateInterestListClicked InterestListId
    | NewInterestListClicked
    | DownloadClicked
    | UploadClicked
    | FileUploaded File
    | FileContentLoaded String
    | OnChartHover ChartHovering
    | Noop


type ModalMsg
    = CalculateModalTargetYearUpdated Int
    | CalculateModalAgsUpdated String


mapActiveInterestList : (InterestList -> InterestList) -> Model -> Model
mapActiveInterestList f =
    mapInterestLists (Pivot.mapC f)


mapInterestLists : (Pivot InterestList -> Pivot InterestList) -> Model -> Model
mapInterestLists f m =
    { m | interestLists = f m.interestLists }


withLoadFailure : String -> Model -> ( Model, Cmd Msg )
withLoadFailure msg model =
    ( { model | showModal = Just (LoadFailure msg) }, Cmd.none )


withEditingActiveInterestListLabel : Bool -> Model -> Model
withEditingActiveInterestListLabel b m =
    { m | editingActiveInterestListLabel = b }


downloadCmd : Model -> Cmd msg
downloadCmd model =
    let
        content =
            Storage.encode { interestLists = Pivot.toList model.interestLists }
                |> Encode.encode 0
    in
    Download.string "explorer.json" "text/json" content


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Noop ->
            model
                |> withNoCmd

        DownloadClicked ->
            model
                |> withCmd (downloadCmd model)

        UploadClicked ->
            model
                |> withCmd (File.Select.file [ "text/json" ] FileUploaded)

        FileUploaded file ->
            model
                |> withCmd (Task.perform FileContentLoaded (File.toString file))

        FileContentLoaded content ->
            case Decode.decodeString Storage.decoder content of
                Err _ ->
                    model
                        |> withLoadFailure "Failed to load file"

                Ok storage ->
                    let
                        ils =
                            case Pivot.fromList storage.interestLists of
                                Nothing ->
                                    model.interestLists

                                Just i ->
                                    i
                    in
                    { model | interestLists = ils }
                        |> withNoCmd

        GotEntries maybeNdx inputs overrides (Ok entries) ->
            model
                |> initiateCalculate maybeNdx inputs entries overrides

        GotEntries _ _ _ (Err _) ->
            model
                |> withNoCmd

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
                    { model
                        | runs = newResults
                        , showModal = Nothing
                    }
                        |> withNoCmd

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

        ToggleCollapseTreeClicked path ->
            { model | collapseStatus = CollapseStatus.toggle path model.collapseStatus }
                |> withNoCmd

        RemoveRunClicked ndx ->
            { model | runs = AllRuns.remove ndx model.runs }
                |> withNoCmd

        ModalMsg modalMsg ->
            updateModal modalMsg model.showModal
                |> Tuple.mapFirst (\md -> { model | showModal = md })
                |> Tuple.mapSecond (Cmd.map ModalMsg)

        DisplayCalculateModalClicked maybeNdx inputs overrides ->
            let
                modal =
                    PrepareCalculate maybeNdx inputs overrides
            in
            { model | showModal = Just modal }
                |> withNoCmd

        CalculateModalOkClicked maybeNdx inputs ->
            -- TODO: Actually lookup any existing overrides
            model
                |> initiateMakeEntries maybeNdx inputs Dict.empty

        AddOrUpdateOverrideClicked ndx name f ->
            { model
                | runs =
                    model.runs
                        |> AllRuns.update ndx (Run.mapOverrides (Dict.insert name f))
            }
                |> withNoCmd

        FilterEdited runId pattern ->
            let
                newActiveSearch =
                    case AllRuns.get runId model.runs of
                        Nothing ->
                            -- Shouldn't really happen, but have to make compiler happy
                            -- would really like elm to have panic
                            model.activeSearch

                        Just run ->
                            let
                                result =
                                    Filter.filter pattern (Run.getTree WithoutOverrides run)
                            in
                            Just
                                { runId = runId
                                , pattern = pattern
                                , result = result
                                }

                activeSearchFieldChanged =
                    case ( model.activeSearch, newActiveSearch ) of
                        ( _, Nothing ) ->
                            False

                        ( Nothing, Just _ ) ->
                            True

                        ( Just a, Just b ) ->
                            a.runId /= b.runId
            in
            { model | activeSearch = newActiveSearch }
                |> withCmd (Task.attempt (\_ -> Noop) (Browser.Dom.focus filterFieldId))

        FilterQuickAddRequested ->
            case model.activeSearch of
                Nothing ->
                    model
                        |> withNoCmd

                Just a ->
                    let
                        paths =
                            Tree.expand a.result
                    in
                    { model | activeSearch = Nothing }
                        |> mapActiveInterestList
                            (\il ->
                                List.foldl (\p i -> InterestList.insert p i) il paths
                            )
                        |> withNoCmd

        FilterFinished ->
            { model | activeSearch = Nothing }
                |> withNoCmd

        OverrideEdited runId name newText ->
            let
                isFocusChanged =
                    case model.activeOverrideEditor of
                        Nothing ->
                            True

                        Just e ->
                            e.runId /= runId || e.name /= name
            in
            ( { model
                | activeOverrideEditor =
                    Just
                        { runId = runId
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
                            case AllRuns.get editor.runId model.runs of
                                Nothing ->
                                    ( modelEditorClosed, Cmd.none )

                                Just run ->
                                    modelEditorClosed
                                        |> initiateMakeEntries (Just editor.runId)
                                            (Run.getInputs run)
                                            (Run.getOverrides run
                                                |> Dict.insert editor.name f
                                            )

        RemoveOverrideClicked runId name ->
            { model
                | runs =
                    model.runs
                        |> AllRuns.update runId (Run.mapOverrides (Dict.remove name))
                , activeOverrideEditor =
                    model.activeOverrideEditor
                        |> Maybe.Extra.filter (\e -> e.runId /= runId || e.name /= name)
            }
                |> withNoCmd

        AddToInterestListClicked path ->
            model
                |> mapActiveInterestList (InterestList.insert path)
                |> withNoCmd

        RemoveFromInterestListClicked id path ->
            model
                |> activateInterestList id
                |> mapActiveInterestList (InterestList.remove path)
                |> withNoCmd

        ToggleShowGraphClicked id ->
            model
                |> activateInterestList id
                |> mapActiveInterestList InterestList.toggleShowGraph
                |> withNoCmd

        NewInterestListClicked ->
            model
                |> mapInterestLists (Pivot.appendR InterestList.empty)
                |> withNoCmd

        DuplicateInterestListClicked id ->
            model
                |> activateInterestList id
                |> mapInterestLists
                    (\p ->
                        Pivot.appendGoR
                            (Pivot.getC p
                                |> InterestList.mapLabel (\l -> l ++ " Copy")
                            )
                            p
                    )
                |> withNoCmd

        RemoveInterestListClicked id ->
            model
                |> activateInterestList id
                |> mapInterestLists
                    (\ils ->
                        case Pivot.removeGoR ils of
                            Nothing ->
                                -- If List was singleton, delete becomes
                                -- reset to empty
                                Maybe.withDefault (Pivot.singleton InterestList.empty) (Pivot.removeGoL ils)

                            Just without ->
                                without
                    )
                |> withNoCmd

        ActivateInterestListClicked id ->
            model
                |> activateInterestList id
                |> withNoCmd

        InterestListLabelEdited id newLabel ->
            model
                |> activateInterestList id
                |> withEditingActiveInterestListLabel True
                |> mapActiveInterestList (InterestList.mapLabel (always newLabel))
                |> withCmd
                    (Task.attempt (\_ -> Noop) (Browser.Dom.focus "interestlabel"))

        InterestListLabelEditFinished ->
            model
                |> withEditingActiveInterestListLabel False
                |> withNoCmd

        OnChartHover hovering ->
            { model | chartHovering = hovering }
                |> withNoCmd


updateModal : ModalMsg -> Maybe ModalState -> ( Maybe ModalState, Cmd ModalMsg )
updateModal msg model =
    case model of
        Nothing ->
            Nothing
                |> withNoCmd

        Just (PrepareCalculate ndx inputs overrides) ->
            case msg of
                CalculateModalAgsUpdated a ->
                    Just (PrepareCalculate ndx { inputs | ags = a } overrides)
                        |> withNoCmd

                CalculateModalTargetYearUpdated y ->
                    Just (PrepareCalculate ndx { inputs | year = y } overrides)
                        |> withNoCmd

        Just Loading ->
            Just Loading
                |> withNoCmd

        Just (LoadFailure f) ->
            Just (LoadFailure f)
                |> withNoCmd



-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none



-- VIEW


viewChart : ChartHovering -> Dict Run.Path String -> InterestListTable -> Element Msg
viewChart chartHovering shortPathLabels interestListTable =
    let
        widthChart =
            800

        heightChart =
            400

        bars =
            interestListTable.runs
                |> List.map
                    (\runId ->
                        let
                            get path =
                                case Dict.get ( runId, path ) interestListTable.values of
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
                            |> C.named (String.fromInt runId)
                            |> C.format (\v -> formatGermanNumber v)
                    )

        getLabel : Run.Path -> String
        getLabel p =
            case Dict.get p shortPathLabels of
                Just s ->
                    s

                Nothing ->
                    String.join "." p

        chart =
            C.chart
                [ CA.height heightChart
                , CA.width widthChart
                , Chart.Events.onMouseMove OnChartHover (Chart.Events.getNearest Chart.Item.bins)
                , Chart.Events.onMouseLeave (OnChartHover [])
                ]
                [ C.xTicks []
                , C.yTicks []
                , C.yLabels []
                , C.xAxis []
                , C.yAxis []
                , C.bars [] bars interestListTable.paths
                , C.binLabels getLabel [ CA.moveDown 40 ]
                , C.legendsAt .max
                    .max
                    [ CA.column
                    , CA.moveRight 20
                    , CA.alignRight
                    , CA.spacing 5
                    ]
                    []
                , C.each chartHovering
                    (\p item ->
                        [ C.tooltip item [] [] [] ]
                    )
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


collapsedStatusIcon : Bool -> Element Msg
collapsedStatusIcon collapsed =
    let
        i =
            if collapsed then
                FeatherIcons.chevronRight

            else
                FeatherIcons.chevronDown
    in
    el iconButtonStyle (icon (size16 i))


onKeys : List ( String, msg ) -> Element.Attribute msg
onKeys keys =
    let
        keyDict =
            Dict.fromList keys
    in
    Element.htmlAttribute
        (Html.Events.on "keyup"
            (Decode.field "key" Decode.string
                |> Decode.andThen
                    (\k ->
                        case Dict.get k keyDict of
                            Just msg ->
                                Decode.succeed msg

                            Nothing ->
                                Decode.fail "Not the expected key"
                    )
            )
        )


onEnter : msg -> Element.Attribute msg
onEnter k =
    onKeys [ ( "Enter", k ) ]


viewEntryAndOverride : Int -> String -> Run.Overrides -> Maybe ActiveOverrideEditor -> Float -> ( Element Msg, Element Msg )
viewEntryAndOverride runId name overrides activeOverrideEditor f =
    let
        formattedF : String
        formattedF =
            formatGermanNumber f

        override =
            Dict.get name overrides

        thisOverrideEditor =
            activeOverrideEditor
                |> Maybe.Extra.filter (\e -> e.runId == runId && e.name == name)

        ( originalStyle, action, o ) =
            case thisOverrideEditor of
                Nothing ->
                    case override of
                        Nothing ->
                            ( [ Font.color germanZeroGreen
                              , Element.mouseOver [ Font.color germanZeroYellow ]
                              ]
                            , OverrideEdited runId name formattedF
                            , Element.none
                            )

                        Just newF ->
                            let
                                newFormattedF =
                                    formatGermanNumber newF
                            in
                            ( [ Font.strike
                              , Font.color red
                              , Element.mouseOver [ Font.color germanZeroYellow ]
                              ]
                            , RemoveOverrideClicked runId name
                            , Input.button
                                (Font.alignRight
                                    :: Font.color germanZeroGreen
                                    :: Element.mouseOver [ Font.color germanZeroYellow ]
                                    :: fonts.explorerValues
                                )
                                { label = text newFormattedF
                                , onPress = Just (OverrideEdited runId name newFormattedF)
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
                    , RemoveOverrideClicked runId name
                    , Input.text textAttributes
                        { text = editor.value
                        , onChange = OverrideEdited runId name
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


viewTree :
    RunId
    -> InterestListId
    -> Run.Path
    -> (RunId -> Run.Path -> Bool)
    -> InterestList
    -> Run.Overrides
    -> Maybe ActiveOverrideEditor
    -> Tree
    -> Element Msg
viewTree runId interestListId path checkIsCollapsed interestList overrides activeOverrideEditor tree =
    if checkIsCollapsed runId path then
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
                                                    [ collapsedStatusIcon (checkIsCollapsed runId childPath)
                                                    , el [ width fill ] (text name)
                                                    , el (Font.italic :: Font.alignRight :: fonts.explorerNodeSize) <|
                                                        text (String.fromInt (Dict.size child))
                                                    ]
                                            , onPress = Just (ToggleCollapseTreeClicked ( runId, path ++ [ name ] ))
                                            }
                                        , viewTree runId
                                            interestListId
                                            childPath
                                            checkIsCollapsed
                                            interestList
                                            overrides
                                            activeOverrideEditor
                                            child
                                        ]

                                Leaf Null ->
                                    itemRow
                                        [ el [ width (px 16) ] Element.none
                                        , el [ width fill ] (text name)
                                        , el (Font.alignRight :: Font.bold :: fonts.explorerValues) <| text "null"
                                        ]

                                Leaf (String s) ->
                                    itemRow
                                        [ el [ width (px 16) ] Element.none
                                        , el [ width fill ] (text name)
                                        , el (Font.alignRight :: fonts.explorerValues) <| text s
                                        ]

                                Leaf (Float f) ->
                                    let
                                        formattedF : String
                                        formattedF =
                                            formatGermanNumber f

                                        button =
                                            if InterestList.member childPath interestList then
                                                dangerousIconButton (size16 FeatherIcons.trash2)
                                                    (RemoveFromInterestListClicked interestListId childPath)

                                            else
                                                iconButton (size16 FeatherIcons.plus) (AddToInterestListClicked childPath)

                                        ( originalValue, maybeOverride ) =
                                            -- Clicking on original value should start or revert
                                            -- an override
                                            if isEntry then
                                                viewEntryAndOverride runId name overrides activeOverrideEditor f

                                            else
                                                ( el (Font.alignRight :: fonts.explorerValues) <|
                                                    text (formatGermanNumber f)
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
                ([ Element.paddingEach { left = sizes.medium, right = 0, top = sizes.medium, bottom = sizes.medium }
                 , spacing sizes.small
                 , width fill
                 ]
                    ++ fonts.explorerItems
                )


buttons : List (Element Msg) -> Element Msg
buttons l =
    row [ Element.spacingXY sizes.medium 0 ] l


viewInputsAndResult : RunId -> InterestListId -> CollapseStatus -> InterestList -> Maybe ActiveOverrideEditor -> Maybe ActiveSearch -> Run -> Element Msg
viewInputsAndResult runId interestListId collapseStatus interestList activeOverrideEditor activeSearch run =
    let
        inputs =
            Run.getInputs run

        overrides =
            Run.getOverrides run

        differentIfFilterActive =
            case activeSearch |> Maybe.Extra.filter (\s -> s.runId == runId) of
                Nothing ->
                    { filterButton = iconButton FeatherIcons.filter (FilterEdited runId "")
                    , treeToDisplay = Run.getTree WithoutOverrides run
                    , isCollapsed = \r p -> isCollapsed ( r, p ) collapseStatus
                    , filterPatternField = Element.none
                    }

                Just s ->
                    { filterButton = dangerousIconButton FeatherIcons.filter FilterFinished
                    , treeToDisplay = s.result
                    , isCollapsed = \_ _ -> False
                    , filterPatternField =
                        column [ width fill, spacing 8 ]
                            [ Input.text
                                [ width fill
                                , Font.size 18
                                , Element.htmlAttribute (Html.Attributes.id filterFieldId)
                                , onKeys
                                    [ ( "Escape", FilterFinished )
                                    , ( "Enter", FilterQuickAddRequested )
                                    ]
                                ]
                                { onChange = FilterEdited runId
                                , text = s.pattern
                                , label = Input.labelHidden "search"
                                , placeholder =
                                    Just
                                        (Input.placeholder [] (text "Pattern, e.g: a18 CO2e_total"))
                                }
                            , el [ Font.size 12 ] (text "Escape to cancel, Enter to add all")
                            ]
                    }
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
                        [ collapsedStatusIcon (differentIfFilterActive.isCollapsed runId [])
                        , el [ Font.bold ] (text (String.fromInt runId ++ ":"))
                        , text (inputs.ags ++ " " ++ String.fromInt inputs.year)
                        ]
                , onPress = Just (ToggleCollapseTreeClicked ( runId, [] ))
                }
            , buttons
                [ differentIfFilterActive.filterButton
                , iconButton FeatherIcons.edit (DisplayCalculateModalClicked (Just runId) inputs overrides)
                , iconButton FeatherIcons.copy (DisplayCalculateModalClicked Nothing inputs overrides)
                , dangerousIconButton FeatherIcons.trash2 (RemoveRunClicked runId)
                ]
            ]
        , differentIfFilterActive.filterPatternField
        , viewTree
            runId
            interestListId
            []
            differentIfFilterActive.isCollapsed
            interestList
            overrides
            activeOverrideEditor
            differentIfFilterActive.treeToDisplay
        ]


defaultInputs : Run.Inputs
defaultInputs =
    { ags = ""
    , year = 2035
    }


{-| The pane on the left hand side containing the results
-}
viewResultsPane : Model -> Element Msg
viewResultsPane model =
    column
        [ height fill
        , spacing sizes.large
        , padding sizes.large
        , height (minimum 0 fill)
        , width (minimum 500 shrink)
        , Element.inFront
            (floatingActionButton FeatherIcons.plus (DisplayCalculateModalClicked Nothing defaultInputs Dict.empty))
        ]
        [ el
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
                                (Pivot.lengthL model.interestLists)
                                model.collapseStatus
                                (Pivot.getC model.interestLists)
                                model.activeOverrideEditor
                                model.activeSearch
                                ir
                        )
                )
            )
        ]


viewInterestListTableAsTable : Dict Run.Path String -> InterestListId -> InterestListTable -> Element Msg
viewInterestListTableAsTable shortPathLabels interestListId interestListTable =
    let
        dataColumns =
            interestListTable.runs
                |> List.map
                    (\runId ->
                        { header = el [ Font.bold, Font.alignRight ] (Element.text (String.fromInt runId))
                        , width = shrink
                        , view =
                            \path ->
                                let
                                    value =
                                        case Dict.get ( runId, path ) interestListTable.values of
                                            Just (Float f) ->
                                                el (Font.alignRight :: fonts.explorerValues) <|
                                                    text (formatGermanNumber f)

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

        shortPathLabelColumn =
            { header = Element.none
            , width = shrink
            , view =
                \path ->
                    column []
                        [ Maybe.withDefault "CAN'T HAPPEN" (Dict.get path shortPathLabels)
                            |> text
                        , el [ Font.size 12 ] (text (String.join "." path))
                        ]
            }

        deleteColumn =
            { header = Element.none
            , width = shrink
            , view =
                \path ->
                    dangerousIconButton (size16 FeatherIcons.trash2) (RemoveFromInterestListClicked interestListId path)
            }
    in
    Element.table
        [ width fill
        , height shrink
        , spacing sizes.large
        , padding sizes.large
        ]
        { data = interestListTable.paths
        , columns = shortPathLabelColumn :: dataColumns ++ [ deleteColumn ]
        }


viewInterestList : InterestListId -> Bool -> Bool -> InterestList -> ChartHovering -> AllRuns -> Element Msg
viewInterestList id editingActiveInterestListLabel isActive interestList chartHovering allRuns =
    let
        interestListTable =
            InterestListTable.create interestList allRuns

        showGraph =
            InterestList.getShowGraph interestList

        labelText =
            InterestList.getLabel interestList

        shortPathLabels =
            InterestList.getShortPathLabels interestList

        ( borderColor, borderWidth ) =
            if isActive then
                ( germanZeroYellow, 2 )

            else
                ( germanZeroGreen, 1 )
    in
    column
        [ width fill
        , Events.onClick (ActivateInterestListClicked id)
        , Element.mouseOver [ Border.color germanZeroYellow ]
        , Border.color borderColor
        , Border.width borderWidth
        , padding sizes.medium
        ]
        [ row
            [ width fill
            , Font.size 24
            , Element.paddingXY sizes.large sizes.medium
            ]
            [ if editingActiveInterestListLabel && isActive then
                Input.text
                    [ Events.onLoseFocus InterestListLabelEditFinished
                    , onEnter InterestListLabelEditFinished
                    , Element.htmlAttribute (Html.Attributes.id "interestlabel")
                    ]
                    { onChange = InterestListLabelEdited id
                    , text = labelText
                    , label = Input.labelHidden "interest list"
                    , placeholder = Just (Input.placeholder [] (text "label"))
                    }

              else
                el
                    [ Events.onClick (InterestListLabelEdited id labelText)
                    , Font.color
                        (if labelText == "" then
                            modalDim

                         else
                            black
                        )
                    , Element.mouseOver [ Font.color germanZeroYellow ]
                    ]
                    (text
                        (if labelText == "" then
                            "label"

                         else
                            labelText
                        )
                    )
            , el [ width fill ] Element.none
            , buttons
                [ iconButton
                    (if showGraph then
                        FeatherIcons.eye

                     else
                        FeatherIcons.eyeOff
                    )
                    (ToggleShowGraphClicked id)
                , iconButton FeatherIcons.copy (DuplicateInterestListClicked id)
                , dangerousIconButton FeatherIcons.trash2 (RemoveInterestListClicked id)
                ]
            ]
        , column [ width fill, spacing 40 ]
            [ if showGraph then
                viewChart chartHovering shortPathLabels interestListTable

              else
                Element.none
            , viewInterestListTableAsTable shortPathLabels id interestListTable
            ]
        ]


viewModel : Model -> Element Msg
viewModel model =
    let
        topBar =
            row
                ([ width fill
                 , padding sizes.large
                 , Border.color black
                 , Border.widthEach { bottom = 2, top = 0, left = 0, right = 0 }
                 ]
                    ++ fonts.explorer
                )
                [ text "LocalZero Explorer"
                , el [ width fill ] Element.none
                , buttons
                    [ iconButton FeatherIcons.download DownloadClicked
                    , iconButton FeatherIcons.upload UploadClicked
                    ]
                ]

        interestLists =
            Pivot.indexAbsolute model.interestLists
                |> Pivot.toList
                |> List.map
                    (\( pos, il ) ->
                        let
                            activePos =
                                Pivot.lengthL model.interestLists
                        in
                        viewInterestList pos model.editingActiveInterestListLabel (pos == activePos) il model.chartHovering model.runs
                    )
    in
    column
        [ width fill
        , height (minimum 0 fill)
        ]
        [ topBar
        , row
            [ width fill
            , height (minimum 0 fill)
            , spacing sizes.large
            ]
            [ viewResultsPane model
            , el
                [ width fill
                , height (minimum 0 fill)
                , Element.inFront
                    (floatingActionButton FeatherIcons.plus NewInterestListClicked)
                ]
                (column
                    [ width fill
                    , height (minimum 0 fill)
                    , scrollbarY
                    , spacing sizes.medium
                    , padding sizes.medium
                    ]
                    interestLists
                )
            ]
        ]


viewModalDialogBox : String -> Element Msg -> Element Msg
viewModalDialogBox title content =
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
            , column
                [ width (minimum 600 fill)
                , height (minimum 400 fill)
                , padding sizes.large
                ]
                [ el
                    [ width fill
                    , Font.color white
                    , Background.color germanZeroYellow
                    , Font.size 24
                    , padding 8
                    ]
                    (text title)
                , el
                    [ Background.color white
                    , width fill
                    , height fill
                    , padding sizes.medium
                    ]
                    content
                ]
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
        , spacing sizes.medium
        ]
        [ Input.text []
            { label = Input.labelLeft labelStyle (text "AGS")
            , text = inputs.ags
            , onChange = ModalMsg << CalculateModalAgsUpdated
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
            , onChange = ModalMsg << CalculateModalTargetYearUpdated << round
            , value = toFloat inputs.year
            , thumb = Input.defaultThumb
            }
        , iconButton (size32 FeatherIcons.check) (CalculateModalOkClicked maybeNdx inputs)
        ]


view : Model -> Html Msg
view model =
    let
        dialog =
            case model.showModal of
                Nothing ->
                    Element.none

                Just modalState ->
                    let
                        ( title, content ) =
                            case modalState of
                                PrepareCalculate maybeNdx inputs overrides ->
                                    ( case maybeNdx of
                                        Nothing ->
                                            "Add new generator run"

                                        Just ndx ->
                                            "Change generator run " ++ String.fromInt ndx
                                    , viewCalculateModal maybeNdx inputs overrides
                                    )

                                Loading ->
                                    ( "Loading"
                                    , paragraph [ width fill, height fill ]
                                        [ text "This should be done immediately. If it doesn't go away something is probably broken." ]
                                    )

                                LoadFailure msg ->
                                    ( "Loading failed", text msg )
                    in
                    viewModalDialogBox title content
    in
    Element.layout
        [ width fill
        , height fill
        , Element.inFront dialog
        ]
        (viewModel model)
