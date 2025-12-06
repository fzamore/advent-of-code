from typing import Iterable, Optional

# Ranges are inclusive.
Range = tuple[int, int]

def _validateRange(r: Range) -> None:
  assert type(r) is tuple and len(r) == 2 and r[0] <= r[1], 'bad range spec'

# Performs an intersection of the two ranges. None represents an empty
# intersection.
def intersectRanges(r1: Range, r2: Range) -> Optional[Range]:
  _validateRange(r1)
  _validateRange(r2)
  if r2[0] > r1[1] or r1[0] > r2[1]:
    return None
  return (max(r1[0], r2[0]), min(r1[1], r2[1]))

# Subtracts r2 from r1. The result could be zero, one, or two ranges.
SubtractionResult = tuple[Optional[Range], Optional[Range]]
def subtractRange(r1: Range, r2: Range) -> SubtractionResult:
  _validateRange(r1)
  _validateRange(r2)
  r1start, r1end = r1
  r2start, r2end = r2
  if r2end < r1start:
    # no overlap
    return (None, r1)
  if r2start > r1end:
    # no overlap
    return (r1, None)
  if r2start <= r1start and r2end >= r1end:
    # r1 entirely contained within r2
    return (None, None)
  if r2start > r1start and r2end < r1end:
    # r2 entirely contained between within r1
    return ((r1start, r2start - 1), (r2end + 1, r1end))
  if r2start <= r1start:
    return (None, (r2end + 1, r1end))
  if r2end >= r1end:
    return ((r1start, r2start - 1), None)
  else:
    assert False, 'bad range subtraction: %s, %s' % (r1, r2)

# Subtracts multiple ranges from a single range. Only non-empty ranges are
# included in the result. Maximum number of results is 2^(number of
# minuends), due to each individual subtraction generating up to two
# results (i.e., branching factor of two).
def subtractMultipleRanges(subtrahend: Range, minuends: Iterable[Range]) -> list[Range]:
  _validateRange(subtrahend)
  results = [subtrahend]
  for minuend in minuends:
    _validateRange(minuend)
    tempResults: list[Range] = []
    for subtra in results:
      r1, r2 = subtractRange(subtra, minuend)
      if r1 is not None:
        tempResults.append(r1)
      if r2 is not None:
        tempResults.append(r2)
    results = tempResults
  return results

def _testSingle(r1: Range, r2: Range, expected: SubtractionResult) -> None:
  print('Testing: "%s - %s"' % (r1, r2))
  actual = subtractRange(r1, r2)
  assert actual == expected, 'test case failed. expected: %s: actual: %s' % (expected, actual)

def _testMultiple(subtrahend: Range, minuends: Iterable[Range], expected: list[Range]) -> None:
  print('Testing: "%s - %s"' % (subtrahend, minuends))
  actual = subtractMultipleRanges(subtrahend, minuends)
  assert actual == expected, 'test case failed. expected: %s: actual: %s' % (expected, actual)

if __name__ == '__main__':
  singleTestcases: list[tuple[Range, Range, SubtractionResult]] = [
    ((1, 10), (-10, -1), (None, (1, 10))), # no overlap
    ((1, 10), (11, 15), ((1, 10), None)), # no overlap
    ((1, 10), (0, 20), (None, None)), # r1 contained within r2
    ((1, 10), (3, 4), ((1, 2), (5, 10))), # r2 contained within r1
    ((1, 10), (-3, 5), (None, (6, 10))),
    ((1, 10), (3, 15), ((1, 2), None)),
    ((1, 10), (1, 10), (None, None)),
    ((1, 10), (10, 12), ((1, 9), None)),
  ]

  print('testing subtract()')
  for r1, r2, expectedSingle in singleTestcases:
    _testSingle(r1, r2, expectedSingle)

  multipleTestcases: list[tuple[Range, list[Range], list[Range]]] = [
    ((1, 10), [(2, 3), (2, 4), (6, 7)], [(1, 1), (5, 5), (8, 10)]),
    ((1, 10), [(-3, 3), (20, 40)], [(4, 10)]),
    ((1, 10), [(1, 30), (2, 4)], []),
  ]

  print()
  print('testing subtractMultipleRanges()')
  for subtrahend, minuends, expectedMultiple in multipleTestcases:
    _testMultiple(subtrahend, minuends, expectedMultiple)

  print('All tests passed.')
