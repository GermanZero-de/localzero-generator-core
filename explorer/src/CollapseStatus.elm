module CollapseStatus exposing
    ( CollapseStatus
    , allCollapsed
    , collapse
    , expand
    , expandUntil
    , isCollapsed
    , toggle
    )

import Explorable
import List.Extra
import Run exposing (Path)
import Set exposing (Set)


type CollapseStatus
    = CollapseStatus (Set ( Explorable.Comparable, Path ))


allCollapsed : CollapseStatus
allCollapsed =
    CollapseStatus Set.empty


absolutePath : Explorable.Id -> Path -> ( Explorable.Comparable, Path )
absolutePath i p =
    ( Explorable.toComparable i, p )


expand : Explorable.Id -> Path -> CollapseStatus -> CollapseStatus
expand i p (CollapseStatus s) =
    CollapseStatus (Set.insert (absolutePath i p) s)


expandUntil : Explorable.Id -> Path -> CollapseStatus -> CollapseStatus
expandUntil i p s =
    List.foldl
        (expand i)
        s
        (List.Extra.inits p)


collapse : Explorable.Id -> Path -> CollapseStatus -> CollapseStatus
collapse i p (CollapseStatus s) =
    CollapseStatus (Set.remove (absolutePath i p) s)


isCollapsed : Explorable.Id -> Path -> CollapseStatus -> Bool
isCollapsed i p (CollapseStatus s) =
    not (Set.member (absolutePath i p) s)


toggle : Explorable.Id -> Path -> CollapseStatus -> CollapseStatus
toggle i p s =
    if isCollapsed i p s then
        expand i p s

    else
        collapse i p s
