from typing import Any, Callable, Hashable, Iterator, Optional, Sized

# Type for an individual coordinate value. We only support integer coordinates.
Coord = int

# Type for a single set of coordinates (e.g., (-2, 3, 6)).
Coords = tuple[Coord, ...]

def _nDimRange(
    d: int,
    minValues: list[Coord],
    maxValues: list[Coord],
) -> Iterator[Coords]:
    if d == 0:
        yield ()
        return

    for coords in _nDimRange(d - 1, minValues, maxValues):
        for i in range(minValues[d - 1], maxValues[d - 1] + 1):
            yield coords + (i,)

# Sentinel value to indicate the cell has been marked.
_MARKED = '_MARKED'

class SparseGrid:
    # Dimension of the grid.
    _dimension: int

    # Underlying value storage.
    _map: dict[Coords, Any]

    # Underlying storage for marking cells.
    _marked: dict[Coords, dict[str, bool]]

    # Arrays that store the minimum and maximum coordinate values in each dimension.
    _minCoords: list[Coord]
    _maxCoords: list[Coord]

    def __init__(self, dimension: int = 2) -> None:
        self._dimension = dimension
        self._map = {}
        self._marked = {}
        self._minCoords = []
        self._maxCoords = []

    def setValue(self, coords: Coords, value: Any) -> None:
        self._validateCoords(coords)
        self._updateBoundaryCoords(coords)
        self._map[coords] = value

    def getValue(self, coords: Coords, default: Any = None) -> Any:
        self._validateCoords(coords)
        if self.hasValue(coords):
            return self._map[coords]
        return default

    def hasValue(self, coords: Coords) -> bool:
        self._validateCoords(coords)
        return coords in self._map

    def deleteValue(self, coords: Coords) -> None:
        self._validateCoords(coords)

        if not self.hasValue(coords):
            return
        del self._map[coords]

    def getAdjacentCoords(self, coords: Coords) -> Iterator[Coords]:
        deltas = _nDimRange(
            self._dimension,
            [-1] * self._dimension,
            [1] * self._dimension
        )

        for delta in deltas:
            if all(x == 0 for x in delta):
                # Skip the zero delta.
                continue
            adjCoords: Coords = ()
            # Apply the delta and concatente resulting coordinate in each dimension.
            for d in range(0, self._dimension):
                adjCoords += ((coords[d] + delta[d]),)
            yield adjCoords

    def getAdjacentCoordsInGrid(self, coords: Coords) -> Iterator[Coords]:
        assert len(self._map) > 0, 'Cannot get adjacent coords of empty grid'
        self._assertBoundaryCoords()

        for adjCoords in self.getAdjacentCoords(coords):
            notInGrid = False
            for d in range(self._dimension):
                if adjCoords[d] < self._minCoords[d] or adjCoords[d] > self._maxCoords[d]:
                    notInGrid = True
                    break
            if notInGrid:
                continue
            yield adjCoords

    def getAllCoordsInOrder(
        self,
        minCoords: Optional[list[Coord]] = None,
        maxCoords: Optional[list[Coord]] = None,
    ) -> Iterator[Coords]:
        return _nDimRange(
            self._dimension,
            minCoords if minCoords is not None else self._minCoords,
            maxCoords if maxCoords is not None else self._maxCoords,
        )

    def getAllCoords(self) -> list[Coords]:
        return list(self._map.keys())

    def getMinCoords(self) -> list[Coord]:
        return self._minCoords.copy()

    def getMaxCoords(self) -> list[Coord]:
        return self._maxCoords.copy()

    def addMark(self, coords: Coords, mark: Optional[str] = None) -> None:
        self._validateCoords(coords)
        mark = self._validateMark(mark)

        if coords not in self._marked:
            self._marked[coords] = {}

        self._marked[coords][mark] = True

    def clearMark(self, coords: Coords, mark: Optional[str] = None) -> None:
        self._validateCoords(coords)
        mark = self._validateMark(mark)

        if coords in self._marked and mark in self._marked[coords]:
            del self._marked[coords][mark]

    def clearAllMarks(self) -> None:
        self._marked = {}

    def hasMark(self, coords: Coords, mark: Optional[str] = None) -> bool:
        mark = self._validateMark(mark)

        return coords in self._marked and mark in self._marked[coords]

    def copy(self) -> 'SparseGrid':
        # This doesn't copy marks.
        grid = SparseGrid(self._dimension)
        for c in self.getAllCoords():
            grid.setValue(c, self.getValue(c))
        return grid

    @staticmethod
    def gridFrom2DInput(
        inputLines: list[str],
        elementFn: Optional[Callable[[str], Any]] = None,
    ) -> 'SparseGrid':
        w, h = len(inputLines[0]), len(inputLines)
        grid = SparseGrid(2)
        for y in range(h):
            line = inputLines[y]
            assert len(line) == w, 'grid input is not rectangle'
            for x in range(w):
                v = line[x] if elementFn is None else elementFn(line[x])
                if v is not None:
                    grid.setValue((x, y), v)
        return grid

    def print2D(
        self,
        *,
        minCoords: Optional[list[Coord]] = None,
        maxCoords: Optional[list[Coord]] = None,
        sep: str = '',
        default: Any = None,
        charMap: dict[Hashable, Hashable] = {},
    ) -> None:
        assert self._dimension == 2, 'Cannot print2D with dimension: %d' % self._dimension
        if len(self._map) == 0:
            return

        if not minCoords:
            minCoords = self._minCoords
        if not maxCoords:
            maxCoords = self._maxCoords

        self._validateCoords(minCoords)
        self._validateCoords(maxCoords)

        for j in range(minCoords[1], maxCoords[1] + 1):
            for i in range(minCoords[0], maxCoords[0] + 1):
                v = self.getValue((i, j), default)
                if v in charMap:
                    v = charMap[v]
                print('%s%s' % (v, sep), end='')
            print()
        print()

    def print2DSlices(
        self,
        minCoords: Optional[list[Coord]] = None,
        maxCoords: Optional[list[Coord]] = None,
        sep: str = '',
        default: Any = None,
        charMap: dict[Hashable, Hashable] = {},
    ) -> None:
        assert self._dimension == 3, 'Cannot print2DSlices with dimension: %d' % self._dimension

        if not minCoords:
            minCoords = self._minCoords
        if not maxCoords:
            maxCoords = self._maxCoords

        self._validateCoords(minCoords)
        self._validateCoords(maxCoords)

        for k in range(minCoords[2], maxCoords[2] + 1):
            print('z = %d' % k)
            for j in range(minCoords[1], maxCoords[1] + 1):
                for i in range(minCoords[0], maxCoords[0] + 1):
                    v = self.getValue((i, j, k), default)
                    if v in charMap:
                        v = charMap[v]
                    print('%s%s' % (v, sep), end='')
                print()
            print()
        print()

    def _validateCoords(self, coords: Sized) -> None:
        assert len(coords) == self._dimension, 'Coords have wrong dimension: %s' % str(coords)

    def _assertBoundaryCoords(self) -> None:
        assert len(self._minCoords) > 0 and len(self._maxCoords) > 0, \
            'max and min coords have not been initialized'

    def _updateBoundaryCoords(self, coords: Coords) -> None:
        self._validateCoords(coords)

        if len(self._minCoords) == 0 and len(self._maxCoords) == 0:
            # Initializing boundary conditions.
            self._minCoords = list(coords)
            self._maxCoords = list(coords)
            return

        self._assertBoundaryCoords()
        for d in range(0, len(coords)):
            v = coords[d]
            if v < self._minCoords[d]:
                self._minCoords[d] = v
            if v > self._maxCoords[d]:
                self._maxCoords[d] = v

    def _validateMark(self, mark: Optional[str]) -> str:
        return mark if mark is not None else _MARKED
