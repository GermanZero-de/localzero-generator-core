module Glob exposing (match)

{-| Shell like globbing (case insensitive).

Concretely:

  - '\*' matches any nuymber of characters including 0
  - '?' matches a single character

Slow for long patterns or texts (cause the implementation is quadratic), but
for short strings this is likely to be faster than any complex
implementation that prepares a proper parser / statemachine first.

-}


matchHelper : String -> String -> Bool
matchHelper pattern text =
    case ( String.uncons pattern, String.uncons text ) of
        ( Nothing, Nothing ) ->
            True

        ( Nothing, _ ) ->
            False

        ( Just ( '*', "" ), _ ) ->
            -- If everything until a '*' at the end of a pattern
            -- has matched, then we are done, no matter how many
            -- more (if any) characters are left in the text
            True

        ( _, Nothing ) ->
            False

        ( Just ( p, ps ), Just ( t, ts ) ) ->
            case p of
                '?' ->
                    matchHelper ps ts

                '*' ->
                    matchHelper pattern ts || matchHelper ps text

                _ ->
                    p == t && matchHelper ps ts


isSpecial : Char -> Bool
isSpecial c =
    c == '?' || c == '*'


match : String -> String -> Bool
match pattern text =
    let
        lowerPat =
            String.toLower pattern

        lowerText =
            String.toLower text
    in
    if String.contains "?" lowerPat || String.contains "*" lowerPat then
        matchHelper lowerPat lowerText

    else
        lowerPat == lowerText
