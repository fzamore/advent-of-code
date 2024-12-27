from itertools import combinations

input = open('day25.txt').read().rstrip().split("\n\n")

def overlap(a: str, b: str) -> bool:
  assert len(a) == len(b), 'strings must be equal lengths'
  return any(a[i] == '#' and b[i] == '#' for i in range(len(a)))

def part1() -> None:
  # For each chunk, we simply check whether there is any overlap of pins
  # between corresponding cells within the chunk (we don't need to count
  # pins within a column, nor do we need to convert it into a 2D grid;
  # using a 1D string works just fine). We don't need to separate locks
  # and keys because all locks will overlap with all other locks (same for
  # keys), and thus won't be counted in the final answer.
  ans = sum(1 for (a, b) in combinations(input, 2) if not overlap(a, b))
  print(ans)

part1()
