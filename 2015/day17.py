from collections import Counter

data = open('day17.txt').read().splitlines()

Cans = tuple[int, ...]

# Returns the number of ways to fill a container of size n with the given
# cans. The result is a Counter that counts the number of ways to fill for
# each distinct quantity of cans.
def fill(
  cans: Cans,
  n: int = 150,
  lastCanChosen: int = -1,
  numCansUsed: int = 0,
) -> Counter[int]:
  assert n >= 0, 'cannot fill to negative'

  if n == 0:
    # Base case: we've filled the container.
    return Counter([numCansUsed])

  result: Counter[int] = Counter()
  # This is the magic sauce that avoids considering duplicate cases. We
  # proceed forward through the list of cans, so that subsequent recursive
  # calls do not consider prior cans.
  for i in range(lastCanChosen + 1, len(cans)):
    can = cans[i]
    if can <= n:
      # If we can fit this can in the container, recur and update the result.
      result += fill(cans, n - can, i, numCansUsed + 1)

  return result

def part1() -> None:
  cans = tuple(map(int, data))
  print('cans:', len(cans))
  print(fill(cans).total())

def part2() -> None:
  cans = tuple(map(int, data))
  print('cans:', len(cans))
  r = fill(cans)
  print('result:', r)
  print(r.most_common()[-1][1])

part2()
