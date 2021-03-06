port module Html5.DragDrop exposing
    ( Model, init, Msg, update, updateSticky
    , draggable, droppable
    , getDragId, getDropId
    , getDragstartEvent, fixFirefoxDragStartCmd
    )

{-| This library handles dragging and dropping using the API
from the HTML 5 recommendation at
<https://www.w3.org/TR/html/editing.html#drag-and-drop>.

It provides attributes and a model/update to handle
dragging and dropping between your elements.

Types are parametrized with a `dragId` and a `dropId` parameter, which are the
types for the drag identifier passed to the [`draggable`](#draggable) function
and the drop identifier passed to the [`droppable`](#droppable) function.
You can put whatever data you like in these, but don't use function types.

You can use several instances of this model at the same time and they won't
interfere with each other. Drag and drop are connected to an instance by the
Msg constructor used, and the update function will not send a result if a drop
was made from another instance.

To use on mobile, you can include the following polyfill:
<https://github.com/Bernardo-Castilho/dragdroptouch>

Note that drag and drop _does not_ work out of the box in Firefox.
See the example folder in github for an example that uses ports
to do `event.dataTransfer.setData('text', '')`. to fix this.


# Model and update

@docs Model, init, Msg, Position, update, updateSticky


# View attributes

@docs draggable, droppable


# Status functions

@docs getDragId, getDropId, getDroppablePosition


# Javascript interop

@docs getDragstartEvent, fixFirefoxDragStartCmd

-}

import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Json.Decode as Json
import Json.Encode exposing (Value)


port dragstart : Value -> Cmd msg


{-| The drag and drop state.

This should be placed inside your application's model like this:

    type alias Model =
        { ...
        , dragDrop : Html5.DragDrop.Model DragId DropId
        }

-}
type Model dragId dropId
    = NotDragging
    | Dragging dragId
    | DraggedOver dragId dropId


{-| The initial drag and drop state.

You should use this as the initital value for the drag and drop state in your model.

-}
init : Model dragId dropId
init =
    NotDragging


{-| The drag and drop messages.

This should be placed inside your application's messages like this:

    type Msg
        = ...
        | DragDropMsg (Html5.DragDrop.Msg DragId DropId)

-}
type Msg dragId dropId
    = DragStart dragId Json.Value
    | DragEnd
    | DragEnter dropId
    | DragLeave dropId
    | DragOver dropId
    | Drop dropId


{-| The update function.

When a successful drag and drop is made, this function will return a result
consisting of the `dragId` and `dropId` that was specified in the
[`draggable`](#draggable) and [`droppable`](#droppable)
calls for the corresponding nodes. It will also return a [`Position`](#Position)
for the drop event.

This should be placed inside your application's update function, like this:

    update msg model =
        case msg of
            ...
            DragDropMsg msg_ ->
                let
                    ( model_, result ) =
                        Html5.DragDrop.update msg_ model.dragDrop
                in
                    { model
                        | dragDrop = model_
                        , ...use result if available...
                    }

-}
update : Msg dragId dropId -> Model dragId dropId -> ( Model dragId dropId, Maybe ( dragId, dropId ) )
update =
    updateCommon False


{-| A "sticky" version of the [`update`](#update) function.

It's used the same way as the [`update`](#update) function, but when you use this version,
droppables are "sticky" so when you drag out of them and release the mouse button,
a drop will still be registered at the last droppable. You should preferably
provide some sort of indication (using [`getDropId`](#getDropId)) where the drop will take
place if you use this function.

-}
updateSticky : Msg dragId dropId -> Model dragId dropId -> ( Model dragId dropId, Maybe ( dragId, dropId ) )
updateSticky =
    updateCommon True


updateCommon :
    Bool
    -> Msg dragId dropId
    -> Model dragId dropId
    -> ( Model dragId dropId, Maybe ( dragId, dropId ) )
updateCommon sticky msg model =
    case ( msg, model, sticky ) of
        ( DragStart dragId _, _, _ ) ->
            ( Dragging dragId, Nothing )

        ( DragEnd, _, _ ) ->
            ( NotDragging, Nothing )

        ( DragEnter dropId, Dragging dragId, _ ) ->
            ( DraggedOver dragId dropId, Nothing )

        ( DragEnter dropId, DraggedOver dragId _, _ ) ->
            ( DraggedOver dragId dropId, Nothing )

        -- Only handle DragLeave if it is for the current dropId.
        -- DragLeave and DragEnter sometimes come in the wrong order
        -- when two droppables are next to each other.
        ( DragLeave dropId_, DraggedOver dragId dropId, False ) ->
            if dropId_ == dropId then
                ( Dragging dragId, Nothing )

            else
                ( model, Nothing )

        --sticky, so don't do a dragleave!
        ( DragLeave _, DraggedOver _ _, True ) ->
            ( model, Nothing )

        ( DragOver dropId, Dragging dragId, _ ) ->
            ( DraggedOver dragId dropId, Nothing )

        ( DragOver dropId, DraggedOver dragId currentDropId, _ ) ->
            if model == DraggedOver dragId dropId then
                ( model, Nothing )

            else
                -- Update coordinates
                ( DraggedOver dragId dropId, Nothing )

        ( Drop dropId, Dragging dragId, _ ) ->
            ( NotDragging, Just ( dragId, dropId ) )

        ( Drop dropId, DraggedOver dragId _, _ ) ->
            ( NotDragging, Just ( dragId, dropId ) )

        --
        -- impossible
        --
        ( DragEnter _, NotDragging, _ ) ->
            ( model, Nothing )

        ( DragLeave _, NotDragging, _ ) ->
            ( model, Nothing )

        ( DragLeave _, Dragging _, _ ) ->
            ( model, Nothing )

        ( DragOver _, NotDragging, _ ) ->
            ( model, Nothing )

        ( Drop _, NotDragging, _ ) ->
            ( model, Nothing )


{-| Attributes to make a node draggable.

The node you put these attributes on will be draggable with the `dragId` you provide.
It should be used like this:

    view =
       ...
       div (... ++ Html5.DragDrop.draggable DragDropMsg dragId) [...]

-}
draggable : (Msg dragId dropId -> msg) -> dragId -> List (Attribute msg)
draggable wrap drag =
    [ attribute "draggable" "true"
    , onWithOptions "dragstart" { stopPropagation = True, preventDefault = False } <| Json.map (wrap << DragStart drag) Json.value
    , onWithOptions "dragend" { stopPropagation = True, preventDefault = False } <| Json.succeed <| wrap <| DragEnd
    ]


{-| Attributes to make a node droppable.

The node you put these attributes on will be droppable with the `dropId` you provide.
It should be used like this:

    view =
       ...
       div (... ++ Html5.DragDrop.droppable DragDropMsg dropId) [...]

-}
droppable : (Msg dragId dropId -> msg) -> dropId -> List (Attribute msg)
droppable wrap dropId =
    [ onWithOptions "dragenter" { stopPropagation = True, preventDefault = True } <| Json.succeed <| wrap <| DragEnter dropId
    , onWithOptions "dragleave" { stopPropagation = True, preventDefault = True } <| Json.succeed <| wrap <| DragLeave dropId

    -- We don't stop propagation for dragover events because this will trigger redraw,
    -- and we get a lot of dragover events.
    , onWithOptions "dragover" { stopPropagation = False, preventDefault = True } <| Json.succeed <| wrap (DragOver dropId)
    , onWithOptions "drop" { stopPropagation = True, preventDefault = True } <| Json.succeed <| wrap (Drop dropId)
    ]


{-| Get the current `dragId` if available.

This function can be used for instance to hide the draggable when dragging.

-}
getDragId : Model dragId dropId -> Maybe dragId
getDragId model =
    case model of
        NotDragging ->
            Nothing

        Dragging dragId ->
            Just dragId

        DraggedOver dragId dropId ->
            Just dragId


{-| Get the current `dropId` if available.

This function can be used for instance to highlight the droppable when dragging over it.

Note that for efficiency reasons, the `dragover` event is being propagated,
so if you have a droppable inside another droppable you could get the wrong info
from `getDropId`. The package tries to ignore the extra events, but it may fail.

-}
getDropId : Model dragId dropId -> Maybe dropId
getDropId model =
    case model of
        NotDragging ->
            Nothing

        Dragging dragId ->
            Nothing

        DraggedOver dragId dropId ->
            Just dropId


{-| Get the `dragstart` event `Value` so that you can pass it to a port.
This is useful to fix Firefox behaviour. See the example directory in github
for how you can do that.

You can also use the event to do other things from Javascript,
such as setting the drag image.

-}
getDragstartEvent : Msg dragId dropId -> Maybe { dragId : dragId, event : Json.Value }
getDragstartEvent msg =
    case msg of
        DragStart dragId event ->
            Just { dragId = dragId, event = event }

        _ ->
            Nothing


fixFirefoxDragStartCmd : Msg dragId dropId -> Cmd msg
fixFirefoxDragStartCmd msg =
    getDragstartEvent msg
        |> Maybe.map (.event >> dragstart)
        |> Maybe.withDefault Cmd.none


{-| polyfill for onWithOptions
-}
onWithOptions :
    String
    ->
        { stopPropagation : Bool
        , preventDefault : Bool
        }
    -> Json.Decoder msg
    -> Attribute msg
onWithOptions name { stopPropagation, preventDefault } decoder =
    decoder
        |> Json.map (\msg -> { message = msg, stopPropagation = stopPropagation, preventDefault = preventDefault })
        |> custom name
