def _index(coords):
    return ','.join([str(x) for x in coords])

def _nDimRange(d, minValues, maxValues):
    if d == 0:
        yield ()
        return

    for coords in _nDimRange(d - 1, minValues, maxValues):
        for i in range(minValues[d - 1], maxValues[d - 1] + 1):
            yield coords + (i,)

class SparseGrid:
    _MARKED = '_MARKED'

    def __init__(self, dimension=2):
        # Dimension of the grid
        self._dimension = dimension

        # Underlying value storage
        self._map = {}

        # Underlying storage for marking cells
        self._marked = {}

        # Arrays that store the minimum and maximum coordinate values in each dimension.
        self._minCoords = [None] * dimension
        self._maxCoords = [None] * dimension

    def setValue(self, coords, value):
        self._validateCoords(coords)
        self._updateBoundaryCoords(coords)
        self._map[_index(coords)] = value

    def getValue(self, coords, default=None):
        self._validateCoords(coords)
        if self.hasValue(coords):
            return self._map[_index(coords)]
        return default

    def hasValue(self, coords):
        self._validateCoords(coords)
        return _index(coords) in self._map

    def deleteValue(self, coords):
        self._validateCoords(coords)

        if not self.hasValue(coords):
            return
        del self._map[_index(coords)]

    def getAdjacentCoords(self, coords):
        deltas = _nDimRange(
            self._dimension,
            [-1] * self._dimension,
            [1] * self._dimension
        )

        for delta in deltas:
            if all(x == 0 for x in delta):
                # Skip the zero delta.
                continue
            adjCoords = ()
            # Apply the delta and concatente resulting coordinate in each dimension.
            for d in range(0, self._dimension):
                adjCoords += ((coords[d] + delta[d]),)
            yield adjCoords

    def getAdjacentCoordsInGrid(self, coords):
        for adjCoords in self.getAdjacentCoords(coords):
            notInGrid = False
            for d in range(self._dimension):
                if adjCoords[d] < self._minCoords[d] or adjCoords[d] > self._maxCoords[d]:
                    notInGrid = True
                    break
            if notInGrid:
                continue
            yield adjCoords

    def getAllCoords(self):
        return _nDimRange(self._dimension, self._minCoords, self._maxCoords)

    def getMinCoords(self):
        return self._minCoords

    def getMaxCoords(self):
        return self._maxCoords

    def addMark(self, coords, mark=None):
        self._validateCoords(coords)
        mark = self._validateMark(mark)

        index = _index(coords)
        if index not in self._marked:
            self._marked[index] = {}

        self._marked[_index(coords)][mark] = True

    def clearMark(self, coords, mark=None):
        self._validateCoords(coords)
        mark = self._validateMark(mark)

        index = _index(coords)
        if index in self._marked and mark in self._marked[index]:
            del self._marked[index][mark]

    def clearAllMarks(self):
        self._marked = {}

    def hasMark(self, coords, mark=None):
        mark = self._validateMark(mark)

        index = _index(coords)
        return index in self._marked and mark in self._marked[index]

    def print2D(self, minCoords=None, maxCoords=None, sep='', default=None):
        assert self._dimension == 2, 'Cannot print2D with dimension: %d' % self._dimension

        if not minCoords:
            minCoords = self._minCoords
        if not maxCoords:
            maxCoords = self._maxCoords

        self._validateCoords(minCoords)
        self._validateCoords(maxCoords)

        for j in range(minCoords[1], maxCoords[1] + 1):
            for i in range(minCoords[0], maxCoords[0] + 1):
                print('%s%s' % (self.getValue((i, j), default), sep), end='')
            print()
        print()

    def print2DSlices(self, minCoords=None, maxCoords=None, sep='', default=None):
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
                    print('%s%s' % (self.getValue((i, j, k), default), sep), end='')
                print()
            print()
        print()

    def _validateCoords(self, coords):
        assert len(coords) == self._dimension, 'Coords have wrong dimension: %s' % str(coords)

    def _updateBoundaryCoords(self, coords):
        self._validateCoords(coords)
        for d in range(0, len(coords)):
            v = coords[d]
            if self._minCoords[d] == None or v < self._minCoords[d]:
                self._minCoords[d] = v
            if self._maxCoords[d] == None or v > self._maxCoords[d]:
                self._maxCoords[d] = v

    def _validateMark(self, mark):
        return mark if mark != None else self._MARKED
