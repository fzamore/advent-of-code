from common.ints import ints
from functools import cache

input = open('day24.txt').read().splitlines()

Port = int
Component = tuple[Port, Port]

def parseInput() -> list[Component]:
  components = []
  for line in input:
    p1, p2 = ints(line)
    comp = p1, p2
    assert comp not in components, 'duplicate component'
    components.append(comp)
  return components

@cache
def findStrongest(components: tuple[Component], lastPort: Port = 0) -> int:
  candidates = (c for c in components if lastPort in c)

  result = 0
  for comp in candidates:
    p1, p2 = comp
    assert p1 == lastPort or p2 == lastPort, 'bad component'
    ncomponents = tuple(c for c in components if c != comp)

    nLastPort = p1 if p2 == lastPort else p2
    result = max(result, p1 + p2 + findStrongest(ncomponents, nLastPort))

  return result

@cache
def findLongest(components: tuple[Component], lastPort: Port = 0) -> tuple[int, int]:
  candidates = (c for c in components if lastPort in c)
  longest = 0
  strongest = 0
  for comp in candidates:
    p1, p2 = comp
    assert p1 == lastPort or p2 == lastPort, 'bad component'
    ncomponents = tuple(c for c in components if c != comp)

    nLastPort = p1 if p2 == lastPort else p2
    nlongest, nstrongest = findLongest(ncomponents, nLastPort)
    nlongest += 1
    nstrongest += p1 + p2
    if nlongest > longest:
      longest = nlongest
      strongest = nstrongest
    elif nlongest == longest:
      strongest = max(strongest, nstrongest)

  return longest, strongest

def part1() -> None:
  components = parseInput()
  print('components:', len(components))
  ans = findStrongest(tuple(components))
  print(ans)

def part2() -> None:
  components = parseInput()
  print('components:', len(components))
  ans = findLongest(tuple(components))
  print('result:', ans)
  print(ans[1])

part2()
