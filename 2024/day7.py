from common.ints import ints

input = open('day7.txt').read().splitlines()

def parseInput() -> dict[int, list[int]]:
  equations = {}
  for line in input:
    v = ints(line)
    equations[v[0]] = v[1:]
    for n in v[1:]:
      assert n > 0, 'positive numbers required'
  print('equations:', len(equations))
  return equations

def canMatchBinary(target: int, values: list[int]) -> bool:
  # We have two possible operators for each slot. There are n - 1 slots,
  # so there are 2^(n - 1) possible combinations. To enumerate them, we
  # generate a bitstring of 2^(n - 1). I decided to not generalize this to
  # three operators because there is no built-in (that I know of) that
  # converts an int into a base-3 string.
  n = len(values)
  for binaryValue in range(2 ** (n - 1)):
    acc = values[0]
    bitstring = bin(binaryValue)[2:].zfill(n - 1)
    assert len(bitstring) == n - 1, 'bad bitstring'
    for i, b in enumerate(bitstring):
      v = values[i + 1]
      if b == '0':
        acc += v
      elif b == '1':
        acc *= v
      else:
        assert False
      if target == acc:
        return True
  return False

# This strategy can be generalized to any number of operators (though it
# may not be efficient).
def isMatch(target: int, values: list[int], acc: int, ops: list[str], vi: int) -> bool:
  if acc > target:
    # We've overshot the target. None of the operators will ever decrease
    # the running total, so we can conclude there is no match at this
    # point.
    return False

  if vi == len(values):
    # We're done.
    return acc == target

  v = values[vi]
  # Try each operator.
  for o in ops:
    match o:
      case '+':
        nacc = acc + v
      case '*':
        nacc = acc * v
      case '|':
        nacc = int(str(acc) + str(v))
      case _:
        assert False, 'bad op'

    # Recur on the next value.
    if isMatch(target, values, nacc, ops, vi + 1):
      return True

  return False

def part1() -> None:
  equations = parseInput()
  ans = sum([t for t in equations if canMatchBinary(t, equations[t])])
  print(ans)

def part2() -> None:
  equations = parseInput()

  ops = ['+', '*', '|']
  # We seed isMatch() with the first value in the list.
  ans = sum([t for t in equations if isMatch(t, equations[t], equations[t][0], ops, 1)])
  print(ans)

part2()
