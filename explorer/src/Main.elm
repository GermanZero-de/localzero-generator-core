port module Main exposing (..)

--import Element.Background as Background

import AgsIndex exposing (AgsIndex)
import AllRuns
    exposing
        ( AllRuns
        , RunId
        )
import Browser
import Browser.Dom
import Cells
import Chart as C
import Chart.Attributes as CA
import Chart.Events
import Chart.Item
import Cmd.Extra exposing (addCmd, withCmd, withNoCmd)
import CollapseStatus exposing (CollapseStatus, allCollapsed, isCollapsed)
import Dict exposing (Dict)
import Diff exposing (Diff(..))
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
import EnterInputsDialog
import Explorable
import FeatherIcons
import File exposing (File)
import File.Download as Download
import File.Select
import Filter
import GeneratorRpc
import Html exposing (Html, p)
import Html.Attributes
import Html5.DragDrop as DragDrop exposing (droppable)
import Json.Decode as Decode
import Json.Encode as Encode
import JsonRpc
import KeyBindings exposing (noModifiers, shift)
import Keyboard.Key as K
import Lens exposing (Lens)
import Lens.CellContent as CellContent
import List.Extra
import Maybe.Extra
import Pivot exposing (Pivot)
import Process
import Run exposing (OverrideHandling(..), Path, Run)
import Set exposing (Set)
import Storage
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
        , scrollableText
        , size16
        , size32
        , sizes
        , treeElementStyle
        , white
        )
import Task
import Tree exposing (Node(..), Tree)
import Value exposing (Value(..))
import ValueSet exposing (ValueSet)


bind m k msg =
    -- In this project I'm not using the ability to generate documentations for key bindings
    KeyBindings.bind m k msg ""



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
    { runId : RunId
    , name : String
    , value : String
    , asFloat : Maybe Float
    }


type alias ActiveSearch =
    { runId : RunId
    , pattern : String
    , result : Tree.Tree Value.MaybeWithTrace
    }


{-| Position of interestlist in pivot
-}
type alias LensId =
    Int


type alias ChartHovering =
    List (Chart.Item.Many (List String) Chart.Item.Any)


type alias DiffId =
    ( RunId, RunId )


type alias DiffData =
    { diff : Tree (Diff Value.MaybeWithTrace)
    , tolerance : Float -- 0 to 100.0
    }


type DropTarget
    = DropOnCell LensId Cells.Pos Lens.CellContent
    | DropInNewColumn LensId Cells.Pos
    | DropInNewRow LensId Cells.Pos


type DropSource
    = DragFromRun RunId Path
    | DragFromCell LensId Cells.Pos Lens.CellContent


type alias DragDrop =
    DragDrop.Model DropSource DropTarget


type alias Model =
    { runs : AllRuns
    , collapseStatus : CollapseStatus
    , lenses : Pivot Lens
    , editingActiveLensLabel : Bool
    , showModal : Maybe ModalState
    , activeOverrideEditor : Maybe ActiveOverrideEditor
    , activeSearch : Maybe ActiveSearch
    , chartHovering : ChartHovering
    , diffs : Dict DiffId DiffData
    , selectedForComparison : Maybe RunId
    , leftPaneWidth : Int
    , dragDrop : DragDrop
    , displayedTrace : List DisplayedTrace
    , agsIndex : AgsIndex
    , showingSidebar : Bool
    , temporaryHighlight : Maybe Run.Path
    }


type alias DisplayedTrace =
    { runId : AllRuns.RunId
    , path : Path
    , value : Value
    , trace : Value.Trace
    , expanded : Set Path
    , showInfo : Maybe GeneratorRpc.Info
    }


type ModalState
    = EnterInputs (Maybe RunId) EnterInputsDialog.State Run.Overrides
    | Loading
    | ErrorMessage String String
    | ReMap ReMapModalState


type alias ReMapModalState =
    { lensId : LensId
    , mapping : Dict RunId RunId
    }


filterFieldId : String
filterFieldId =
    "filter"


port save : Encode.Value -> Cmd msg


port copyToClipboard : Encode.Value -> Cmd msg


port scrollIntoView : String -> Cmd msg


toClipboardData : Lens -> AllRuns -> Encode.Value
toClipboardData lens allRuns =
    let
        valueSet =
            ValueSet.create lens allRuns

        encodeCell : Lens.CellContent -> Encode.Value
        encodeCell content =
            case content of
                CellContent.ValueAt r p ->
                    let
                        value =
                            Dict.get ( r, p ) valueSet.values
                                |> Maybe.map .value
                                |> Maybe.withDefault Value.Null
                    in
                    case value of
                        Value.Float f ->
                            Encode.string (String.fromFloat f)

                        Value.String s ->
                            Encode.string s

                        Value.Null ->
                            Encode.string ""

                CellContent.Label s ->
                    Encode.string s
    in
    case Lens.getCells lens of
        Nothing ->
            Encode.string "Copying classic lenses not supported yet"

        Just cells ->
            Cells.toList cells
                |> Encode.list (Encode.list encodeCell)


initiateInfo : String -> Model -> ( Model, Cmd Msg )
initiateInfo name model =
    ( model -- TODO: Think about showing a loading spinner
    , GeneratorRpc.info { name = name, toMsg = GotInfo }
    )


initiateCalculate : Maybe RunId -> Run.Inputs -> Run.Entries -> Run.Overrides -> Model -> ( Model, Cmd Msg )
initiateCalculate maybeNdx inputs entries overrides model =
    ( { model | showModal = Just Loading }
    , GeneratorRpc.calculate
        { inputs = inputs
        , overrides = overrides
        , toMsg = GotGeneratorResult maybeNdx inputs entries overrides
        }
    )


initiateMakeEntries : Maybe RunId -> Run.Inputs -> Run.Overrides -> Model -> ( Model, Cmd Msg )
initiateMakeEntries maybeNdx inputs overrides model =
    ( { model | showModal = Just Loading }
    , GeneratorRpc.makeEntries { inputs = inputs, toMsg = GotEntries maybeNdx inputs overrides }
    )


initiateListAgs : Model -> ( Model, Cmd Msg )
initiateListAgs model =
    ( { model | showModal = Just Loading }
    , GeneratorRpc.listAgs { toMsg = GotListAgs }
    )


activateLens : LensId -> Model -> Model
activateLens id model =
    { model
        | lenses = Pivot.withRollback (Pivot.goTo id) model.lenses
    }


init : Decode.Value -> ( Model, Cmd Msg )
init storage =
    { runs = AllRuns.empty
    , showModal = Nothing
    , lenses = Pivot.singleton Lens.empty
    , editingActiveLensLabel = False
    , collapseStatus = allCollapsed
    , activeOverrideEditor = Nothing
    , activeSearch = Nothing
    , chartHovering = []
    , diffs = Dict.empty
    , selectedForComparison = Nothing
    , leftPaneWidth = 600
    , dragDrop = DragDrop.init
    , displayedTrace = []
    , agsIndex = AgsIndex.init []
    , showingSidebar = True
    , temporaryHighlight = Nothing
    }
        |> update (LocalStorageLoaded storage)



-- UPDATE


type Msg
    = -- Running the generator
      GotGeneratorResult (Maybe RunId) Run.Inputs Run.Entries Run.Overrides (JsonRpc.RpcData (Tree Value.MaybeWithTrace))
    | GotEntries (Maybe RunId) Run.Inputs Run.Overrides (JsonRpc.RpcData Run.Entries)
    | GotListAgs (JsonRpc.RpcData (List GeneratorRpc.AgsData))
    | GotInfo (JsonRpc.RpcData GeneratorRpc.Info)
      -- trace handling
    | DisplayTrace RunId Path Value Value.Trace
    | CloseTrace Int -- Number of steps to pop
    | ExpandInTrace Path
    | CollapseInTrace Path
    | FactOrAssTraceInfoRequest String
    | CloseInfo
      -- Override handling
    | AddOrUpdateOverrideClicked RunId String Float
    | RemoveOverrideClicked RunId String
    | OverrideEdited RunId String String
    | OverrideEditFinished
      -- Filter
    | FilterEdited RunId String
    | FilterFinished
    | FilterQuickAddRequested RunId
      -- Tree navigation
    | ToggleCollapseTreeClicked Explorable.Id Path
    | Highlight RunId Path
    | HighlightRemove
      -- Modal dialog
    | ModalMsg ModalMsg
    | DisplayCalculateModalClicked (Maybe RunId) { agsFilter : String, year : Int } Run.Overrides
    | CalculateModalOkClicked (Maybe RunId) Run.Inputs Run.Overrides
    | RemoveExplorableClicked Explorable.Id
    | ModalDismissed
    | DisplayReMapModalClicked LensId
    | ReMapModalOkClicked LensId (Dict RunId RunId)
      -- Lens Modifications
    | AddToLensClicked RunId Run.Path
    | RemoveFromLensClicked LensId (List ( RunId, Run.Path ))
    | LensLabelEdited LensId String
    | LensLabelEditFinished
    | DuplicateLensClicked LensId
    | RemoveLensClicked LensId
    | ActivateLensClicked LensId
    | NewLensClicked
    | NewTableClicked
    | LensTableEditModeChanged LensId (Maybe Lens.TableEditMode)
    | AddRowToLensTableClicked LensId Int
    | AddColumnToLensTableClicked LensId Int
    | CellOfLensTableEdited LensId Cells.Pos Lens.CellContent
    | CellOfLensTableEditFinished LensId Cells.Pos Lens.CellContent
    | MoveToCellRequested RunId Path LensId Cells.Pos
    | SwapCellsRequested LensId Cells.Pos Lens.CellContent LensId Cells.Pos Lens.CellContent
    | MoveIntoNewColumnRequested (Maybe ( LensId, Cells.Pos )) Lens.CellContent LensId Cells.Pos
    | MoveIntoNewRowRequested (Maybe ( LensId, Cells.Pos )) Lens.CellContent LensId Cells.Pos
    | MoveCellEditorRequested LensId Cells.Pos Lens.CellContent Cells.Pos Lens.CellContent
    | DeleteRowClicked LensId Int
    | DeleteColumnClicked LensId Int
    | CopyToClipboardRequested LensId
      -- Graphics
    | ToggleShowGraphClicked LensId
    | OnChartHover ChartHovering
      -- Upload / Download / Storage
    | DownloadClicked
    | UploadClicked
    | FileUploaded File
    | FileContentLoaded String
    | LocalStorageLoaded Decode.Value
      -- Misc
    | Noop
    | LeftPaneMoved Int
    | DragDropMsg (DragDrop.Msg DropSource DropTarget)
      -- Comparison
    | ToggleSelectForCompareClicked RunId
    | DiffToleranceUpdated RunId RunId Float
    | ToggleSidebar
    | ScrollIntoView String


type ModalMsg
    = UpdateEnterInputs EnterInputsDialog.State
    | ReMapChangeMapping RunId RunId


getActiveLens : Model -> Lens
getActiveLens model =
    Pivot.getC model.lenses


mapActiveLens : (Lens -> Lens) -> Model -> Model
mapActiveLens f =
    mapLenses (Pivot.mapC f)


mapLenses : (Pivot Lens -> Pivot Lens) -> Model -> Model
mapLenses f m =
    { m | lenses = f m.lenses }


withErrorMessage : String -> String -> Model -> ( Model, Cmd Msg )
withErrorMessage title msg model =
    ( { model | showModal = Just (ErrorMessage title msg) }, Cmd.none )


withEditingActiveLensLabel : Bool -> Model -> Model
withEditingActiveLensLabel b m =
    { m | editingActiveLensLabel = b }


downloadCmd : Model -> Cmd msg
downloadCmd model =
    let
        content =
            Storage.encode { interestLists = Pivot.toList model.lenses }
                |> Encode.encode 0
    in
    Download.string "explorer.json" "text/json" content


saveCmd : Model -> Cmd msg
saveCmd model =
    let
        content =
            Storage.encode { interestLists = Pivot.toList model.lenses }
    in
    save content


withSaveCmd : Model -> ( Model, Cmd Msg )
withSaveCmd model =
    model
        |> withCmd (saveCmd model)


removeRunAndDiffsThatDependOnIt : RunId -> Model -> Model
removeRunAndDiffsThatDependOnIt runId model =
    let
        newDiffs =
            Dict.filter (\( runA, runB ) _ -> runA /= runId && runB /= runId) model.diffs
    in
    { model | runs = AllRuns.remove runId model.runs, diffs = newDiffs }


removeDiff : RunId -> RunId -> Model -> Model
removeDiff aId bId model =
    { model | diffs = Dict.remove ( aId, bId ) model.diffs }


insertDiff : RunId -> RunId -> DiffData -> Model -> Model
insertDiff runA runB diffData model =
    { model | diffs = Dict.insert ( runA, runB ) diffData model.diffs }


callIf : Bool -> (a -> a) -> a -> a
callIf p f x =
    if p then
        f x

    else
        x


callIfJust : Maybe x -> (x -> a -> a) -> a -> a
callIfJust mb fn x =
    case mb of
        Just a ->
            fn a x

        Nothing ->
            x


mapHead : (a -> a) -> List a -> List a
mapHead fn l =
    case l of
        [] ->
            []

        x :: xs ->
            fn x :: xs


mapExpanded : (Set Path -> Set Path) -> DisplayedTrace -> DisplayedTrace
mapExpanded fn dt =
    { dt | expanded = fn dt.expanded }


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Noop ->
            model
                |> withNoCmd

        Highlight r p ->
            { model
                | collapseStatus =
                    CollapseStatus.expandUntil (Explorable.Run r) p model.collapseStatus
                , temporaryHighlight = Just p
            }
                |> withCmd
                    (Cmd.batch
                        [ Task.perform (always (ScrollIntoView (treeItemId (Explorable.Run r) p))) (Process.sleep 50)
                        , Task.perform (always HighlightRemove) (Process.sleep 3000.0)
                        ]
                    )

        ScrollIntoView id ->
            model
                |> withCmd (scrollIntoView id)

        HighlightRemove ->
            { model | temporaryHighlight = Nothing }
                |> withNoCmd

        -- |> withCmd (Task.attempt HighlightGetElement (Browser.Dom.getElement ()
        ToggleSidebar ->
            { model | showingSidebar = not model.showingSidebar }
                |> withNoCmd

        -- |> withNoCmd
        DisplayTrace runId path value trace ->
            { model | displayedTrace = { runId = runId, path = path, value = value, trace = trace, expanded = Set.empty, showInfo = Nothing } :: model.displayedTrace }
                |> withNoCmd

        ExpandInTrace path ->
            { model | displayedTrace = mapHead (mapExpanded (Set.insert path)) model.displayedTrace }
                |> withNoCmd

        CollapseInTrace path ->
            { model | displayedTrace = mapHead (mapExpanded (Set.remove path)) model.displayedTrace }
                |> withNoCmd

        CloseTrace n ->
            { model | displayedTrace = List.drop n model.displayedTrace }
                |> withNoCmd

        CloseInfo ->
            { model | displayedTrace = mapHead (\dt -> { dt | showInfo = Nothing }) model.displayedTrace }
                |> withNoCmd

        FactOrAssTraceInfoRequest name ->
            initiateInfo name model

        AddRowToLensTableClicked id num ->
            model
                |> activateLens id
                |> mapActiveLens (Lens.mapCells (Cells.addRow num))
                |> withSaveCmd

        AddColumnToLensTableClicked id num ->
            model
                |> activateLens id
                |> mapActiveLens (Lens.mapCells (Cells.addColumn num))
                |> withSaveCmd

        DownloadClicked ->
            model
                |> withCmd (downloadCmd model)

        UploadClicked ->
            model
                |> withCmd (File.Select.file [ "text/json" ] FileUploaded)

        FileUploaded file ->
            model
                |> withCmd (Task.perform FileContentLoaded (File.toString file))

        LocalStorageLoaded value ->
            case Decode.decodeValue (Decode.nullable Storage.decoder) value of
                Err e ->
                    model
                        |> withErrorMessage "Failed to load previous session"
                            (Decode.errorToString e)

                Ok Nothing ->
                    -- no previous localstorage
                    model
                        |> initiateListAgs

                Ok (Just storage) ->
                    let
                        ls =
                            case Pivot.fromList storage.interestLists of
                                Nothing ->
                                    model.lenses

                                Just i ->
                                    i
                    in
                    { model | lenses = ls }
                        |> initiateListAgs

        FileContentLoaded content ->
            case Decode.decodeString Storage.decoder content of
                Err e ->
                    model
                        |> withErrorMessage "Failed to load file"
                            (Decode.errorToString e)

                Ok storage ->
                    let
                        ls =
                            case Pivot.fromList storage.interestLists of
                                Nothing ->
                                    model.lenses

                                Just i ->
                                    i
                    in
                    { model | lenses = ls }
                        |> withSaveCmd

        GotListAgs response ->
            case JsonRpc.flat response of
                JsonRpc.RpcResult ad ->
                    { model
                        | showModal = Nothing
                        , agsIndex = AgsIndex.init ad
                    }
                        |> withNoCmd

                JsonRpc.RpcErr _ ->
                    model
                        |> withErrorMessage "Failed to call list-ags rpc"
                            "rpc failed"

                JsonRpc.HttpErr _ ->
                    model
                        |> withErrorMessage "Failed to call list-ags rpc"
                            "HTTP failed"

        GotInfo response ->
            case JsonRpc.flat response of
                JsonRpc.RpcResult info ->
                    { model
                        | displayedTrace = mapHead (\dt -> { dt | showInfo = Just info }) model.displayedTrace
                    }
                        |> withNoCmd

                JsonRpc.RpcErr _ ->
                    model
                        |> withErrorMessage "Failed to call info rpc"
                            "rpc failed"

                JsonRpc.HttpErr _ ->
                    model
                        |> withErrorMessage "Failed to call info rpc"
                            "HTTP failed"

        GotEntries maybeRunId inputs overrides response ->
            case JsonRpc.flat response of
                JsonRpc.RpcResult e ->
                    model
                        |> initiateCalculate maybeRunId inputs e overrides

                JsonRpc.RpcErr _ ->
                    model
                        |> withErrorMessage "Failed to call make-entries rpc"
                            "rpc failed"

                JsonRpc.HttpErr _ ->
                    model
                        |> withErrorMessage "Failed to call make-entries rpc"
                            "HTTP failed"

        GotGeneratorResult maybeRunId inputs entries overrides response ->
            case JsonRpc.flat response of
                JsonRpc.RpcErr _ ->
                    model
                        |> withErrorMessage "Failed to call calculate rpc"
                            "rpc failed"

                JsonRpc.HttpErr _ ->
                    model
                        |> withErrorMessage "Failed to call calculate rpc"
                            "HTTP failed"

                JsonRpc.RpcResult result ->
                    let
                        run =
                            Run.create
                                { inputs = inputs
                                , entries = entries
                                , result = result
                                , overrides = overrides
                                }

                        modelWithRun =
                            { model
                                | runs =
                                    case maybeRunId of
                                        Nothing ->
                                            AllRuns.add run model.runs

                                        Just runId ->
                                            AllRuns.set runId run model.runs
                            }

                        newDiffs =
                            case maybeRunId of
                                Nothing ->
                                    modelWithRun.diffs

                                Just runId ->
                                    modelWithRun.diffs
                                        |> Dict.map
                                            (\( runA, runB ) diffData ->
                                                if runA == runId || runB == runId then
                                                    -- A input into the diff was recomputed. Recompute the diff
                                                    case diffRunsById runA runB diffData.tolerance modelWithRun of
                                                        Nothing ->
                                                            -- If elm had panic I should panic
                                                            diffData

                                                        Just d ->
                                                            d

                                                else
                                                    diffData
                                            )
                    in
                    { modelWithRun
                        | diffs = newDiffs
                        , showModal = Nothing
                    }
                        |> withSaveCmd

        ToggleCollapseTreeClicked i path ->
            { model | collapseStatus = CollapseStatus.toggle i path model.collapseStatus }
                |> withNoCmd

        RemoveExplorableClicked id ->
            case id of
                Explorable.Run runId ->
                    removeRunAndDiffsThatDependOnIt runId model
                        |> withSaveCmd

                Explorable.Diff runA runB ->
                    removeDiff runA runB model
                        |> withNoCmd

        ModalMsg modalMsg ->
            updateModal modalMsg model.showModal model.agsIndex
                |> Tuple.mapFirst (\md -> { model | showModal = md })
                |> Tuple.mapSecond (Cmd.map ModalMsg)

        ModalDismissed ->
            { model | showModal = Nothing }
                |> withNoCmd

        DisplayCalculateModalClicked maybeNdx { agsFilter, year } overrides ->
            let
                modal =
                    EnterInputs maybeNdx (EnterInputsDialog.init year agsFilter model.agsIndex) overrides
            in
            { model | showModal = Just modal }
                |> withNoCmd

        DisplayReMapModalClicked lensId ->
            let
                newModel =
                    model
                        |> activateLens lensId

                lens =
                    getActiveLens newModel

                valueSet =
                    ValueSet.create lens model.runs

                mapping =
                    valueSet.runs
                        |> List.map (\ri -> ( ri, ri ))
                        |> Dict.fromList
            in
            { model | showModal = Just (ReMap { lensId = lensId, mapping = mapping }) }
                |> withNoCmd

        CalculateModalOkClicked maybeNdx inputs overrides ->
            model
                |> initiateMakeEntries maybeNdx inputs overrides

        ReMapModalOkClicked lensId mapping ->
            { model | showModal = Nothing }
                |> activateLens lensId
                |> mapActiveLens
                    (Lens.mapCells
                        (Cells.map
                            (\cc ->
                                case cc of
                                    CellContent.ValueAt ri p ->
                                        CellContent.ValueAt
                                            (Dict.get ri mapping |> Maybe.withDefault ri)
                                            p

                                    CellContent.Label _ ->
                                        cc
                            )
                        )
                    )
                |> withSaveCmd

        AddOrUpdateOverrideClicked ndx name f ->
            { model
                | runs =
                    model.runs
                        |> AllRuns.update ndx (Run.mapOverrides (Dict.insert name f))
            }
                |> withSaveCmd

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
            in
            { model | activeSearch = newActiveSearch }
                |> withCmd (Task.attempt (\_ -> Noop) (Browser.Dom.focus filterFieldId))

        FilterQuickAddRequested run ->
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
                        |> mapActiveLens
                            (\lens ->
                                List.foldl (\p i -> Lens.insert run p i) lens paths
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
            case AllRuns.get runId model.runs of
                Nothing ->
                    ( model, Cmd.none )

                Just run ->
                    { model
                        | activeOverrideEditor =
                            model.activeOverrideEditor
                                |> Maybe.Extra.filter (\e -> e.runId /= runId || e.name /= name)
                    }
                        |> initiateMakeEntries (Just runId)
                            (Run.getInputs run)
                            (Run.getOverrides run
                                |> Dict.remove name
                            )

        AddToLensClicked runId path ->
            model
                |> mapActiveLens (Lens.insert runId path)
                |> withSaveCmd

        RemoveFromLensClicked lensId what ->
            model
                |> activateLens lensId
                |> mapActiveLens (Lens.removeList what)
                |> withSaveCmd

        ToggleShowGraphClicked lensId ->
            model
                |> activateLens lensId
                |> mapActiveLens Lens.toggleShowGraph
                |> withSaveCmd

        NewLensClicked ->
            model
                |> mapLenses (Pivot.appendGoR Lens.empty)
                |> withSaveCmd

        NewTableClicked ->
            model
                |> mapLenses (Pivot.appendGoR Lens.emptyTable)
                |> withSaveCmd

        DuplicateLensClicked id ->
            model
                |> activateLens id
                |> mapLenses
                    (\p ->
                        Pivot.appendGoR
                            (Pivot.getC p
                                |> Lens.mapLabel (\l -> l ++ " Copy")
                            )
                            p
                    )
                |> withSaveCmd

        RemoveLensClicked id ->
            model
                |> activateLens id
                |> mapLenses
                    (\ils ->
                        case Pivot.removeGoR ils of
                            Nothing ->
                                -- If List was singleton, delete becomes
                                -- reset to empty
                                Maybe.withDefault (Pivot.singleton Lens.empty) (Pivot.removeGoL ils)

                            Just without ->
                                without
                    )
                |> withSaveCmd

        LensTableEditModeChanged id mode ->
            model
                |> activateLens id
                |> mapActiveLens (Lens.setTableEditMode mode)
                |> withSaveCmd

        DeleteRowClicked id row ->
            model
                |> activateLens id
                |> mapActiveLens
                    (Lens.mapCells
                        (Cells.deleteRow row
                            >> Cells.ifHasAZeroDimensionReplaceByOneCell
                        )
                    )
                |> withSaveCmd

        DeleteColumnClicked id column ->
            model
                |> activateLens id
                |> mapActiveLens
                    (Lens.mapCells
                        (Cells.deleteColumn column
                            >> Cells.ifHasAZeroDimensionReplaceByOneCell
                        )
                    )
                |> withSaveCmd

        MoveCellEditorRequested id currentPos currentValue nextPos nextValue ->
            -- NOTE: This event may happen BEFORE we have saved the currently
            -- edited cell (because loseFocus hasn't happened yet)
            model
                |> activateLens id
                |> mapActiveLens (Lens.mapCells (Cells.set currentPos currentValue))
                |> mapActiveLens
                    (Lens.setTableEditMode (Just (Lens.Cell nextPos nextValue)))
                |> withSaveCmd
                |> addCmd
                    (Task.attempt (\_ -> Noop) (Browser.Dom.focus "cell"))

        CellOfLensTableEditFinished id pos value ->
            -- NOTE: This event may happen after MoveCellEditorRequested has changed
            -- the TableEditMode
            model
                |> mapActiveLens
                    (Lens.mapTableEditMode
                        (Maybe.map
                            (\me ->
                                case me of
                                    Lens.All ->
                                        Lens.All

                                    Lens.Cell p _ ->
                                        if p == pos then
                                            -- Only if we haven't moved away already quit edit cell mode
                                            Lens.All

                                        else
                                            me
                            )
                        )
                    )
                |> mapActiveLens (Lens.mapCells (Cells.set pos value))
                |> withSaveCmd

        CellOfLensTableEdited id pos value ->
            model
                |> activateLens id
                |> mapActiveLens (Lens.setTableEditMode (Just (Lens.Cell pos value)))
                |> withSaveCmd
                |> addCmd
                    (Task.attempt (\_ -> Noop) (Browser.Dom.focus "cell"))

        CopyToClipboardRequested id ->
            let
                lens =
                    getActiveLens model
            in
            model
                |> withCmd (copyToClipboard (toClipboardData lens model.runs))

        ActivateLensClicked id ->
            model
                |> activateLens id
                |> withSaveCmd

        LensLabelEdited id newLabel ->
            model
                |> activateLens id
                |> withEditingActiveLensLabel True
                |> mapActiveLens (Lens.mapLabel (always newLabel))
                |> withCmd
                    (Task.attempt (\_ -> Noop) (Browser.Dom.focus "interestlabel"))

        LensLabelEditFinished ->
            model
                |> withEditingActiveLensLabel False
                |> withSaveCmd

        OnChartHover hovering ->
            { model | chartHovering = hovering }
                |> withNoCmd

        DiffToleranceUpdated aId bId newTolerance ->
            case diffRunsById aId bId newTolerance model of
                Nothing ->
                    model
                        |> withNoCmd

                Just d ->
                    model
                        |> insertDiff aId bId d
                        |> withSaveCmd

        ToggleSelectForCompareClicked runId ->
            case model.selectedForComparison of
                Nothing ->
                    { model | selectedForComparison = Just runId }
                        |> withNoCmd

                Just r ->
                    if r == runId then
                        { model | selectedForComparison = Nothing }
                            |> withNoCmd

                    else
                        let
                            idA =
                                r

                            idB =
                                runId

                            withoutComparison =
                                { model | selectedForComparison = Nothing }
                        in
                        case diffRunsById idA idB Value.defaultTolerance withoutComparison of
                            Nothing ->
                                withoutComparison
                                    |> withNoCmd

                            Just d ->
                                withoutComparison
                                    |> insertDiff idA idB d
                                    |> withSaveCmd

        LeftPaneMoved w ->
            { model | leftPaneWidth = w }
                |> withNoCmd

        MoveToCellRequested runId path lensId cellPos ->
            model
                |> activateLens lensId
                |> mapActiveLens (Lens.mapCells (Cells.set cellPos (CellContent.ValueAt runId path)))
                |> withSaveCmd

        MoveIntoNewRowRequested sourceCell cv1 l2 p2 ->
            model
                |> mapLenses
                    (Pivot.indexAbsolute
                        >> Pivot.mapA
                            (\( lensId, lens ) ->
                                lens
                                    |> callIfJust sourceCell
                                        (\( l1, p1 ) ->
                                            callIf (lensId == l1)
                                                (Lens.mapCells (Cells.set p1 (CellContent.Label "")))
                                        )
                                    |> callIf (lensId == l2)
                                        (Lens.mapCells
                                            (Cells.addRow p2.row
                                                >> Cells.set p2 cv1
                                            )
                                        )
                            )
                    )
                |> withSaveCmd

        MoveIntoNewColumnRequested sourceCell cv1 l2 p2 ->
            model
                |> mapLenses
                    (Pivot.indexAbsolute
                        >> Pivot.mapA
                            (\( lensId, lens ) ->
                                lens
                                    |> callIfJust sourceCell
                                        (\( l1, p1 ) ->
                                            callIf (lensId == l1)
                                                (Lens.mapCells
                                                    (Cells.set p1 (CellContent.Label ""))
                                                )
                                        )
                                    |> callIf (lensId == l2)
                                        (Lens.mapCells
                                            (Cells.addColumn p2.column
                                                >> Cells.set p2 cv1
                                            )
                                        )
                            )
                    )
                |> withSaveCmd

        SwapCellsRequested l1 p1 cv1 l2 p2 cv2 ->
            model
                |> mapLenses
                    (Pivot.indexAbsolute
                        >> Pivot.mapA
                            (\( lensId, lens ) ->
                                lens
                                    |> callIf (lensId == l1)
                                        (Lens.mapCells (Cells.set p1 cv2))
                                    |> callIf (lensId == l2)
                                        (Lens.mapCells (Cells.set p2 cv1))
                            )
                    )
                |> withSaveCmd

        DragDropMsg dragMsg ->
            let
                ( newDragDrop, dropEvent ) =
                    DragDrop.update dragMsg model.dragDrop

                applyDrop =
                    case dropEvent of
                        Nothing ->
                            identity

                        Just ( DragFromRun runId path, DropOnCell lensId pos _ ) ->
                            Cmd.Extra.andThen (update (MoveToCellRequested runId path lensId pos))

                        Just ( DragFromCell l1 p1 cv1, DropOnCell l2 p2 cv2 ) ->
                            Cmd.Extra.andThen (update (SwapCellsRequested l1 p1 cv1 l2 p2 cv2))

                        Just ( DragFromCell l1 p1 cv1, DropInNewRow l2 p2 ) ->
                            Cmd.Extra.andThen (update (MoveIntoNewRowRequested (Just ( l1, p1 )) cv1 l2 p2))

                        Just ( DragFromRun runId path, DropInNewRow l2 p2 ) ->
                            Cmd.Extra.andThen
                                (update (MoveIntoNewRowRequested Nothing (CellContent.ValueAt runId path) l2 p2))

                        Just ( DragFromRun runId path, DropInNewColumn l2 p2 ) ->
                            Cmd.Extra.andThen
                                (update (MoveIntoNewColumnRequested Nothing (CellContent.ValueAt runId path) l2 p2))

                        Just ( DragFromCell l1 p1 cv1, DropInNewColumn l2 p2 ) ->
                            Cmd.Extra.andThen (update (MoveIntoNewColumnRequested (Just ( l1, p1 )) cv1 l2 p2))
            in
            { model | dragDrop = newDragDrop }
                |> withCmd (DragDrop.fixFirefoxDragStartCmd dragMsg)
                |> applyDrop


diffRunsById : RunId -> RunId -> Float -> Model -> Maybe DiffData
diffRunsById idA idB tolerance model =
    case ( AllRuns.get idA model.runs, AllRuns.get idB model.runs ) of
        ( Nothing, _ ) ->
            Nothing

        ( _, Nothing ) ->
            Nothing

        ( Just runA, Just runB ) ->
            let
                diff =
                    Diff.diff (Value.isValueEqual (tolerance / 100.0))
                        (Run.getTree WithOverrides runA)
                        (Run.getTree WithOverrides runB)

                diffData =
                    { diff = diff, tolerance = tolerance }
            in
            Just diffData


updateModal : ModalMsg -> Maybe ModalState -> AgsIndex -> ( Maybe ModalState, Cmd ModalMsg )
updateModal msg model agsIndex =
    case model of
        Nothing ->
            Nothing
                |> withNoCmd

        Just (EnterInputs ndx _ overrides) ->
            case msg of
                UpdateEnterInputs ei ->
                    Just (EnterInputs ndx ei overrides)
                        |> withNoCmd

                ReMapChangeMapping _ _ ->
                    model
                        |> withNoCmd

        Just (ReMap reMapState) ->
            case msg of
                ReMapChangeMapping a b ->
                    Just (ReMap { reMapState | mapping = Dict.insert a b reMapState.mapping })
                        |> withNoCmd

                UpdateEnterInputs _ ->
                    model
                        |> withNoCmd

        Just Loading ->
            Just Loading
                |> withNoCmd

        Just (ErrorMessage title m) ->
            Just (ErrorMessage title m)
                |> withNoCmd



-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none



-- VIEW


viewChart : ChartHovering -> Dict Run.Path String -> ValueSet -> Element Msg
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
                                case Dict.get ( runId, path ) interestListTable.values |> Maybe.map .value of
                                    Just (Float f) ->
                                        f

                                    Just (String _) ->
                                        0.0

                                    Just Null ->
                                        0.0

                                    Nothing ->
                                        0.0
                        in
                        C.bar get [ CA.color (Styling.runColorForChart runId) ]
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


collapsedStatusIcon : Bool -> Element msg
collapsedStatusIcon collapsed =
    let
        i =
            if collapsed then
                FeatherIcons.chevronRight

            else
                FeatherIcons.chevronDown
    in
    el iconButtonStyle (icon (size16 i))


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
                            -- TODO: textStyle is a bad name for this. Restructure!
                            case editor.asFloat of
                                Nothing ->
                                    [ Border.color red, Border.width 1 ]

                                Just _ ->
                                    [ KeyBindings.on
                                        [ bind noModifiers K.Enter OverrideEditFinished
                                        ]
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
    { isCollapsed : Run.Path -> Bool
    , collapsedToggledMsg : Run.Path -> msg
    , viewLeaf : Run.Path -> String -> leaf -> List (Element msg)
    , itemId : Run.Path -> String
    , temporaryHighlight : Maybe Run.Path
    }
    -> Run.Path
    -> Tree leaf
    -> Element msg
viewTree cfg path tree =
    if cfg.isCollapsed path then
        Element.none

    else
        Dict.toList tree
            |> List.map
                (\( name, val ) ->
                    let
                        childPath =
                            path ++ [ name ]

                        maybeHighlight =
                            if Just childPath == cfg.temporaryHighlight then
                                [ Border.glow Styling.highlightColor 1.0 ]

                            else
                                []

                        itemRow content =
                            row
                                ([ spacing sizes.large
                                 , width fill
                                 , Element.htmlAttribute (Html.Attributes.id (cfg.itemId childPath))
                                 ]
                                    ++ maybeHighlight
                                    ++ treeElementStyle
                                )
                                content

                        element =
                            case val of
                                Tree child ->
                                    column [ width fill ]
                                        [ Input.button [ width fill, Element.focused [] ]
                                            { label =
                                                itemRow
                                                    [ collapsedStatusIcon (cfg.isCollapsed childPath)
                                                    , el [ width fill ] (text name)
                                                    , el (Font.italic :: Font.alignRight :: fonts.explorerNodeSize) <|
                                                        text (String.fromInt (Dict.size child))
                                                    ]
                                            , onPress = Just (cfg.collapsedToggledMsg childPath)
                                            }
                                        , viewTree cfg
                                            childPath
                                            child
                                        ]

                                Leaf leaf ->
                                    itemRow <| cfg.viewLeaf path name leaf
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


nullValueElement : Element msg
nullValueElement =
    el (Font.alignRight :: Font.bold :: fonts.explorerValues) <| text "null"


viewStringValue : String -> Element msg
viewStringValue s =
    el (Font.alignRight :: fonts.explorerValues) <| text s


viewFloatValue : Float -> Element msg
viewFloatValue f =
    el (Font.alignRight :: fonts.explorerValues) <|
        text (formatGermanNumber f)


viewValue : Value -> Element msg
viewValue v =
    case v of
        Null ->
            nullValueElement

        String s ->
            viewStringValue s

        Float f ->
            viewFloatValue f


runsAndComparisonsViewPortId : String
runsAndComparisonsViewPortId =
    "runs-and-comparisons"


treeItemId : Explorable.Id -> Run.Path -> String
treeItemId runId path =
    String.fromInt (Explorable.toComparable runId) ++ "_" ++ String.join "-" path


viewValueTree :
    RunId
    -> LensId
    -> Run.Path
    -> Maybe Run.Path
    -> (RunId -> Run.Path -> Bool)
    -> Lens
    -> Run.Overrides
    -> Maybe ActiveOverrideEditor
    -> Tree Value.MaybeWithTrace
    -> Element Msg
viewValueTree runId lensId path temporaryHighlight checkIsCollapsed lens overrides activeOverrideEditor tree =
    let
        viewLeaf : Run.Path -> String -> Value.MaybeWithTrace -> List (Element Msg)
        viewLeaf pathToParent name valueWithTrace =
            case valueWithTrace.value of
                Null ->
                    [ el [ width (px 16) ] Element.none
                    , el [ width fill ] (text name)
                    , nullValueElement
                    ]

                String s ->
                    [ el [ width (px 16) ] Element.none
                    , el [ width fill ] (text name)
                    , viewStringValue s
                    ]

                Float f ->
                    let
                        isEntry =
                            pathToParent == [ "entries" ]

                        thisPath =
                            pathToParent ++ [ name ]

                        button =
                            if Lens.member runId thisPath lens then
                                dangerousIconButton (size16 FeatherIcons.trash2)
                                    (RemoveFromLensClicked lensId [ ( runId, thisPath ) ])

                            else
                                iconButton (size16 FeatherIcons.plus) (AddToLensClicked runId thisPath)

                        ( originalValue, maybeOverride ) =
                            -- Clicking on original value should start or revert
                            -- an override
                            if isEntry then
                                viewEntryAndOverride runId name overrides activeOverrideEditor f

                            else
                                ( viewFloatValue f
                                , Element.none
                                )
                    in
                    [ button
                    , case valueWithTrace.trace of
                        Nothing ->
                            iconButton (size16 FeatherIcons.info) Noop

                        Just t ->
                            iconButton (size16 FeatherIcons.info)
                                (DisplayTrace
                                    runId
                                    thisPath
                                    valueWithTrace.value
                                    t
                                )
                    , el
                        (width fill
                            :: List.map Element.htmlAttribute
                                (DragDrop.draggable DragDropMsg (DragFromRun runId thisPath))
                        )
                        (text name)
                    , originalValue
                    , maybeOverride
                    ]
    in
    viewTree
        { isCollapsed = checkIsCollapsed runId
        , collapsedToggledMsg = ToggleCollapseTreeClicked (Explorable.Run runId)
        , viewLeaf = viewLeaf
        , itemId = treeItemId (Explorable.Run runId)
        , temporaryHighlight = temporaryHighlight
        }
        path
        tree


buttons : List (Element Msg) -> Element Msg
buttons l =
    row [ Element.spacingXY sizes.medium 0 ] l


viewDiffTree : Explorable.Id -> Maybe Run.Path -> CollapseStatus -> Tree (Diff.Diff Value.MaybeWithTrace) -> Element Msg
viewDiffTree id temporaryHighlight collapseStatus tree =
    let
        missingElement =
            el (Font.alignRight :: fonts.explorerValues) <|
                text "∅"

        viewLeaf : Run.Path -> String -> Diff.Diff Value.MaybeWithTrace -> List (Element Msg)
        viewLeaf pathToParent name leaf =
            -- TODO: Make the diff display something useful in more cases
            case leaf of
                LeftOnly v ->
                    [ el [ width fill ] (text name)
                    , viewValue v.value
                    , missingElement
                    ]

                Unequal a b ->
                    [ el [ width fill ] (text name)
                    , viewValue a.value
                    , viewValue b.value
                    ]

                RightOnly v ->
                    [ el [ width fill ] (text name)
                    , missingElement
                    , viewValue v.value
                    ]
    in
    viewTree
        { isCollapsed = \p -> isCollapsed id p collapseStatus
        , collapsedToggledMsg = ToggleCollapseTreeClicked id
        , viewLeaf = viewLeaf
        , itemId = treeItemId id
        , temporaryHighlight = temporaryHighlight
        }
        []
        tree


viewComparison : RunId -> RunId -> Maybe Run.Path -> CollapseStatus -> DiffData -> Element Msg
viewComparison aId bId temporaryHighlight collapseStatus diffData =
    let
        id =
            Explorable.Diff aId bId
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
            [ Input.button treeElementStyle
                { label =
                    row [ spacing sizes.medium ]
                        [ collapsedStatusIcon (isCollapsed id [] collapseStatus)
                        , row [] [ viewRunId [] aId, text " ≈ ", viewRunId [] bId ]
                        ]
                , onPress = Just (ToggleCollapseTreeClicked id [])
                }
            , Input.slider
                [ height (px 20)
                , Element.behindContent
                    (el
                        [ width fill
                        , Font.center
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
                        (text (">" ++ formatGermanNumber diffData.tolerance ++ "%"))
                    )
                ]
                { label = Input.labelHidden "tolerance"
                , min = 0.001
                , max = 100.0
                , step = Just 0.001
                , onChange = DiffToleranceUpdated aId bId
                , value = diffData.tolerance
                , thumb = Input.defaultThumb
                }
            , buttons
                [ -- differentIfFilterActive.filterButton
                  dangerousIconButton FeatherIcons.trash2 (RemoveExplorableClicked id)
                ]
            ]

        --, differentIfFilterActive.filterPatternField
        , viewDiffTree
            id
            temporaryHighlight
            collapseStatus
            diffData.diff
        ]


viewRun : RunId -> LensId -> Maybe Path -> Lens -> CollapseStatus -> Maybe ActiveOverrideEditor -> Maybe ActiveSearch -> Maybe RunId -> Run -> Element Msg
viewRun runId lensId temporaryHighlight lens collapseStatus activeOverrideEditor activeSearch selectedForComparison run =
    let
        inputs =
            Run.getInputs run

        overrides =
            Run.getOverrides run

        isSelectedForComparison =
            case selectedForComparison of
                Nothing ->
                    False

                Just ri ->
                    ri == runId

        selectForComparisonButton =
            if isSelectedForComparison then
                dangerousIconButton
                    FeatherIcons.trello
                    (ToggleSelectForCompareClicked runId)

            else
                iconButton
                    FeatherIcons.trello
                    (ToggleSelectForCompareClicked runId)

        differentIfFilterActive =
            case activeSearch |> Maybe.Extra.filter (\s -> s.runId == runId) of
                Nothing ->
                    { filterButton = iconButton FeatherIcons.filter (FilterEdited runId "")
                    , treeToDisplay = Run.getTree WithoutOverrides run
                    , isCollapsed = \r p -> isCollapsed (Explorable.Run r) p collapseStatus
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
                                , KeyBindings.on
                                    [ bind noModifiers K.Escape FilterFinished
                                    , bind noModifiers K.Enter (FilterQuickAddRequested runId)
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
                        , viewRunId [] runId
                        , text (inputs.ags ++ " " ++ String.fromInt inputs.year)
                        ]
                , onPress = Just (ToggleCollapseTreeClicked (Explorable.Run runId) [])
                }
            , buttons
                [ differentIfFilterActive.filterButton
                , selectForComparisonButton
                , iconButton FeatherIcons.edit (DisplayCalculateModalClicked (Just runId) { agsFilter = inputs.ags, year = inputs.year } overrides)
                , iconButton FeatherIcons.copy (DisplayCalculateModalClicked Nothing { agsFilter = inputs.ags, year = inputs.year } overrides)
                , dangerousIconButton FeatherIcons.trash2 (RemoveExplorableClicked (Explorable.Run runId))
                ]
            ]
        , differentIfFilterActive.filterPatternField
        , viewValueTree
            runId
            lensId
            []
            temporaryHighlight
            differentIfFilterActive.isCollapsed
            lens
            overrides
            activeOverrideEditor
            differentIfFilterActive.treeToDisplay
        ]


defaultInputs : { agsFilter : String, year : Int }
defaultInputs =
    { agsFilter = ""
    , year = 2035
    }


{-| The pane on the left hand side containing the results
-}
viewRunsAndComparisons : Model -> Element Msg
viewRunsAndComparisons model =
    column
        [ height fill
        , spacing sizes.large
        , padding sizes.large
        , height (minimum 0 fill)
        , width (px model.leftPaneWidth)
        , Element.inFront
            (floatingActionButton FeatherIcons.plus (DisplayCalculateModalClicked Nothing defaultInputs Dict.empty))
        ]
        [ el
            [ scrollbarY
            , width fill
            , height fill
            , Element.htmlAttribute (Html.Attributes.id runsAndComparisonsViewPortId)
            ]
            (column
                [ spacing sizes.large
                , width fill
                , height fill
                ]
                ((AllRuns.toList model.runs
                    |> List.map
                        (\( resultNdx, ir ) ->
                            viewRun resultNdx
                                (Pivot.lengthL model.lenses)
                                model.temporaryHighlight
                                (getActiveLens model)
                                model.collapseStatus
                                model.activeOverrideEditor
                                model.activeSearch
                                model.selectedForComparison
                                ir
                        )
                 )
                    ++ (model.diffs
                            |> Dict.toList
                            |> List.map
                                (\( ( a, b ), diffData ) ->
                                    viewComparison a b model.temporaryHighlight model.collapseStatus diffData
                                )
                       )
                )
            )
        ]


type TableElement
    = Data Int
    | GapBefore Int


tableElementFromIndex : Int -> TableElement
tableElementFromIndex ndx =
    let
        element =
            ndx // 2
    in
    if remainderBy 2 ndx == 0 then
        GapBefore element

    else
        Data element


viewValueSetAsUserDefinedTable : LensId -> DragDrop -> Lens.TableData -> ValueSet -> Element Msg
viewValueSetAsUserDefinedTable lensId dragDrop td valueSet =
    let
        ifEditing =
            if td.editing /= Nothing then
                identity

            else
                always []

        viewCell : Lens.CellContent -> Cells.Pos -> Element Msg
        viewCell cell pos =
            let
                onClick =
                    ifEditing
                        [ Events.onClick
                            (CellOfLensTableEdited lensId pos cell)
                        ]

                dropTarget =
                    ifEditing
                        (List.map Element.htmlAttribute
                            (DragDrop.droppable DragDropMsg (DropOnCell lensId pos cell))
                        )

                draggable =
                    ifEditing
                        (List.map Element.htmlAttribute
                            (DragDrop.draggable DragDropMsg (DragFromCell lensId pos cell))
                        )

                highlight =
                    ifEditing <|
                        case DragDrop.getDropId dragDrop of
                            Nothing ->
                                []

                            Just (DropOnCell li p _) ->
                                if lensId == li && p == pos then
                                    [ Background.color Styling.germanZeroYellow
                                    , Border.glow Styling.germanZeroYellow 2
                                    ]

                                else
                                    []

                            Just (DropInNewColumn _ _) ->
                                []

                            Just (DropInNewRow _ _) ->
                                []

                cellElement attrs v =
                    el
                        (([ Background.color Styling.emptyCellColor
                          , width fill
                          , padding 3
                          , Element.htmlAttribute <| Html.Attributes.tabindex 0
                          ]
                            ++ onClick
                            ++ fonts.table
                            ++ dropTarget
                            ++ highlight
                            ++ draggable
                         )
                            ++ attrs
                        )
                        v

                displayLabel l =
                    if l == "" then
                        cellElement [] (text " ")

                    else
                        cellElement [ Font.bold ] (paragraph [] [ text l ])

                viewPath : List String -> Element msg
                viewPath p =
                    paragraph [] (List.map text (List.intersperse "." p))

                viewAbsolutePath ( runId, path ) =
                    row []
                        [ viewRunId [] runId
                        , text " "
                        , viewPath path
                        ]

                displayCell =
                    case cell of
                        CellContent.Label l ->
                            displayLabel l

                        CellContent.ValueAt r p ->
                            let
                                value =
                                    Dict.get ( r, p ) valueSet.values
                            in
                            if td.editing /= Nothing then
                                -- We are in editing mode, but not editing THIS cell.
                                -- So display the path itself
                                cellElement []
                                    (viewAbsolutePath ( r, p ))

                            else
                                -- We are not in editing mode at all. Display the value at the
                                -- path
                                case value of
                                    Nothing ->
                                        -- Making the compiler happy
                                        cellElement [ Font.alignRight ] (text "INTERNAL ERROR")

                                    Just valueAndTrace ->
                                        let
                                            onValueClick =
                                                Events.onClick (Highlight r p)
                                        in
                                        case valueAndTrace.value of
                                            Float f ->
                                                cellElement [ onValueClick, Font.alignRight ] (text (formatGermanNumber f))

                                            Null ->
                                                cellElement [ onValueClick, Font.alignRight, Font.bold ] (text "null")

                                            String s ->
                                                cellElement
                                                    [ onValueClick
                                                    , Font.alignRight
                                                    , Font.family [ Font.monospace ]
                                                    ]
                                                    (text
                                                        (if s == "" then
                                                            " "

                                                         else
                                                            s
                                                        )
                                                    )
            in
            case td.editing of
                Nothing ->
                    displayCell

                Just Lens.All ->
                    displayCell

                Just (Lens.Cell p editValue) ->
                    if p == pos then
                        let
                            tabKey =
                                case Cells.nextPos pos td.grid of
                                    Nothing ->
                                        []

                                    Just nextPos ->
                                        [ bind noModifiers
                                            K.Tab
                                            (MoveCellEditorRequested lensId
                                                pos
                                                editValue
                                                nextPos
                                                (Cells.get nextPos td.grid)
                                            )
                                        ]

                            shiftTabKey =
                                case Cells.prevPos pos td.grid of
                                    Nothing ->
                                        []

                                    Just prevPos ->
                                        [ bind shift
                                            K.Tab
                                            (MoveCellEditorRequested lensId
                                                pos
                                                editValue
                                                prevPos
                                                (Cells.get prevPos td.grid)
                                            )
                                        ]
                        in
                        Input.text
                            ([ width fill
                             , Font.bold
                             , padding 3
                             , Events.onLoseFocus (CellOfLensTableEditFinished lensId pos editValue)
                             , KeyBindings.on
                                ([ bind noModifiers K.Enter (CellOfLensTableEditFinished lensId pos editValue)
                                 , bind noModifiers K.Escape (LensTableEditModeChanged lensId (Just Lens.All))
                                 ]
                                    ++ tabKey
                                    ++ shiftTabKey
                                )
                             , Element.htmlAttribute <| Html.Attributes.id "cell"
                             , Element.focused
                                [ Border.innerGlow germanZeroYellow 1.0
                                ]
                             ]
                                ++ fonts.table
                            )
                            { onChange = CellOfLensTableEdited lensId pos << CellContent.Label
                            , text = CellContent.getLabel editValue |> Maybe.withDefault ""
                            , placeholder =
                                CellContent.getValueAt cell
                                    |> Maybe.map (viewAbsolutePath >> Input.placeholder [])
                            , label = Input.labelHidden "label"
                            }

                    else
                        displayCell

        separator isColumn pos =
            let
                highlight : List (Element.Attribute Msg)
                highlight =
                    ifEditing <|
                        let
                            background =
                                Background.color germanZeroGreen
                        in
                        case DragDrop.getDropId dragDrop of
                            Nothing ->
                                [ background
                                , Events.onClick
                                    (if isColumn then
                                        AddColumnToLensTableClicked lensId pos.column

                                     else
                                        AddRowToLensTableClicked lensId pos.row
                                    )
                                , Element.mouseOver
                                    [ Background.color germanZeroYellow
                                    ]
                                ]

                            Just (DropInNewRow li p) ->
                                if lensId == li && pos == p && not isColumn then
                                    [ Background.color germanZeroYellow, Border.glow germanZeroYellow 2 ]

                                else
                                    [ background ]

                            Just (DropOnCell _ _ _) ->
                                [ background ]

                            Just (DropInNewColumn li p) ->
                                if lensId == li && pos == p && isColumn then
                                    [ Background.color germanZeroYellow, Border.glow germanZeroYellow 2 ]

                                else
                                    [ background ]

                droppable =
                    ifEditing <|
                        if DragDrop.getDropId dragDrop /= Nothing then
                            List.map Element.htmlAttribute
                                (DragDrop.droppable DragDropMsg
                                    (if isColumn then
                                        DropInNewColumn lensId pos

                                     else
                                        DropInNewRow lensId pos
                                    )
                                )

                        else
                            []
            in
            el
                ([ width
                    (if isColumn then
                        px sizes.tableGap

                     else
                        fill
                    )
                 , height
                    (if isColumn then
                        fill

                     else
                        px sizes.tableGap
                    )
                 , Border.rounded 2
                 ]
                    ++ highlight
                    ++ droppable
                )
                Element.none

        deleteRowButtonColumn =
            { header = Element.none
            , width = shrink
            , view =
                \rowNdx ->
                    case tableElementFromIndex rowNdx of
                        GapBefore _ ->
                            Element.none

                        Data row ->
                            dangerousIconButton
                                (FeatherIcons.withSize (toFloat sizes.tableFontSize) FeatherIcons.trash2)
                                (DeleteRowClicked lensId row)
            }

        columnDefs =
            List.Extra.initialize (Cells.columns td.grid * 2 + 1)
                (\columnNdx ->
                    let
                        columnElement =
                            tableElementFromIndex columnNdx
                    in
                    { header =
                        if td.editing == Nothing then
                            Element.none

                        else
                            case columnElement of
                                GapBefore _ ->
                                    Element.none

                                Data column ->
                                    el [ centerX ] <|
                                        dangerousIconButton
                                            (FeatherIcons.withSize (toFloat sizes.tableFontSize) FeatherIcons.trash2)
                                            (DeleteColumnClicked lensId column)
                    , width =
                        case columnElement of
                            GapBefore _ ->
                                px sizes.tableGap

                            Data _ ->
                                shrink |> Element.minimum 60 |> Element.maximum 300
                    , view =
                        \rowNdx ->
                            case ( tableElementFromIndex rowNdx, columnElement ) of
                                ( GapBefore _, GapBefore _ ) ->
                                    Element.none

                                ( GapBefore row, Data column ) ->
                                    separator False { row = row, column = column }

                                ( Data row, GapBefore column ) ->
                                    separator True { row = row, column = column }

                                ( Data row, Data column ) ->
                                    let
                                        pos =
                                            { row = row, column = column }
                                    in
                                    viewCell (Cells.get pos td.grid) pos
                    }
                )
    in
    Element.column []
        [ Element.row [ spacing sizes.small, Font.size sizes.tableFontSize ]
            [ text "Showing values of "
            , case valueSet.runs of
                [] ->
                    text "nothing"

                _ ->
                    Input.button
                        []
                        { label =
                            row [ spacing sizes.small ]
                                (List.map (viewRunId []) valueSet.runs)
                        , onPress = Just (DisplayReMapModalClicked lensId)
                        }
            ]
        , Element.table
            [ padding sizes.large
            ]
            { columns =
                case td.editing of
                    Nothing ->
                        columnDefs

                    Just _ ->
                        deleteRowButtonColumn :: columnDefs
            , data = List.range 0 (Cells.rows td.grid * 2)
            }
        ]


viewRunId : List (Element.Attribute msg) -> RunId -> Element msg
viewRunId attrs runId =
    el
        (attrs
            ++ [ Font.bold
               , Font.color (Styling.runColorForUI runId)
               ]
        )
        (text (String.fromInt runId))


{-| View valueset as table of values
where the rows are indexed by path names and the columns by runs
-}
viewValueSetAsClassicTable : Dict Run.Path String -> LensId -> ValueSet -> Element Msg
viewValueSetAsClassicTable shortPathLabels lensId valueSet =
    let
        dataColumns =
            valueSet.runs
                |> List.map
                    (\runId ->
                        { header = viewRunId [ Font.alignRight ] runId
                        , width = shrink
                        , view =
                            \path ->
                                let
                                    value =
                                        case Dict.get ( runId, path ) valueSet.values |> Maybe.map .value of
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
                    let
                        removeMsg =
                            valueSet.runs
                                |> List.map
                                    (\runId ->
                                        ( runId, path )
                                    )
                                |> RemoveFromLensClicked lensId
                    in
                    dangerousIconButton (size16 FeatherIcons.trash2) removeMsg
            }
    in
    Element.table
        [ width fill
        , height shrink
        , spacing sizes.large
        , padding sizes.large
        ]
        { data = valueSet.paths
        , columns = shortPathLabelColumn :: dataColumns ++ [ deleteColumn ]
        }


viewLens : LensId -> DragDrop -> Bool -> Bool -> Lens -> ChartHovering -> AllRuns -> Element Msg
viewLens id dragDrop editingActiveLensLabel isActive lens chartHovering allRuns =
    let
        valueSet =
            ValueSet.create lens allRuns

        showGraph =
            Lens.getShowGraph lens

        labelText =
            Lens.getLabel lens

        shortPathLabels =
            Lens.getShortPathLabels lens

        ( borderColor, borderWidth ) =
            if isActive then
                ( germanZeroYellow, 2 )

            else
                ( germanZeroGreen, 1 )

        maybeEditTableButton =
            case Lens.asUserDefinedTable lens of
                Nothing ->
                    Element.none

                Just t ->
                    if t.editing == Nothing then
                        iconButton FeatherIcons.edit
                            (LensTableEditModeChanged id (Just Lens.All))

                    else
                        iconButton FeatherIcons.check (LensTableEditModeChanged id Nothing)

        maybeShowGraphButton =
            case Lens.asUserDefinedTable lens of
                Nothing ->
                    iconButton
                        (if showGraph then
                            FeatherIcons.eye

                         else
                            FeatherIcons.eyeOff
                        )
                        (ToggleShowGraphClicked id)

                Just _ ->
                    Element.none

        maybeCopyToClipboardButton =
            case Lens.asUserDefinedTable lens of
                Nothing ->
                    Element.none

                Just t ->
                    iconButton FeatherIcons.clipboard (CopyToClipboardRequested id)
    in
    column
        [ width fill
        , Events.onClick (ActivateLensClicked id)
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
            [ if editingActiveLensLabel && isActive then
                Input.text
                    [ Events.onLoseFocus LensLabelEditFinished
                    , KeyBindings.on
                        [ bind noModifiers K.Enter LensLabelEditFinished
                        ]
                    , Element.htmlAttribute (Html.Attributes.id "interestlabel")
                    , padding sizes.small
                    ]
                    { onChange = LensLabelEdited id
                    , text = labelText
                    , label = Input.labelHidden "interest list"
                    , placeholder = Just (Input.placeholder [] (text "label"))
                    }

              else
                el
                    [ Events.onClick (LensLabelEdited id labelText)
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
                [ maybeEditTableButton
                , maybeShowGraphButton
                , maybeCopyToClipboardButton
                , iconButton FeatherIcons.copy (DuplicateLensClicked id)
                , dangerousIconButton FeatherIcons.trash2 (RemoveLensClicked id)
                ]
            ]
        , column [ width fill, spacing 40, padding sizes.large ]
            [ if showGraph then
                viewChart chartHovering shortPathLabels valueSet

              else
                Element.none
            , case Lens.asUserDefinedTable lens of
                Nothing ->
                    viewValueSetAsClassicTable shortPathLabels id valueSet

                Just g ->
                    viewValueSetAsUserDefinedTable id dragDrop g valueSet
            ]
        ]


viewRunsAndInterestLists : Model -> Element Msg
viewRunsAndInterestLists model =
    let
        interestLists =
            Pivot.indexAbsolute model.lenses
                |> Pivot.toList
                |> List.map
                    (\( pos, il ) ->
                        let
                            activePos =
                                Pivot.lengthL model.lenses
                        in
                        viewLens pos
                            model.dragDrop
                            model.editingActiveLensLabel
                            (pos == activePos)
                            il
                            model.chartHovering
                            model.runs
                    )

        sidebar =
            if model.showingSidebar then
                [ viewRunsAndComparisons model
                , el
                    [ width (px 2)
                    , Background.color black
                    , height fill
                    ]
                    Element.none
                ]

            else
                []
    in
    row
        [ width fill
        , height (minimum 0 fill)
        , spacing sizes.large
        ]
        (sidebar
            ++ [ el
                    [ width fill
                    , height (minimum 0 fill)
                    , Element.inFront
                        (row
                            [ spacing 10
                            , Element.alignBottom
                            , Element.moveUp 10
                            , Element.alignRight
                            , padding 0
                            ]
                            [ floatingActionButton FeatherIcons.plus NewLensClicked
                            , floatingActionButton FeatherIcons.grid NewTableClicked
                            ]
                        )
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
        )


viewTraceAsBlocks : Set Path -> RunId -> AllRuns -> Value.Trace -> Element Msg
viewTraceAsBlocks expanded runId allRuns t =
    let
        nameText s =
            el [ Font.size Styling.sizes.tableFontSize ] <| text s
    in
    case t of
        Value.DataTrace { source, key, attr, value } ->
            row
                [ spacing sizes.small
                , padding sizes.medium
                , Border.solid
                , Border.width 1
                , Border.color Styling.modalDim
                , width fill
                ]
                [ nameText (source ++ "[" ++ key ++ "]." ++ attr)
                , el [ Element.alignRight ] <| viewValue (Float value)
                ]

        Value.LiteralTrace f ->
            el
                [ height fill
                , padding sizes.medium
                , Border.solid
                , Border.width 1
                , Border.color Styling.modalDim
                , width fill
                ]
                (el [ Element.alignRight ] <| viewValue (Float f))

        Value.NameTrace { name } ->
            let
                path =
                    String.split "." name

                shorterPath =
                    String.join "."
                        -- We truncate result in the display
                        (case path of
                            "result" :: rest ->
                                rest

                            _ ->
                                path
                        )

                nameElement =
                    nameText shorterPath
            in
            case AllRuns.getValue Run.WithOverrides runId path allRuns of
                Just leaf ->
                    case leaf.trace of
                        Nothing ->
                            nameElement

                        Just nestedTrace ->
                            if Set.member path expanded then
                                column
                                    [ spacing sizes.small
                                    , padding sizes.medium
                                    , Border.solid
                                    , Border.width 1
                                    , Border.color Styling.modalDim
                                    , width fill
                                    ]
                                    [ row [ spacing sizes.small, width fill ]
                                        [ el [ Element.alignTop ] <| iconButton FeatherIcons.chevronDown (CollapseInTrace path)
                                        , column [ spacing sizes.small, width fill ]
                                            [ row [ width fill, spacing sizes.small ]
                                                [ Input.button []
                                                    { onPress = Just (DisplayTrace runId path leaf.value nestedTrace)
                                                    , label = nameElement
                                                    }
                                                , el [ Element.alignRight ] <| viewValue leaf.value
                                                ]
                                            , viewTraceAsBlocks expanded runId allRuns nestedTrace
                                            ]
                                        ]
                                    ]

                            else
                                column
                                    [ spacing sizes.small
                                    , padding sizes.medium
                                    , Border.solid
                                    , Border.width 1
                                    , Border.color Styling.modalDim
                                    , width fill
                                    ]
                                    [ row [ spacing sizes.small, width fill ]
                                        [ el [ Element.alignTop ] <| iconButton FeatherIcons.chevronRight (ExpandInTrace path)
                                        , column [ spacing sizes.small, width fill ]
                                            [ row [ width fill, spacing sizes.small ]
                                                [ Input.button []
                                                    { onPress = Just (DisplayTrace runId path leaf.value nestedTrace)
                                                    , label = nameElement
                                                    }
                                                , el [ Element.alignRight ] <| viewValue leaf.value
                                                ]
                                            ]
                                        ]
                                    ]

                Nothing ->
                    nameElement

        Value.FactOrAssTrace { fact_or_ass, value } ->
            row
                [ spacing sizes.small
                , padding sizes.medium
                , Border.solid
                , Border.width 1
                , Border.color Styling.modalDim
                , width fill
                ]
                [ el [ Events.onClick (FactOrAssTraceInfoRequest fact_or_ass) ] <| nameText fact_or_ass
                , el [ Element.alignRight ] <| viewValue (Float value)
                ]

        Value.UnaryTrace { unary, a } ->
            row
                [ spacing sizes.small
                , padding sizes.medium
                , Border.solid
                , Border.width 1
                , Border.color Styling.modalDim
                , width fill
                ]
                [ el [ Font.center, width fill ] <|
                    case unary of
                        Value.UnaryMinus ->
                            text "-"

                        Value.UnaryPlus ->
                            text "+"
                , viewTraceAsBlocks expanded runId allRuns a
                ]

        Value.BinaryTrace bTrace ->
            let
                ( op, bgColor ) =
                    case bTrace.binary of
                        Value.Plus ->
                            ( "+"
                            , Element.rgb255 194 255 153
                              -- mint green
                            )

                        Value.Minus ->
                            ( "-"
                            , Element.rgb255 255 153 153
                              -- salmon pink
                            )

                        Value.Times ->
                            ( "*"
                            , Element.rgb255 153 252 255
                              -- electric blue
                            )

                        Value.Divide ->
                            ( "/"
                            , Element.rgb255 255 236 173
                              -- medium champagne
                            )
            in
            column
                [ spacing sizes.small
                , padding sizes.medium
                , Border.solid
                , Border.width 1
                , Border.color bgColor
                , width fill
                ]
                [ el [ Element.alignRight ] <| viewValue (Float bTrace.value)
                , row [ width fill ]
                    [ el [ Font.center, width fill ] <| text op
                    , column [ spacing sizes.medium, padding sizes.small ]
                        (List.map
                            (viewTraceAsBlocks expanded runId allRuns)
                            (Value.binaryTraceToList bTrace)
                        )
                    ]
                ]


viewInfo : GeneratorRpc.Info -> Element Msg
viewInfo { label, description, value, unit, rationale, reference, link } =
    column [ width fill, height fill, padding sizes.medium, spacing sizes.small, Events.onClick CloseInfo ]
        [ paragraph fonts.explorer [text label, text " -- ", text description]
        , row ( spacing sizes.small :: fonts.explorerValues) [ text (formatGermanNumber value), text unit ]
        , paragraph fonts.explorerItems [text rationale]
        , el fonts.explorerItems (text reference)
        , Element.link fonts.explorerItems { url = link, label = text link }
        ]

viewDisplayedTrace : AllRuns -> List Path -> DisplayedTrace -> Element Msg
viewDisplayedTrace allRuns breadcrumbs { runId, path, expanded, value, trace, showInfo } =
    let
        breadcrumbsWithCloseActions =
            breadcrumbs
                |> List.reverse
                |> List.indexedMap (\n b -> ( b, CloseTrace (n + 1) ))
                |> List.reverse
    in
    column
        [ width fill
        , height fill
        , padding sizes.large
        ]
        [ row [ width fill, padding sizes.medium, spacing sizes.small ]
            [ row [ width fill, padding sizes.medium, spacing sizes.small, Font.size 12 ]
                (List.intersperse (icon (FeatherIcons.withSize 12 <| FeatherIcons.chevronRight)) <|
                    List.map
                        (\( b, a ) ->
                            Input.button [] { onPress = Just a, label = text (String.join "." b) }
                        )
                        breadcrumbsWithCloseActions
                )
            , iconButton FeatherIcons.x (CloseTrace (List.length breadcrumbs + 1))
            ]
        ,
            case showInfo of
                Nothing ->
                    el [] <| viewTraceAsBlocks (Set.insert path expanded) runId allRuns (Value.NameTrace { name = String.join "." path })
                Just info ->
                    viewInfo info
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
                    [ (if model.showingSidebar then
                        dangerousIconButton

                       else
                        iconButton
                      )
                        FeatherIcons.sidebar
                        ToggleSidebar
                    , iconButton FeatherIcons.download DownloadClicked
                    , iconButton FeatherIcons.upload UploadClicked
                    ]
                ]
    in
    column
        [ width fill
        , height (minimum 0 fill)
        ]
        [ topBar
        , case model.displayedTrace of
            [] ->
                viewRunsAndInterestLists model

            dt :: dts ->
                viewDisplayedTrace model.runs (List.map .path dts) dt
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
                [ row
                    [ width fill
                    , Font.color white
                    , Background.color germanZeroYellow
                    , Font.size 24
                    , padding 8
                    ]
                    [ el [ width fill ] <| text title
                    , el
                        [ padding 2
                        , Background.color white
                        , Border.rounded 5
                        ]
                      <|
                        iconButton FeatherIcons.x ModalDismissed
                    ]
                , el
                    [ Background.color white
                    , width fill
                    , height (minimum 0 fill)
                    , padding sizes.medium
                    ]
                    content
                ]
            , filler
            ]
        , filler
        ]


viewRunReMapModal : ReMapModalState -> AllRuns -> Element Msg
viewRunReMapModal { lensId, mapping } allRuns =
    let
        listOfMappings =
            Dict.toList mapping

        allActualRuns =
            allRuns
                |> AllRuns.toList
                |> List.map Tuple.first

        allMissingRuns =
            Dict.keys mapping
                |> List.filter (\ri -> AllRuns.get ri allRuns == Nothing)

        options =
            (allActualRuns ++ allMissingRuns)
                -- dedup
                |> Set.fromList
                |> Set.toList
                |> List.map
                    (\ri ->
                        Input.option ri (viewRunId [ Element.moveDown 1 ] ri)
                    )
    in
    column
        [ width fill
        , height fill
        , spacing sizes.medium
        ]
        ((listOfMappings
            |> List.map
                (\( fromRunId, toRunId ) ->
                    Input.radioRow
                        [ spacing (2 * sizes.large) ]
                        { onChange = ModalMsg << ReMapChangeMapping fromRunId
                        , options = options
                        , selected = Just toRunId
                        , label =
                            Input.labelLeft [ Element.paddingXY sizes.large 0 ]
                                (row (spacing sizes.medium :: fonts.explorer)
                                    [ viewRunId [ Element.moveDown 1 ] fromRunId
                                    , icon
                                        (FeatherIcons.withSize (toFloat sizes.fontSize)
                                            FeatherIcons.arrowRight
                                        )
                                    ]
                                )
                        }
                )
         )
            ++ [ iconButton
                    (size32 FeatherIcons.check)
                    (ReMapModalOkClicked lensId mapping)
               ]
        )


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
                                EnterInputs maybeNdx state overrides ->
                                    ( case maybeNdx of
                                        Nothing ->
                                            "Add new generator run"

                                        Just ndx ->
                                            "Change generator run " ++ String.fromInt ndx
                                    , EnterInputsDialog.view
                                        (ModalMsg << UpdateEnterInputs)
                                        (\i -> CalculateModalOkClicked maybeNdx i overrides)
                                        state
                                    )

                                Loading ->
                                    ( "Loading"
                                    , scrollableText
                                        "This should be done immediately. If it doesn't go away something is probably broken."
                                    )

                                ErrorMessage t m ->
                                    ( t, scrollableText m )

                                ReMap reMapState ->
                                    ( "Change which runs are shown"
                                    , viewRunReMapModal reMapState model.runs
                                    )
                    in
                    viewModalDialogBox title content
    in
    Element.layout
        [ width fill
        , height fill
        , Element.inFront dialog
        ]
        (viewModel model)
