from common.sparsegrid import SparseGrid

def getBitValue(image, x, y, minCoords, maxCoords, sparsebit):
    if image.hasValue((x, y)):
        return 1

    # if coords are outside grid bounds, return the sparsebit
    if x < minCoords[0] or y < minCoords[1] or x > maxCoords[0] or y > maxCoords[1]:
        return sparsebit

    return 0

def getPixelNumber(image, x, y, minCoords, maxCoords, sparsebit):
    bits = [
        getBitValue(image, x - 1, y - 1, minCoords, maxCoords, sparsebit),
        getBitValue(image, x + 0, y - 1, minCoords, maxCoords, sparsebit),
        getBitValue(image, x + 1, y - 1, minCoords, maxCoords, sparsebit),
        getBitValue(image, x - 1, y + 0, minCoords, maxCoords, sparsebit),
        getBitValue(image, x + 0, y + 0, minCoords, maxCoords, sparsebit),
        getBitValue(image, x + 1, y + 0, minCoords, maxCoords, sparsebit),
        getBitValue(image, x - 1, y + 1, minCoords, maxCoords, sparsebit),
        getBitValue(image, x + 0, y + 1, minCoords, maxCoords, sparsebit),
        getBitValue(image, x + 1, y + 1, minCoords, maxCoords, sparsebit),
    ]
    bitstring = ''.join([str(x) for x in bits])
    return int(bitstring, 2)

def enhance(algo, image, minCoords, maxCoords, sparsebit):
    newImage = SparseGrid(2)
    for y in range(minCoords[1] - 1, maxCoords[1] + 2):
        for x in range(minCoords[0] - 1, maxCoords[0] + 2):
            pixelNumber = getPixelNumber(image, x, y, minCoords, maxCoords, sparsebit)
            assert pixelNumber >= 0, 'pixel number negative: %d' % pixelNumber
            assert pixelNumber < 512, 'pixel number too high: %d' % pixelNumber
            algoValue = algo[pixelNumber]
            assert algoValue == '#' or algoValue == '.', 'invalid algo value: %s' % algoValue
            if algoValue == '#':
                newImage.setValue((x, y), 1)
    return newImage

def updateSparsebit(algo, sparsebit):
    i = None
    match sparsebit:
      case 0:
        i = 0
      case 1:
        # all 1's in the bitstring means the last algo position
        i = -1
      case _:
        assert False, 'bad sparsebit: %s' % sparsebit

    match algo[i]:
      case '.':
        return 0
      case '#':
        return 1
      case _:
        assert False, 'bad algo index %d' % i

def printImage(image, minCoords, maxCoords):
    image.print2D(minCoords, maxCoords, default='.')

def part1():
    algo = None
    image = SparseGrid(2)
    minCoords = (0, 0)
    maxCoords = None
    with open('day20.txt') as f:
        algo = f.readline().strip()
        f.readline()
        lines = f.read().splitlines()
        y = 0
        for line in lines:
            if maxCoords == None:
                maxCoords = (len(line) - 1, len(lines) - 1)
            x = 0
            for c in line:
                if c == '#':
                    image.setValue((x, y), 1)
                x += 1
            y += 1

    print(algo)
    print(len(algo))
    print()
    #printImage(image, minCoords, maxCoords)

    # sparse grid points start off as zeroes
    sparsebit = 0

    n = 2
    for i in range(n):
        print('step', i)
        print(sparsebit, minCoords, maxCoords)
        image = enhance(algo, image, minCoords, maxCoords, sparsebit)
        sparsebit = updateSparsebit(algo, sparsebit)
        minCoords = (minCoords[0] - 1, minCoords[1] - 1)
        maxCoords = (maxCoords[0] + 1, maxCoords[1] + 1)
        print()
        #printImage(image, minCoords, maxCoords)

    print(sparsebit, minCoords, maxCoords)
    print(len(image.getAllCoords()))

def part2():
    algo = None
    image = SparseGrid(2)
    minCoords = (0, 0)
    maxCoords = None
    with open('day20.txt') as f:
        algo = f.readline().strip()
        f.readline()
        lines = f.read().splitlines()
        y = 0
        for line in lines:
            if maxCoords == None:
                maxCoords = (len(line) - 1, len(lines) - 1)
            x = 0
            for c in line:
                if c == '#':
                    image.setValue((x, y), 1)
                x += 1
            y += 1

    print(algo)
    print(len(algo))
    print()

    # sparse grid points start off as zeroes
    sparsebit = 0

    n = 50
    for i in range(n):
        print('step', i)
        print(sparsebit, minCoords, maxCoords)
        image = enhance(algo, image, minCoords, maxCoords, sparsebit)
        sparsebit = updateSparsebit(algo, sparsebit)
        minCoords = (minCoords[0] - 1, minCoords[1] - 1)
        maxCoords = (maxCoords[0] + 1, maxCoords[1] + 1)
        print()

    print(sparsebit, minCoords, maxCoords)
    print(len(image.getAllCoords()))

part2()
