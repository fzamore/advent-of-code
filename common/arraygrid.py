from typing import Any, Hashable

class ArrayGrid:
    def __init__(self, width: int, height: int) -> None:
        self._width = width
        self._height = height
        self._grid = [None] * self._width * self._height
        self._gridLen = self._width * self._height

    def getWidth(self) -> int:
        return self._width

    def getHeight(self) -> int:
        return self._height

    def hasValue(self, x: int, y: int) -> bool:
        return self.getValue(x, y) is not None

    def getValue(self, x: int, y: int, default: Any = None) -> Any:
        i = self._gridIndex(x, y)
        if i < 0 or i >= self._gridLen:
            if default:
                return default
            assert False, 'Invalid grid coordinates: (%d, %d)' % (x, y)
        return self._grid[i]

    def setValue(self, x: int, y: int, value: Any) -> None:
        i = self._gridIndex(x, y)
        assert i >= 0 and i < self._gridLen, 'Invalid grid coordinates: (%d, %d)' % (x, y)
        self._grid[i] = value

    def areCoordsWithinBounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.getWidth() and 0 <= y < self.getHeight()

    def copy(self) -> 'ArrayGrid':
        grid = ArrayGrid(self._width, self._height)
        for y in range(self._height):
            for x in range(self._width):
                grid.setValue(x, y, self.getValue(x, y))
        return grid

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self._grid == other._grid

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(tuple(self._grid))

    def print2D(self, charMap: dict[Hashable, Hashable] = {}) -> None:
        print()
        for y in range(0, self._height):
            for x in range(0, self._width):
                v = self.getValue(x, y)
                if v in charMap:
                    v = charMap[v]
                print(v, end='')
            print()
        print()

    def _gridIndex(self, x: int, y: int) -> int:
        return y * self._width + x
