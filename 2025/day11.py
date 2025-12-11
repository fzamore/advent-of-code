from collections import defaultdict
from functools import cache

data = open('day11.txt').read().splitlines()

Graph = dict[str, list[str]]

def parse() -> Graph:
  g = defaultdict(list)
  for line in data:
    v = line.split()
    assert len(v) >= 2, 'bad input line'
    g[v[0][:-1]].extend(v[1:])
  return g

def dfs(g: Graph, start: str, target: str = 'out') -> int:
  @cache
  def dfsInner(n: str) -> int:
    return 1 if n == target else sum(dfsInner(an) for an in g[n])

  return dfsInner(start)

def part1() -> None:
  g = parse()
  print('nodes:', len(g))
  print(dfs(g, 'you'))

def part2() -> None:
  g = parse()
  print('nodes:', len(g))

  # We break the search into components. We first search from the start to
  # one intermediate node, then to the second intermediate node, then to
  # the finish. We multiply each partial result together to get the total
  # from start to end, visiting the two intermediate nodes in that order.
  # We then do the same thing, but switch the order of the intermediate
  # nodes. The answer is the sum of the two values.
  searches = [
    [
      ('svr', 'dac'),
      ('dac', 'fft'),
      ('fft', 'out'),
    ],
    [
      ('svr', 'fft'),
      ('fft', 'dac'),
      ('dac', 'out'),
    ],
  ]

  ans = 0
  for search in searches:
    pathResult = 1
    for start, target in search:
      print('starting dfs:', start, target)
      r = dfs(g, start, target)
      print('** result:', r)
      pathResult *= r
    print('total for path:', pathResult)
    ans += pathResult
    print('---')
  print(ans)

part2()
