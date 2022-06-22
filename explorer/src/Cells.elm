module Cells exposing
    ( Cells
    , Pos
    , addColumn
    , addRow
    , columns
    , decoder
    , encode
    , foldRowMajor
    , get
    , initialize
    , map
    , repeat
    , rows
    , set
    , toList
    )

import Array exposing (Array)
import Json.Decode as Decode
import Json.Encode as Encode
import List.Extra


{-| A two dimensional grid. Any new rows are filled with empty,
and empty is returned when get is called with an index out of bounds
-}
type Cells a
    = Cells
        { empty : a
        , rows : Int
        , columns : Int
        , values : Array a
        }


type alias Pos =
    { row : Int, column : Int }


emptyValue : Cells a -> a
emptyValue (Cells c) =
    c.empty


columns : Cells a -> Int
columns (Cells c) =
    c.columns


rows : Cells a -> Int
rows (Cells c) =
    c.rows


repeat : a -> Int -> Int -> Cells a
repeat empty rowNum columnNum =
    Cells
        { empty = empty
        , rows = rowNum
        , columns = columnNum
        , values = Array.repeat (rowNum * columnNum) empty
        }


map : (a -> a) -> Cells a -> Cells a
map fn (Cells c) =
    Cells
        { empty = c.empty
        , rows = c.rows
        , columns = c.columns
        , values = Array.map fn c.values
        }


get : Pos -> Cells a -> a
get pos (Cells c) =
    let
        startOfRow =
            c.columns * pos.row
    in
    Array.get (startOfRow + pos.column) c.values
        |> Maybe.withDefault c.empty


set : Pos -> a -> Cells a -> Cells a
set pos val (Cells c) =
    let
        startOfRow =
            c.columns * pos.row
    in
    Cells { c | values = Array.set (startOfRow + pos.column) val c.values }


initialize : a -> Int -> Int -> (Pos -> a) -> Cells a
initialize empty rowsNum columnsNum fn =
    Cells
        { empty = empty
        , rows = rowsNum
        , columns = columnsNum
        , values =
            Array.initialize (rowsNum * columnsNum)
                (\off ->
                    let
                        row =
                            off // columnsNum

                        column =
                            off
                                |> remainderBy columnsNum
                    in
                    fn { row = row, column = column }
                )
        }


foldRowMajor : (Pos -> a -> acc -> acc) -> acc -> Cells a -> acc
foldRowMajor fn init cs =
    let
        helper : acc -> Pos -> acc
        helper acc pos =
            if pos.row >= rows cs then
                acc

            else if pos.column >= columns cs then
                helper acc { row = pos.row + 1, column = 0 }

            else
                helper (fn pos (get pos cs) acc) { pos | column = pos.column + 1 }
    in
    helper init { row = 0, column = 0 }


addRow : Int -> Cells a -> Cells a
addRow rowNum cs =
    initialize
        (emptyValue cs)
        (rows cs + 1)
        (columns cs)
        (\p ->
            if p.row < rowNum then
                get p cs

            else if p.row == rowNum then
                emptyValue cs

            else
                get { p | row = p.row - 1 } cs
        )


addColumn : Int -> Cells a -> Cells a
addColumn columnNum cs =
    initialize
        (emptyValue cs)
        (rows cs)
        (columns cs + 1)
        (\p ->
            if p.column < columnNum then
                get p cs

            else if p.column == columnNum then
                emptyValue cs

            else
                get { p | column = p.column - 1 } cs
        )


decoder : a -> Decode.Decoder a -> Decode.Decoder (Cells a)
decoder empty cellDecoder =
    Decode.list (Decode.list cellDecoder)
        |> Decode.andThen
            (\listOfRows ->
                case listOfRows of
                    [] ->
                        Decode.succeed (repeat empty 0 0)

                    r1 :: rRest ->
                        let
                            numColumns =
                                List.length r1

                            numRows =
                                List.length rRest + 1
                        in
                        if List.all (\l -> List.length l == numColumns) rRest then
                            Decode.succeed
                                (Cells
                                    { empty = empty
                                    , rows = numRows
                                    , columns = numColumns
                                    , values =
                                        Array.fromList
                                            (List.concat listOfRows)
                                    }
                                )

                        else
                            Decode.fail "Irregular shaped cells"
            )


toListOfArrays : Cells a -> List (Array a)
toListOfArrays (Cells c) =
    List.Extra.initialize c.rows
        (\row ->
            let
                start =
                    row * c.columns
            in
            Array.slice start (start + c.columns) c.values
        )


toList : Cells a -> List (List a)
toList cs =
    toListOfArrays cs
        |> List.map Array.toList


encode : (a -> Encode.Value) -> Cells a -> Encode.Value
encode encodeCell cs =
    toListOfArrays cs
        |> Encode.list (Encode.array encodeCell)
