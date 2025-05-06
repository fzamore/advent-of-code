from common.sparsegrid import SparseGrid, Coords
from itertools import combinations

input = open('day22.txt').read().splitlines()[2:]

def parseSizeSpec(s: str) -> int:
	assert s[-1] == 'T', 'bad size spec'
	return int(s[:-1])

def parseLine(grid: SparseGrid, line: str) -> None:
	v = line.split()
	d = [parseSizeSpec(v[i]) for i in [1, 2, 3]]
	size, used, avail = d
	assert size - used == avail, 'bad line'

	_, xs, ys = v[0].split('/')[-1].split('-')
	assert xs[0] == 'x', 'bad x'
	assert ys[0] == 'y', 'bad y'

	x, y = int(xs[1:]), int(ys[1:])
	grid.setValue((x, y), (size, used))

def parseInput() -> SparseGrid:
	grid = SparseGrid(2)
	for line in input:
		parseLine(grid, line)
	return grid

def isViablePair(grid: SparseGrid, c1: Coords, c2: Coords) -> bool:
	assert c1 != c2, 'coords cannot be same'
	_, u1 = grid.getValue(c1)
	s2, u2 = grid.getValue(c2)
	return 0 < u1 <= s2 - u2

def moveData(grid: SparseGrid, src: Coords, dst: Coords) -> None:
	ssize, sused = grid.getValue(src)
	dsize, dused = grid.getValue(dst)

	assert dsize >= sused + dused, 'cannot move data'

	grid.setValue(src, (ssize, 0))
	grid.setValue(dst, (dsize, sused + dused))

def part1() -> None:
	print('nodes:', len(input))

	grid = parseInput()

	ans = 0
	for c1, c2 in combinations(grid.getAllCoords(), 2):
		if isViablePair(grid, c1, c2):
			ans += 1
		if isViablePair(grid, c2, c1):
			ans += 1
	print(ans)

def part2() -> None:
	print()
	print('nodes:', len(input))

	grid = parseInput()
	print('max coords:', grid.getMaxCoords())

	maxX, _ = grid.getMaxCoords()

	for n in grid.getAllCoords():
		if grid.getValue(n)[1] == 0:
			zero = n
	assert zero is not None, 'did not find zero node'

	print('zero node:', zero)

	# todo: add comment saying this solution is based on a horizontal wall
	# thats anchored to the right of the grod above the zero node

  # This solution is based on the grid containing a horizontall "wall" of
  # nodes that cannot move their data (because they have too much). The
  # wall is anchored to the right of the grid, so the zero node must move
  # up and left around the wall.

	steps = 0
	x, y = zero

	# Moves the zero node.
	def mz(dx, dy):
		nonlocal x, y, steps
		# moving the zero node is represented backward, since we're moving data into the zero node
		src = x + dx, y + dy
		dst = x, y
		assert isViablePair(grid, src, dst), 'cannot move zero node'
		moveData(grid, src, dst)
		steps += 1
		x += dx
		y += dy

	# First, try to move the zero node up to the top, and if we encounter a
	# wall, move it left around the wall.
	while y > 0:
		while not isViablePair(grid, (x, y - 1), (x, y)):
			# Move left around the wall.
			mz(-1, 0)

		# Move up.
		mz(0, -1)

	print('first row:', x, y, steps)

	# Next, move the zero node to the right until it's at the right edge.
	while x < maxX:
		mz(1, 0)

	print('at target:', x, y, steps)

	# Now, the zero node has to move in a series of U-shaped patterns to the
	# left untip we reach the source.
	while (x, y) != (1, 0):
		mz(0, 1)
		mz(-1, 0)
		mz(-1, 0)
		mz(0, -1)

		# After we finish the U, we need to move the zero node right again (to
		# re-position for the next U).
		mz(1, 0)

	print('done:', x, y, steps)
	print(steps)

part2()
