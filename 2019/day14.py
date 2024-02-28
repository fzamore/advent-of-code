from collections import Counter
from math import ceil

input = open('day14.txt').read().splitlines()

Requirement = tuple[int, str] # qty, elem
Reaction = tuple[int, list[Requirement]] # qty, reqs
Reactions = dict[str, Reaction] # elem, Reaction
Dependencies = set[str]

def computeReactions() -> Reactions:
  reactions = {}
  for line in input:
    srcS, dst = line.split(' => ')
    assert len(dst.split(', ')) == 1, 'can produce multiple dst'
    reqs = []
    for src in srcS.split(', '):
      qtyS, val = src.split()
      qty = int(qtyS)
      reqs.append((qty, val))
    qtyS, val = dst.split()
    qty = int(qtyS)
    assert val not in reactions, 'multiple reactions for same element'
    reactions[val] = (qty, reqs)
  return reactions

def computeDependencies(reactions: Reactions, elem: str) -> Dependencies:
  if elem == 'ORE':
    return set()

  results = set()
  for _, dep in reactions[elem][1]:
    results.add(dep)
    results.update(computeDependencies(reactions, dep))
  return results

# Returns the amount of each element needed to produce the given quantity
# of the given element.
def neededQtys(reactions: Reactions, need: str, qty: int) -> dict[str, int]:
  reaction = reactions[need]
  reactQty = reaction[0]
  numReactions = ceil(qty / reactQty)
  # This assumes there are no cycles in the graph.
  needs: dict[str, int] = Counter()
  for srcQty, src in reaction[1]:
    needs[src] += srcQty * numReactions
  return needs

def computeOreForFuel(
  reactions: Reactions,
  dependencies: dict[str, Dependencies],
  fuel: int,
):
  needs = Counter({'FUEL': fuel})
  while not (len(needs) == 1 and 'ORE' in needs):
    # Choose an element with no dependencies among any of our needs.
    choice = None
    for guess in needs:
      if not any([guess in dependencies[n] for n in needs]):
        choice = guess
        break
    assert choice is not None, 'could not find choice'

    # Compute all needs for this choice and add them to our current needs.
    needs += neededQtys(reactions, choice, needs[choice])

    # We're done with this choice.
    del needs[choice]

  assert 'ORE' in needs, 'did not result in ore'
  return needs['ORE']

def part1() -> None:
  reactions = computeReactions()

  print(reactions)
  print(len(reactions))

  dependencies: dict[str, Dependencies] = {'ORE': set()}
  for elem in reactions:
    dependencies[elem] = computeDependencies(reactions, elem)

  print('dependencies:', dependencies)

  print()
  print('fuel:')
  assert reactions['FUEL'][0] == 1, 'bad fuel reaction'
  print(reactions['FUEL'])
  print()

  ore = computeOreForFuel(reactions, dependencies, 1)
  print(ore)

def part2() -> None:
  reactions = computeReactions()

  dependencies: dict[str, Dependencies] = {'ORE': set()}
  for elem in reactions:
    dependencies[elem] = computeDependencies(reactions, elem)

  print('dependencies:', dependencies)

  print()
  print('fuel:')
  assert reactions['FUEL'][0] == 1, 'bad fuel reaction'
  print(reactions['FUEL'])
  print()

  target = 1000000000000

  # Binary search
  low = 1
  hi = 100000000 # through experimentation
  while low < hi - 1:
    print('search', low, hi)
    mid = (low + hi) // 2
    ore = computeOreForFuel(reactions, dependencies, mid)
    assert ore != target, 'oops, found target'
    if ore < target:
      low = mid
    else:
      hi = mid

  print('done', low, hi)
  print(low)

part2()
