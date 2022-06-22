port module Main exposing (Model, Msg(..), init, main, subscriptions, update, view)

--import Element.Background as Background

import AllRuns
    exposing
        ( AllRuns
        , RunId
        )
import Array
import Browser
import Browser.Dom
import Cells
import Chart as C
import Chart.Attributes as CA
import Chart.Events
import Chart.Item
import Cmd.Extra exposing (withCmd, withNoCmd)
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
import Explorable
import FeatherIcons
import File exposing (File)
import File.Download as Download
import File.Select
import Filter
import Html exposing (Html, p)
import Html.Attributes
import Html.Events
import Html5.DragDrop as DragDrop exposing (droppable)
import Http
import Json.Decode as Decode
import Json.Encode as Encode
import Lens exposing (Lens)
import List.Extra
import Maybe.Extra
import Pivot exposing (Pivot)
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
    , result : Tree.Tree Value
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
    { diff : Tree (Diff Value)
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
    }


type ModalState
    = PrepareCalculate (Maybe RunId) Run.Inputs Run.Overrides
    | Loading
    | ErrorMessage String String


filterFieldId : String
filterFieldId =
    "filter"


encodeOverrides : Run.Overrides -> Encode.Value
encodeOverrides d =
    Encode.dict
        identity
        Encode.float
        d


port save : Encode.Value -> Cmd msg


initiateCalculate : Maybe RunId -> Run.Inputs -> Run.Entries -> Run.Overrides -> Model -> ( Model, Cmd Msg )
initiateCalculate maybeNdx inputs entries overrides model =
    ( { model | showModal = Just Loading }
    , Http.post
        { url = "http://localhost:4070/calculate/" ++ inputs.ags ++ "/" ++ String.fromInt inputs.year
        , expect = Http.expectJson (GotGeneratorResult maybeNdx inputs entries overrides) (Tree.decoder Value.decoder)
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
    }
        |> update (LocalStorageLoaded storage)



-- UPDATE


type Msg
    = -- Running the generator
      GotGeneratorResult (Maybe RunId) Run.Inputs Run.Entries Run.Overrides (Result Http.Error (Tree Value))
    | GotEntries (Maybe RunId) Run.Inputs Run.Overrides (Result Http.Error Run.Entries)
      -- Override handling
    | AddOrUpdateOverrideClicked RunId String Float
    | RemoveOverrideClicked RunId String
    | OverrideEdited RunId String String
    | OverrideEditFinished
      -- Filter
    | FilterEdited RunId String
    | FilterFinished
    | FilterQuickAddRequested
      -- Tree navigation
    | ToggleCollapseTreeClicked Explorable.Id Path
      -- Modal dialog
    | ModalMsg ModalMsg
    | DisplayCalculateModalClicked (Maybe RunId) Run.Inputs Run.Overrides
    | CalculateModalOkClicked (Maybe RunId) Run.Inputs Run.Overrides
    | RemoveExplorableClicked Explorable.Id
    | ModalDismissed
      -- Lens Modifications
    | AddToLensClicked Run.Path
    | RemoveFromLensClicked LensId Run.Path
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
    | CellOfLensTableEdited LensId Cells.Pos String
    | MoveToCellRequested Path LensId Cells.Pos
    | SwapCellsRequested LensId Cells.Pos Lens.CellContent LensId Cells.Pos Lens.CellContent
    | MoveIntoNewColumnRequested (Maybe ( LensId, Cells.Pos )) Lens.CellContent LensId Cells.Pos
    | MoveIntoNewRowRequested (Maybe ( LensId, Cells.Pos )) Lens.CellContent LensId Cells.Pos
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


type ModalMsg
    = CalculateModalTargetYearUpdated Int
    | CalculateModalAgsUpdated String


mapActiveLens : (Lens -> Lens) -> Model -> Model
mapActiveLens f =
    mapLens (Pivot.mapC f)


mapLens : (Pivot Lens -> Pivot Lens) -> Model -> Model
mapLens f m =
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


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Noop ->
            model
                |> withNoCmd

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
                        |> withNoCmd

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
                        |> withNoCmd

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

        GotEntries maybeRunId inputs overrides (Ok entries) ->
            model
                |> initiateCalculate maybeRunId inputs entries overrides

        GotEntries _ _ _ (Err _) ->
            model
                |> withNoCmd

        GotGeneratorResult maybeRunId inputs entries overrides resultOrError ->
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

                Err (Http.BadUrl s) ->
                    model
                        |> withErrorMessage "BAD URL: " s

                Err Http.Timeout ->
                    model
                        |> withErrorMessage "TIMEOUT" ""

                Err Http.NetworkError ->
                    model
                        |> withErrorMessage "NETWORK ERROR" ""

                Err (Http.BadStatus code) ->
                    model
                        |> withErrorMessage ("BAD STATUS CODE" ++ String.fromInt code)
                            ""

                Err (Http.BadBody error) ->
                    model
                        |> withErrorMessage "Failed to decode" error

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
            updateModal modalMsg model.showModal
                |> Tuple.mapFirst (\md -> { model | showModal = md })
                |> Tuple.mapSecond (Cmd.map ModalMsg)

        ModalDismissed ->
            { model | showModal = Nothing }
                |> withNoCmd

        DisplayCalculateModalClicked maybeNdx inputs overrides ->
            let
                modal =
                    PrepareCalculate maybeNdx inputs overrides
            in
            { model | showModal = Just modal }
                |> withNoCmd

        CalculateModalOkClicked maybeNdx inputs overrides ->
            model
                |> initiateMakeEntries maybeNdx inputs overrides

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
                        |> mapActiveLens
                            (\il ->
                                List.foldl (\p i -> Lens.insert p i) il paths
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

        AddToLensClicked path ->
            model
                |> mapActiveLens (Lens.insert path)
                |> withSaveCmd

        RemoveFromLensClicked id path ->
            model
                |> activateLens id
                |> mapActiveLens (Lens.remove path)
                |> withSaveCmd

        ToggleShowGraphClicked id ->
            model
                |> activateLens id
                |> mapActiveLens Lens.toggleShowGraph
                |> withSaveCmd

        NewLensClicked ->
            model
                |> mapLens (Pivot.appendGoR Lens.empty)
                |> withSaveCmd

        NewTableClicked ->
            model
                |> mapLens (Pivot.appendGoR Lens.emptyTable)
                |> withSaveCmd

        DuplicateLensClicked id ->
            model
                |> activateLens id
                |> mapLens
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
                |> mapLens
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

        CellOfLensTableEdited id pos value ->
            model
                |> activateLens id
                |> mapActiveLens (Lens.setTableEditMode (Just (Lens.Cell pos)))
                |> mapActiveLens (Lens.mapCells (Cells.set pos (Lens.Label value)))
                |> withSaveCmd

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

        MoveToCellRequested path lensId cellPos ->
            model
                |> activateLens lensId
                |> mapActiveLens (Lens.mapCells (Cells.set cellPos (Lens.ValueAt path)))
                |> withSaveCmd

        MoveIntoNewRowRequested sourceCell cv1 l2 p2 ->
            model
                |> mapLens
                    (Pivot.indexAbsolute
                        >> Pivot.mapA
                            (\( lensId, lens ) ->
                                lens
                                    |> callIfJust sourceCell
                                        (\( l1, p1 ) ->
                                            callIf (lensId == l1) (Lens.mapCells (Cells.set p1 (Lens.Label "")))
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
                |> mapLens
                    (Pivot.indexAbsolute
                        >> Pivot.mapA
                            (\( lensId, lens ) ->
                                lens
                                    |> callIfJust sourceCell
                                        (\( l1, p1 ) ->
                                            callIf (lensId == l1) (Lens.mapCells (Cells.set p1 (Lens.Label "")))
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
                |> mapLens
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

                        Just ( DragFromRun _ path, DropOnCell lensId pos _ ) ->
                            Cmd.Extra.andThen (update (MoveToCellRequested path lensId pos))

                        Just ( DragFromCell l1 p1 cv1, DropOnCell l2 p2 cv2 ) ->
                            Cmd.Extra.andThen (update (SwapCellsRequested l1 p1 cv1 l2 p2 cv2))

                        Just ( DragFromCell l1 p1 cv1, DropInNewRow l2 p2 ) ->
                            Cmd.Extra.andThen (update (MoveIntoNewRowRequested (Just ( l1, p1 )) cv1 l2 p2))

                        Just ( DragFromRun _ path, DropInNewRow l2 p2 ) ->
                            Cmd.Extra.andThen (update (MoveIntoNewRowRequested Nothing (Lens.ValueAt path) l2 p2))

                        Just ( DragFromRun _ path, DropInNewColumn l2 p2 ) ->
                            Cmd.Extra.andThen (update (MoveIntoNewColumnRequested Nothing (Lens.ValueAt path) l2 p2))

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
                    Diff.diff (Value.isEqual (tolerance / 100.0))
                        (Run.getTree WithOverrides runA)
                        (Run.getTree WithOverrides runB)

                diffData =
                    { diff = diff, tolerance = tolerance }
            in
            Just diffData


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
    { isCollapsed : Run.Path -> Bool
    , collapsedToggledMsg : Run.Path -> msg
    , viewLeaf : Run.Path -> String -> leaf -> List (Element msg)
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


viewValueTree :
    RunId
    -> LensId
    -> Run.Path
    -> (RunId -> Run.Path -> Bool)
    -> Lens
    -> Run.Overrides
    -> Maybe ActiveOverrideEditor
    -> Tree Value
    -> Element Msg
viewValueTree runId lensId path checkIsCollapsed lens overrides activeOverrideEditor tree =
    let
        viewLeaf : Run.Path -> String -> Value -> List (Element Msg)
        viewLeaf pathToParent name value =
            case value of
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
                            if Lens.member thisPath lens then
                                dangerousIconButton (size16 FeatherIcons.trash2)
                                    (RemoveFromLensClicked lensId thisPath)

                            else
                                iconButton (size16 FeatherIcons.plus) (AddToLensClicked thisPath)

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
                    , el
                        ([ width fill
                         ]
                            ++ List.map Element.htmlAttribute
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
        }
        path
        tree


buttons : List (Element Msg) -> Element Msg
buttons l =
    row [ Element.spacingXY sizes.medium 0 ] l


viewDiffTree : Explorable.Id -> CollapseStatus -> Tree (Diff.Diff Value) -> Element Msg
viewDiffTree id collapseStatus tree =
    let
        missingElement =
            el (Font.alignRight :: fonts.explorerValues) <|
                text "∅"

        viewLeaf : Run.Path -> String -> Diff.Diff Value -> List (Element Msg)
        viewLeaf pathToParent name leaf =
            -- TODO: Make the diff display something useful in more cases
            case leaf of
                LeftOnly v ->
                    [ el [ width fill ] (text name)
                    , viewValue v
                    , missingElement
                    ]

                Unequal a b ->
                    [ el [ width fill ] (text name)
                    , viewValue a
                    , viewValue b
                    ]

                RightOnly v ->
                    [ el [ width fill ] (text name)
                    , missingElement
                    , viewValue v
                    ]
    in
    viewTree
        { isCollapsed = \p -> isCollapsed id p collapseStatus
        , collapsedToggledMsg = ToggleCollapseTreeClicked id
        , viewLeaf = viewLeaf
        }
        []
        tree


viewComparison : RunId -> RunId -> CollapseStatus -> DiffData -> Element Msg
viewComparison aId bId collapseStatus diffData =
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
                        , el [ Font.bold ] (text (String.fromInt aId ++ " ≈ " ++ String.fromInt bId))
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
            collapseStatus
            diffData.diff
        ]


viewRun : RunId -> LensId -> Lens -> CollapseStatus -> Maybe ActiveOverrideEditor -> Maybe ActiveSearch -> Maybe RunId -> Run -> Element Msg
viewRun runId lensId lens collapseStatus activeOverrideEditor activeSearch selectedForComparison run =
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
                , onPress = Just (ToggleCollapseTreeClicked (Explorable.Run runId) [])
                }
            , buttons
                [ differentIfFilterActive.filterButton
                , selectForComparisonButton
                , iconButton FeatherIcons.edit (DisplayCalculateModalClicked (Just runId) inputs overrides)
                , iconButton FeatherIcons.copy (DisplayCalculateModalClicked Nothing inputs overrides)
                , dangerousIconButton FeatherIcons.trash2 (RemoveExplorableClicked (Explorable.Run runId))
                ]
            ]
        , differentIfFilterActive.filterPatternField
        , viewValueTree
            runId
            lensId
            []
            differentIfFilterActive.isCollapsed
            lens
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
                                (Pivot.getC model.lenses)
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
                                    viewComparison a b model.collapseStatus diffData
                                )
                       )
                )
            )
        ]


viewValueSetAsUserDefinedTable : LensId -> DragDrop -> Lens.TableData -> ValueSet -> Element Msg
viewValueSetAsUserDefinedTable lensId dragDrop td valueSet =
    let
        cells =
            Cells.toList td.grid

        viewCell : Lens.CellContent -> Cells.Pos -> Element Msg
        viewCell cell pos =
            let
                editOnClick editValue =
                    if td.editing /= Nothing then
                        [ Events.onClick
                            (CellOfLensTableEdited lensId pos editValue)
                        ]

                    else
                        []

                dropTarget =
                    List.map Element.htmlAttribute
                        (DragDrop.droppable DragDropMsg (DropOnCell lensId pos cell))

                draggable =
                    List.map Element.htmlAttribute
                        (DragDrop.draggable DragDropMsg (DragFromCell lensId pos cell))

                highlight =
                    case DragDrop.getDropId dragDrop of
                        Nothing ->
                            []

                        Just (DropOnCell li p _) ->
                            if lensId == li && p == pos then
                                [ Border.glow Styling.germanZeroGreen 2 ]

                            else
                                []

                        Just (DropInNewColumn _ _) ->
                            []

                        Just (DropInNewRow _ _) ->
                            []

                cellElement attrs editValue v =
                    el
                        (([ Background.color Styling.emptyCellColor
                          , width fill
                          , padding 2
                          ]
                            ++ fonts.table
                            ++ editOnClick editValue
                            ++ dropTarget
                            ++ highlight
                            ++ draggable
                         )
                            ++ attrs
                        )
                        v
            in
            case cell of
                Lens.Label l ->
                    if td.editing == Just (Lens.Cell pos) then
                        Input.text
                            ([ width fill
                             , Font.bold
                             , padding 2
                             , onEnter (LensTableEditModeChanged lensId (Just Lens.All))
                             ]
                                ++ fonts.table
                            )
                            { onChange = CellOfLensTableEdited lensId pos
                            , text = l
                            , placeholder = Nothing
                            , label = Input.labelHidden "label"
                            }

                    else if l == "" then
                        cellElement [] "" (text " ")

                    else
                        cellElement [ Font.bold ] l (paragraph [] [ text l ])

                Lens.ValueAt p ->
                    let
                        value =
                            case valueSet.runs of
                                [] ->
                                    Nothing

                                r :: _ ->
                                    Dict.get ( r, p ) valueSet.values
                    in
                    if td.editing /= Nothing then
                        cellElement []
                            ""
                            (paragraph [] (List.map text (List.intersperse "." p)))

                    else
                        case value of
                            Nothing ->
                                -- Making the compiler happy
                                cellElement [ Font.alignRight ] "" (text "INTERNAL ERROR")

                            Just (Float f) ->
                                cellElement [ Font.alignRight ] "" (text (formatGermanNumber f))

                            Just Null ->
                                cellElement [ Font.alignRight, Font.bold ] "" (text "null")

                            Just (String s) ->
                                cellElement
                                    [ Font.alignRight
                                    , Font.family [ Font.monospace ]
                                    ]
                                    ""
                                    (text s)

        insertColumnSeparator pos =
            let
                highlight : List (Element.Attribute Msg)
                highlight =
                    case DragDrop.getDropId dragDrop of
                        Nothing ->
                            []

                        Just (DropInNewRow _ _) ->
                            []

                        Just (DropOnCell _ _ _) ->
                            []

                        Just (DropInNewColumn li p) ->
                            if lensId == li && pos == p then
                                [ Border.glow germanZeroGreen 2 ]

                            else
                                []

                droppable =
                    List.map Element.htmlAttribute (DragDrop.droppable DragDropMsg (DropInNewColumn lensId pos))
            in
            el
                ([ width (px sizes.tableGap)
                 , height fill
                 ]
                    ++ highlight
                    ++ droppable
                )
                Element.none

        insertRowSeparator pos =
            let
                highlight =
                    case DragDrop.getDropId dragDrop of
                        Nothing ->
                            []

                        Just (DropInNewRow li p) ->
                            if lensId == li && pos == p then
                                [ Border.glow germanZeroGreen 2 ]

                            else
                                []

                        Just (DropOnCell _ _ _) ->
                            []

                        Just (DropInNewColumn _ _) ->
                            []

                droppable =
                    List.map Element.htmlAttribute (DragDrop.droppable DragDropMsg (DropInNewRow lensId pos))
            in
            el
                ([ height (px sizes.tableGap)
                 , width fill
                 ]
                    ++ highlight
                    ++ droppable
                )
                Element.none

        rows =
            cells
                |> List.indexedMap
                    (\rowNum cellsOfRow ->
                        row
                            [ width fill
                            , spacing 1
                            ]
                            (cellsOfRow
                                |> List.indexedMap
                                    (\columnNum cell ->
                                        let
                                            pos =
                                                { row = rowNum, column = columnNum }
                                        in
                                        [ insertColumnSeparator pos
                                        , column [ width fill ]
                                            [ insertRowSeparator pos
                                            , viewCell cell pos
                                            , if rowNum == Cells.rows td.grid - 1 then
                                                insertRowSeparator { pos | row = pos.row + 1 }

                                              else
                                                Element.none
                                            ]
                                        , if columnNum == Cells.columns td.grid - 1 then
                                            insertColumnSeparator { pos | column = pos.column + 1 }

                                          else
                                            Element.none
                                        ]
                                    )
                                |> List.concat
                            )
                    )
    in
    column
        [ width fill
        , padding sizes.large
        , spacing 1
        ]
        rows


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
                        { header = el [ Font.bold, Font.alignRight ] (Element.text (String.fromInt runId))
                        , width = shrink
                        , view =
                            \path ->
                                let
                                    value =
                                        case Dict.get ( runId, path ) valueSet.values of
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
                    dangerousIconButton (size16 FeatherIcons.trash2) (RemoveFromLensClicked lensId path)
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
                    , onEnter LensLabelEditFinished
                    , Element.htmlAttribute (Html.Attributes.id "interestlabel")
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
                , iconButton
                    (if showGraph then
                        FeatherIcons.eye

                     else
                        FeatherIcons.eyeOff
                    )
                    (ToggleShowGraphClicked id)
                , iconButton FeatherIcons.copy (DuplicateLensClicked id)
                , dangerousIconButton FeatherIcons.trash2 (RemoveLensClicked id)
                ]
            ]
        , column [ width fill, spacing 40 ]
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
            [ viewRunsAndComparisons model
            , el
                [ width (px 2)
                , Background.color black
                , height fill
                ]
                Element.none
            , el
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
        , iconButton
            (size32 FeatherIcons.check)
            (CalculateModalOkClicked maybeNdx inputs overrides)
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
                                    , scrollableText
                                        "This should be done immediately. If it doesn't go away something is probably broken."
                                    )

                                ErrorMessage t m ->
                                    ( t, scrollableText m )
                    in
                    viewModalDialogBox title content
    in
    Element.layout
        [ width fill
        , height fill
        , Element.inFront dialog
        ]
        (viewModel model)
