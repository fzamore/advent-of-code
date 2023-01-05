from enum import Enum
from math import ceil

input = open('day19.txt').read().splitlines()

class Robot(Enum):
  ORE = 0
  CLAY = 1
  OBSIDIAN = 2
  GEODE = 3

class Resource(Enum):
  ORE = 0
  CLAY = 1
  OBSIDIAN = 2

# If it takes this many minutes to produce a robot, we cannot produce it.
CANNOT_PRODUCE = 33

Resources = tuple[int, int, int] # quantities of ore, clay, and obsidian
Robots = tuple[int, int, int] # quantities of ore, clay, and obsidian robots

# Stores the costs for each robot type as a tuple.
Blueprint = tuple[Resources, Resources, Resources, Resources]

def parseInput() -> dict[int, Blueprint]:
  result = {}
  for line in input:
    id = int(line.split(':')[0].split()[1])
    values = line.split(':')[1].split('.')
    robots = {}
    for v in values:
      if v == '':
        continue
      robot = v.split()[1]
      costs = {}
      for s in v.split(' costs ')[1].split(' and '):
        resource = s.split()[1]
        cost = int(s.split()[0])
        costs[resource] = cost
      # Each robot will cost exactly one or two types of resources.
      assert len(costs) == 1 or len(costs) == 2
      robots[robot] = (
        costs.get('ore', 0),
        costs.get('clay', 0),
        costs.get('obsidian', 0),
      )
    result[id] = (
      robots['ore'],
      robots['clay'],
      robots['obsidian'],
      robots['geode'],
    )
    assert robots['geode'][2] >= 7, 'must require at least 7 obsidian to produce geode'
  return result

def consumeResourcesForNewRobot(
  resourcesForNewRobot: Resources,
  resources: Resources,
) -> Resources:
  return (
    resources[0] - resourcesForNewRobot[0],
    resources[1] - resourcesForNewRobot[1],
    resources[2] - resourcesForNewRobot[2],
  )

def produceResources(
  robots: Robots,
  resources: Resources,
  elapsedTime: int,
) -> Resources:
  return (
    resources[0] + elapsedTime * robots[0],
    resources[1] + elapsedTime * robots[1],
    resources[2] + elapsedTime * robots[2],
  )

def hasNeededResourcesNow(
  resources: Resources,
  resourcesNeeded: Resources,
) -> bool:
  for r in Resource:
    if resources[r.value] < resourcesNeeded[r.value]:
      return False
  return True

def getTimeToProduceRobot(
  resourcesNeeded: Resources,
  robots: Robots,
  resources: Resources,
) -> int:
  if hasNeededResourcesNow(resources, resourcesNeeded):
    # We have the resources to produce this robot immediately.
    return 0

  productionTime = 0
  for r in Resource:
    i = r.value
    # Calculate the minimum time to accumulate enough of this resource to
    # produce this robot, given our current robots and robots in progress.
    additionalResourcesNeeded = resourcesNeeded[i] - resources[i]
    if additionalResourcesNeeded <= 0:
      # We already have enough of this resource. Skip it.
      continue

    assert robots[i] >= 0
    if robots[i] == 0:
      # We cannot accumulate this resource, and thus cannot produce this
      # robot.
      return CANNOT_PRODUCE

    # Maintain the maximum production time across all resources, which
    # will be the minimum required time to produce the robot.
    productionTime = max(productionTime, ceil(additionalResourcesNeeded / robots[i]))

  assert productionTime > 0, 'bad result in time calculation: %d' % productionTime
  return productionTime

# Returns whether we have the maximum amount of a given resource that is
# required for any bot (and thus do not need to collect more).
def hasMaxResources(
  robot: Robot,
  blueprint: Blueprint,
  resources: Resources,
) -> bool:
  if robot == Robot.GEODE:
    return False
  i = robot.value
  return resources[i] >= max([r[i] for r in blueprint])

# Recursively compute the maximum number of geodes we can crack. At each
# level of recursion, we try to produce each robot type (if we have enough
# time), and advance the time by however long it takes to produce that
# robot. This eliminates the need to implement "waiting" to produce enough
# resources to produce a robot.
def computeMaxGeodes(
  blueprint: Blueprint,
  robots: Robots,
  resources: Resources,
  minutesRemaining: int,
) -> int:
  assert CANNOT_PRODUCE > minutesRemaining

  mostGeodesCracked = 0
  for robot in Robot:
    # First, try to buy this robot in however many minutes it will take to
    # accumulate sufficient resources.
    minutesUntilProductionStart = getTimeToProduceRobot(
      blueprint[robot.value],
      robots,
      resources,
    )
    assert 0 <= minutesUntilProductionStart <= CANNOT_PRODUCE

    # We always tick at least 1 minute when buying a robot. I think this
    # is because you can only build one robot in each minute, but I'm not
    # completely sure why this is.
    newMinutesRemaining = minutesRemaining - (minutesUntilProductionStart + 1)

    if newMinutesRemaining <= 0:
      # We do not have enough time to produce this robot.
      continue

    if hasMaxResources(robot, blueprint, resources):
      # Do not bother producing this robot if we're already have the
      # maximum resource that robot produces.
      continue

    # Consume the resources necessary to produce this robot.
    newResources = consumeResourcesForNewRobot(blueprint[robot.value], resources)

    # Accumulate resources from our existing robots (not including the new
    # one). Add one to account for the extra minute it takes to produce
    # the robot.
    newResources = produceResources(robots, newResources, minutesUntilProductionStart + 1)

    # Add the new robot to our list.
    newRobots = (
      robots[0] + (1 if robot == Robot.ORE else 0),
      robots[1] + (1 if robot == Robot.CLAY else 0),
      robots[2] + (1 if robot == Robot.OBSIDIAN else 0),
    )

    # Resursively compute the geodes cracked at the next step.
    geodesCracked = computeMaxGeodes(
      blueprint,
      newRobots,
      newResources,
      newMinutesRemaining,
    )

    assert newMinutesRemaining > 0
    geodesFromNewRobot = newMinutesRemaining if robot == Robot.GEODE else 0
    geodesCracked += geodesFromNewRobot

    if geodesCracked > mostGeodesCracked:
      mostGeodesCracked = geodesCracked

  return mostGeodesCracked

def part1():
  blueprints = parseInput()
  print('blueprints:', blueprints)
  print('num blueprints:', len(blueprints))
  print()

  minutesRemaining = 24
  result = 0
  for blueprintID in blueprints:
    print('blueprint:',  blueprintID)
    blueprint = blueprints[blueprintID]
    geodes = computeMaxGeodes(
      blueprint,
      (1, 0, 0),
      (0, 0, 0),
      minutesRemaining,
    )
    qualityScore = blueprintID * geodes
    print('blueprint finished:', blueprintID, geodes, qualityScore)
    print()
    result += qualityScore

  print(result)

def part2():
  blueprints = parseInput()
  if len(blueprints) > 3:
    blueprints = {
      1: blueprints[1],
      2: blueprints[2],
      3: blueprints[3],
    }
  print('blueprints:', blueprints)
  print('num blueprints:', len(blueprints))
  print()

  minutesRemaining = 32
  result = 1
  for blueprintID in blueprints:
    print('blueprint:',  blueprintID)
    blueprint = blueprints[blueprintID]
    geodes = computeMaxGeodes(
      blueprint,
      (1, 0, 0),
      (0, 0, 0),
      minutesRemaining,
    )
    print('blueprint finished:', blueprintID, geodes)
    result *= geodes
    print()

  print(result)

part2()
