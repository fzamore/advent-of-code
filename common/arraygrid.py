class ArrayGrid:
    def __init__(self, maxX, maxY):
        self._maxX = maxX
        self._maxY = maxY
        self._grid = [None] * self._maxX * self._maxY
        self._gridLen = self._maxX * self._maxY

    def getMaxX(self):
        return self._maxX

    def getMaxY(self):
        return self._maxY

    def getValue(self, x, y, default=None):
        i = self._gridIndex(x, y)
        if i < 0 or i >= self._gridLen:
            if default:
                return default
            assert False, 'Invalid grid coordinates: (%d, %d)' % (x, y)
        return self._grid[i]

    def setValue(self, x, y, value):
        i = self._gridIndex(x, y)
        assert i >= 0 and i < self._gridLen, 'Invalid grid coordinates: (%d, %d)' % (x, y)
        self._grid[i] = value

    def print2D(self, charMap={}):
        print()
        for y in range(0, self._maxY):
            for x in range(0, self._maxX):
                v = self.getValue(x, y)
                if v in charMap:
                    v = charMap[v]
                print(v, end='')
            print()
        print()

    def _gridIndex(self, x, y):
        return y * self._maxX + x
