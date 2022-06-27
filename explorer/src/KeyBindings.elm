module KeyBindings exposing
    ( KeyBinding, bind, on
    , Modifiers, noModifiers, shift, ctrl
    , keyToString
    )

{-| This module provides helpers to define keybindings

@docs KeyBinding, bind, on

@docs Modifiers, noModifiers, shift, ctrl

@docs keyToString

-}

import Element
import Html.Events
import Keyboard.Event exposing (considerKeyboardEvent)
import Keyboard.Key as K
import List.Extra


type alias KeyBinding msg =
    { modifiers : Modifiers
    , key : K.Key
    , msg : msg
    , doc : String
    }


type alias Modifiers =
    { alt : Bool, ctrl : Bool, cmd : Bool, shift : Bool }


noModifiers : Modifiers
noModifiers =
    { alt = False, ctrl = False, cmd = False, shift = False }


shift : Modifiers
shift =
    { noModifiers | shift = True }


ctrl : Modifiers
ctrl =
    { noModifiers | ctrl = True }


bind : Modifiers -> K.Key -> msg -> String -> KeyBinding msg
bind modifiers key msg doc =
    { modifiers = modifiers
    , key = key
    , msg = msg
    , doc = doc
    }


keyToString : Modifiers -> K.Key -> String
keyToString mods key =
    let
        lowercaseLetter =
            case key of
                K.Unknown 220 ->
                    Just '|'

                K.Unknown 191 ->
                    Just '/'

                _ ->
                    K.toChar key
                        |> Maybe.map
                            Char.toLower

        ( addShiftStr, keyString ) =
            case ( mods.shift, lowercaseLetter ) of
                ( False, Just c ) ->
                    ( False, String.fromChar c )

                ( True, Just c ) ->
                    ( False, String.fromChar (Char.toUpper c) )

                ( b, Nothing ) ->
                    ( b
                    , case key of
                        K.Tab ->
                            "Tab"

                        K.Enter ->
                            "Enter"

                        _ ->
                            "??"
                    )

        addMod b modStr acc =
            if b then
                acc ++ modStr ++ " + "

            else
                acc
    in
    (""
        |> addMod mods.ctrl "CTRL"
        |> addMod mods.alt "ALT"
        |> addMod mods.cmd "CMD"
        |> addMod addShiftStr "SHIFT"
    )
        ++ " "
        ++ keyString


matchesModifiers : Keyboard.Event.KeyboardEvent -> Modifiers -> Bool
matchesModifiers ev mods =
    (ev.altKey
        == mods.alt
    )
        && ev.ctrlKey
        == mods.ctrl
        && ev.metaKey
        == mods.cmd
        && ev.shiftKey
        == mods.shift


on : List (KeyBinding msg) -> Element.Attribute msg
on keys =
    Element.htmlAttribute
        (Html.Events.preventDefaultOn "keydown"
            (considerKeyboardEvent
                (\ev ->
                    keys
                        |> List.Extra.findMap
                            (\kb ->
                                if ev.keyCode == kb.key && matchesModifiers ev kb.modifiers then
                                    Just ( kb.msg, True )

                                else
                                    Nothing
                            )
                )
            )
        )
