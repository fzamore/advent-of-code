from collections import Counter, deque

input = open('day7.txt').read().splitlines()

Deps = dict[str, tuple]

def parseInput() -> tuple[dict[str, int], Deps]:
  weights = {}
  deps = {}

  for line in input:
    n = line.split()[0]
    if ' -> ' in line:
      first, second = line.split(' -> ')
      deps[n] = tuple(second.split(', '))
    else:
      first = line
      deps[n] = ()

    weights[n] = int(first[len(n) + 2:-1])

  assert len(weights) == len(deps), 'bad input parsing'
  return weights, deps

def findRoot(deps: Deps) -> str:
  candidates = set(deps.keys())
  # Remove dependencies until we have only one entry.
  for n in deps:
    for dep in deps[n]:
      if dep in candidates:
        candidates.remove(dep)

  assert len(candidates) == 1, 'should have only found one candidate'
  for n in candidates:
    return n
  assert False, 'should have returned a value'

def recursiveWeight(n: str, deps: Deps, weights: dict[str, int]) -> int:
  return weights[n] + sum([recursiveWeight(d, deps, weights) for d in deps[n]])

def part1() -> None:
  _, deps = parseInput()

  print('items:', len(deps))
  print(findRoot(deps))

def part2() -> None:
  weights, deps = parseInput()

  print('items:', len(deps))
  root = findRoot(deps)
  print('root:', root)

  def rw(n: str) -> int:
    return recursiveWeight(n, deps, weights)

  # Parse the dependency tree from the top down and look for imbalances.
  # The last imbalance we find (i.e., the one furthest from the root) is
  # the answer we're looking for.
  adjustValues = []
  q = deque([root])
  while len(q) > 0:
    n = q.popleft()
    if len(deps[n]) == 0:
      continue

    for d in deps[n]:
      q.append(d)

    rweights = Counter([rw(d) for d in deps[n]])
    if len(rweights) > 1:
      # All subweights are not the same. We've found an imbalance.
      print('imbalance:', n, rweights)
      target = rweights.most_common(1)[0][0]
      print('target:', target)
      for d in deps[n]:
        if rw(d) != target:
          adjustValue = target - sum([rw(x) for x in deps[d]])
          print('adjust:', d, adjustValue)
          adjustValues.append(adjustValue)

  assert len(adjustValues) > 0, 'did not find any nodes to adjust'
  print(adjustValues[-1])

part2()
