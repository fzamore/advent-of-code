from typing import Iterable, Optional

# Ranges are inclusive.

# Subtracts r2 from r1. The result could be zero, one, or two ranges.
SubtractionResult = tuple[Optional[range], Optional[range]]
def subtractRange(r1: range, r2: range) -> SubtractionResult:
  if r2.stop < r1.start:
    # no overlap
    return (None, r1)
  if r2.start > r1.stop:
    # no overlap
    return (r1, None)
  if r2.start <= r1.start and r2.stop >= r1.stop:
    # r1 entirely contained within r2
    return (None, None)
  if r2.start > r1.start and r2.stop < r1.stop:
    # r2 entirely contained between within r1
    return (range(r1.start, r2.start - 1), range(r2.stop + 1, r1.stop))
  if r2.start <= r1.start:
    return (None, range(r2.stop + 1, r1.stop))
  if r2.stop >= r1.stop:
    return (range(r1.start, r2.start - 1), None)
  else:
    assert False, 'bad range subtraction: %s, %s' % (r1, r2)

# Subtracts multiple ranges from a single range. Only non-empty ranges are
# included in the result. Maximum number of results is 2^(number of
# minuends), due to each individual subtraction generating up to two
# results (i.e., branching factor of two).
def subtractMultipleRanges(subtrahend: range, minuends: Iterable[range]) -> list[range]:
  results = [subtrahend]
  for minuend in minuends:
    tempResults = []
    for subtra in results:
      r1, r2 = subtractRange(subtra, minuend)
      if r1 is not None:
        tempResults.append(r1)
      if r2 is not None:
        tempResults.append(r2)
    results = tempResults
  return tempResults

def _testSingle(r1: range, r2: range, expected: SubtractionResult) -> None:
  print('Testing: "%s - %s"' % (r1, r2))
  actual = subtractRange(r1, r2)
  assert actual == expected, 'test case failed. expected: %s: actual: %s' % (expected, actual)

def _testMultiple(subtrahend: range, minuends: Iterable[range], expected: list[range]) -> None:
  print('Testing: "%s - %s"' % (subtrahend, minuends))
  actual = subtractMultipleRanges(subtrahend, minuends)
  assert actual == expected, 'test case failed. expected: %s: actual: %s' % (expected, actual)

if __name__ == '__main__':
  singleTestcases: list[tuple[range, range, SubtractionResult]] = [
    (range(1, 10), range(-10, -1), (None, range(1, 10))), # no overlap
    (range(1, 10), range(11, 15), (range(1, 10), None)), # no overlap
    (range(1, 10), range(0, 20), (None, None)), # r1 contained within r2
    (range(1, 10), range(3, 4), (range(1, 2), range(5, 10))), # r2 contained within r1
    (range(1, 10), range(-3, 5), (None, range(6, 10))),
    (range(1, 10), range(3, 15), (range(1, 2), None)),
    (range(1, 10), range(1, 10), (None, None)),
    (range(1, 10), range(10, 12), (range(1, 9), None)),
  ]

  print('testing subtractRange()')
  for r1, r2, expectedSingle in singleTestcases:
    _testSingle(r1, r2, expectedSingle)

  multipleTestcases: list[tuple[range, list[range], list[range]]] = [
    (range(1, 10), [range(2, 3), range(2, 4), range(6, 7)], [range(1, 1), range(5, 5), range(8, 10)]),
    (range(1, 10), [range(-3, 3), range(20, 40)], [range(4, 10)]),
    (range(1, 10), [range(1, 30), range(2, 4)], []),
  ]

  print()
  print('testing subtractMultipleRanges()')
  for subtrahend, minuends, expectedMultiple in multipleTestcases:
    _testMultiple(subtrahend, minuends, expectedMultiple)

  print('All tests passed.')
