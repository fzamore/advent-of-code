from collections import defaultdict
from common.sparsegrid import SparseGrid

input = open('day18.txt').read().splitlines()

def part1() -> None:
  deltas = {
    'U': (0, -1),
    'D': (0, 1),
    'L': (-1, 0),
    'R': (1, 0),
  }

  grid = SparseGrid(2)
  cx, cy = 0, 0
  grid.setValue((cx, cy), '#')
  for line in input:
    values = line.split()
    dir = values[0]
    qty = int(values[1])
    dx, dy = deltas[dir]

    for _ in range(qty):
      cx += dx
      cy += dy
      grid.setValue((cx, cy), '#')

  grid.print2D(default='.')

  # Count interior spaces by shooting a ray across each row and flip
  # in/out when you hit a vertical wall.
  count = 0
  (mnx, mny), (mxx, mxy) = grid.getMinCoords(), grid.getMaxCoords()
  for y in range(mny, mxy):
    # Examine row between y and y + 1
    on = False
    for x in range(mnx - 1, mxx + 1):
      if grid.hasValue((x, y)) and grid.hasValue((x, y + 1)):
        # If we're crossing a vertical wall (indicated by existing values
        # in both rows of the grid), flip.
        on = not on
      if on and not grid.hasValue((x, y)):
        # We're inside the grid.
        count += 1
  print('count inside:', count)
  print('count on border:', len(grid.getAllCoords()))
  print(count + len(grid.getAllCoords()))

def part2() -> None:
  deltas = [(1, 0), (0, 1), (-1, 0), (0, -1)]

  borderCount = 0
  verticalLines: list[tuple[int, int, int]] = []
  horizLines = defaultdict(list)
  x, y = 0, 0
  minY, maxY = 0, 0
  for line in input:
    values = line.split()

    dx, dy = deltas[int(values[2][-2])]
    qty = int(values[2][2:-2], 16)

    nx = x + qty * dx
    ny = y + qty * dy

    if dx == 0:
      # List of vertical lines.
      verticalLines.append((x, min(y, ny), max(y, ny)))
    else:
      # Dict of lists of horizontal lines keyed by y-coordinate.
      horizLines[y].append((y, min(x, nx), max(x, nx)))

    # Count the border spaces by just walking the border.
    borderCount += qty

    x = nx
    y = ny
    minY, maxY = min(y, minY), max(y, maxY)

  print()
  assert x == 0 and y == 0, 'bad walking the border'
  print(minY, maxY)

  # Sort vertical lines by x coordinate, breaking ties by smaller y
  # coordinate.
  verticalLines = sorted(verticalLines, key=lambda x: (x[0], x[1]))

  for y in horizLines:
    # Sort the horizontal lines in each row by smaller x coordinate.
    horizLines[y] = sorted(horizLines[y], key=lambda x: x[1])

  print('number of rows to process:', maxY - minY)

  insideCount = 0
  # Iterating through all rows one by one is very slow.
  for y in range(minY, maxY):
    # Move from left to right across each row.

    # Determine whether we're inside the shape.
    inside = False

    # Vertical line that caused us to enter the shape.
    entryVerticalLine = None

    # Iterate through vertical lines from left to right.
    for verticalLine in verticalLines:
      x, y1, y2 = verticalLine

      if y1 < y + 0.5 < y2:
        # We use an "epsilon" trick to determine whether a ray intersects
        # a vertical line between rows y and y + 1 (since everything is
        # aligned on an integer grid). This allows is to ignore horizontal
        # lines when determining entry/exit points.
        inside = not inside
        if inside:
          # We've entered the shape. Store the vertical line we crossed to enter.
          entryVerticalLine = verticalLine

      if not inside and entryVerticalLine is not None:
        # We've exited the shape. Compute the number of spaces inside the
        # shape (not including the border) within this segment.
        segStart = entryVerticalLine[0]
        segEnd = x

        # Keep track of the spaces along a horizontal line that are
        # completely contained within the shape, and thus we should wholly
        # subtract them out (since we account for border spaces
        # separately).
        completelyContainedCount = 0

        # Iterate through all horizontal lines in this row.
        for horizLine in horizLines[y + 1]:
          hStart, hEnd = horizLine[1], horizLine[2]
          if segStart < hStart and hEnd < segEnd:
            # This horizontal line is completely contained within the segment.
            # Delete the whole thing.
            completelyContainedCount += horizLine[2] - horizLine[1] + 1
          if hStart == segStart:
            # If the segment alines with the start of the horizontal line,
            # move the segment start to the end of the horizontal line so
            # we don't count it.
            segStart = hEnd
          if hEnd == segEnd:
            # Ditto end of the horizontal line.
            segEnd = hStart

        # Calculate the number of interior spaces in this segment and add
        # them to the total. Ignore if negative.
        segCount = segEnd - segStart - 1 - completelyContainedCount
        if segCount > 0:
          insideCount += segCount

        # We've exited the shape. Reset the entry line.
        entryVerticalLine = None

    if len(horizLines[y]) > 0 or len(horizLines[y + 1]) > 0:
      print('inside count after row:', y, insideCount)

  print('borderCount:', borderCount)
  print('insideCount:', insideCount)
  print(borderCount + insideCount)

part2()
