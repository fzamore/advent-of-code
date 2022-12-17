from common.shortestpath import floydWarshall

input = open('day16.txt').read().splitlines()

def parseInput(
  input: list[str],
) -> tuple[dict[str, int], dict[tuple[str, str], int]]:
  values = {}
  edgeWeights = {}
  for line in input:
    name = line[6:8]
    value = int(line.split(';')[0].split('=')[1])

    values[name] = value

    v = line.split(' valves ')
    if len(v) == 1:
      v = line.split(' valve ')
    neighbors = v[1].split(', ')
    for neighbor in neighbors:
      edgeWeights[(name, neighbor)] = 1

  return (values, edgeWeights)

def moveToValve(
  curValve: str,
  closedValves: dict[str, int],
  dist: dict[tuple[str, str], int],
  minutesRemaining: int,
  totalScore: int,
  incrScore: int,
) -> int:
  assert totalScore >= 0, 'totalScore must be positive: %d' % totalScore
  assert incrScore >= 0, 'incrScore must be positive: %d' % incrScore

  # Returns how many minutes it would take to navigate to a valve and open it.
  def getMinutesToValve(valve: str) -> int:
    return dist[(curValve, valve)] + 1

  # Returns whether any valves are reachable.
  def canReachAnyValve() -> bool:
    for valve in closedValves:
      if getMinutesToValve(valve) <= minutesRemaining:
        return True
    return False

  if not canReachAnyValve():
    # We can't reach any more valves. Stop.
    return totalScore + minutesRemaining * incrScore

  best = -1
  for valve in closedValves:
    # Navigate to this valve.
    closedValvesCopy = closedValves.copy()
    # Open the valve by removing it from the closed valves set.
    del closedValvesCopy[valve]
    minutesToValve = getMinutesToValve(valve)
    score = moveToValve(
      valve,
      closedValvesCopy,
      dist,
      minutesRemaining - minutesToValve,
      totalScore + minutesToValve * incrScore,
      incrScore + closedValves[valve],
    )
    if score > best:
      best = score

  return best

def part1():
  values, edgeWeights = parseInput(input)
  print('total node count:', len(values))

  # Compute distances between all pairs of points.
  distances = floydWarshall(list(values.keys()), edgeWeights)

  # Filter to only valves with non-zero flow value.
  closedValves = dict(
    [(valve, value) for valve, value in values.items() if value > 0],
  )

  print(closedValves)
  print('non-zero valve count:', len(closedValves))

  assert values['AA'] == 0, 'bad start node value: %d' % values['AA']
  score = moveToValve('AA', closedValves, distances, 30, 0, 0)
  print(score)

part1()
