module CollapseStatus exposing
    ( CollapseStatus
    , allCollapsed
    , collapse
    , expand
    , isCollapsed
    , toggle
    )

import GeneratorRuns exposing (AbsolutePath)
import Set exposing (Set)


type CollapseStatus
    = CollapseStatus (Set AbsolutePath)


allCollapsed : CollapseStatus
allCollapsed =
    CollapseStatus Set.empty


expand : AbsolutePath -> CollapseStatus -> CollapseStatus
expand ap (CollapseStatus s) =
    CollapseStatus (Set.insert ap s)


collapse : AbsolutePath -> CollapseStatus -> CollapseStatus
collapse ap (CollapseStatus s) =
    CollapseStatus (Set.remove ap s)


isCollapsed : AbsolutePath -> CollapseStatus -> Bool
isCollapsed ap (CollapseStatus s) =
    not (Set.member ap s)


toggle : AbsolutePath -> CollapseStatus -> CollapseStatus
toggle ap s =
    if isCollapsed ap s then
        expand ap s

    else
        collapse ap s
