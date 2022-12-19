from functools import cache
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

def part1():
  values, edgeWeights = parseInput(input)
  print('total node count:', len(values))

  # Compute distances between all pairs of points.
  distances = floydWarshall(list(values.keys()), edgeWeights)

  # Filter to only valves with non-zero flow value.
  closedValves = tuple([valve for valve, value in values.items() if value > 0])

  print(closedValves)
  print('non-zero valve count:', len(closedValves))

  @cache
  def getMaxScore(
    valve: str,
    closedValves: tuple[str], # tuples can be memoized
    minutesRemaining: int,
  ) -> int:
    score = 0
    for closedValve in closedValves:
      minutesToValve = distances[valve, closedValve] + 1
      if minutesRemaining < minutesToValve:
        # Not enough time to reach this valve.
        continue
      # Remove this valve from the new collection of closed valves.
      closedValvesCopy = tuple([v for v in closedValves if v != closedValve])
      # Immediately add the total pressure for opening this valve, and
      # then add the score by moving to that valve. Update our total if
      # it's higher.
      score = max(
        score,
        (minutesRemaining - minutesToValve) * values[closedValve] + \
          getMaxScore(closedValve, closedValvesCopy, minutesRemaining - minutesToValve),
      )
    return score

  assert values['AA'] == 0, 'bad start node value: %d' % values['AA']
  score = getMaxScore('AA', closedValves, 30)
  print(score)

def part2():
  values, edgeWeights = parseInput(input)
  print('total node count:', len(values))

  # Compute distances between all pairs of points.
  distances = floydWarshall(list(values.keys()), edgeWeights)

  # Filter to only valves with non-zero flow value.
  nonZeroValves = tuple([valve for valve, value in values.items() if value > 0])

  print(nonZeroValves)
  print('non-zero valve count:', len(nonZeroValves))

  @cache
  def getMaxScore(
    valve: str,
    closedValves: tuple[str, ...], # tuples can be memoized
    minutesRemaining: int,
  ) -> int:
    score = 0
    for closedValve in closedValves:
      minutesToValve = distances[valve, closedValve] + 1
      if minutesRemaining < minutesToValve:
        # Not enough time to reach this valve.
        continue
      # Remove this valve from the new collection of closed valves.
      closedValvesCopy = tuple([v for v in closedValves if v != closedValve])
      # Immediately add the total pressure for opening this valve, and
      # then add the score by moving to that valve. Update our total if
      # it's higher.
      score = max(
        score,
        (minutesRemaining - minutesToValve) * values[closedValve] + \
          getMaxScore(closedValve, closedValvesCopy, minutesRemaining - minutesToValve),
      )
    return score

  # With more elephants!
  def getMaxScoreWithElephant(
    valve: str,
    closedValves: tuple[str, ...], # tuples can be memoized
    minutesRemaining: int,
  ) -> int:
    # Set the elephant loose on these valves by himself and use that as a
    # base score. I still don't understand how this doesn't double-count,
    # given that the same set of closed valves is under consideration
    # below.
    score = getMaxScore('AA', closedValves, 26)
    for closedValve in closedValves:
      minutesToValve = distances[valve, closedValve] + 1
      if minutesRemaining < minutesToValve:
        # Not enough time to reach this valve.
        continue
      # Remove this valve from the new collection of closed valves.
      newClosedValves = tuple([v for v in closedValves if v != closedValve])
      # Immediately add the total pressure for opening this valve, and
      # then add the score by moving to that valve. Update our total if
      # it's higher.
      score = max(
        score,
        (minutesRemaining - minutesToValve) * values[closedValve] + \
          getMaxScoreWithElephant(
            closedValve,
            newClosedValves,
            minutesRemaining - minutesToValve,
          ),
      )
    return score

  assert values['AA'] == 0, 'bad start node value: %d' % values['AA']
  score = getMaxScoreWithElephant('AA', nonZeroValves, 26)
  print(score)
part2()
