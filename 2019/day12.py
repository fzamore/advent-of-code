from itertools import combinations
from math import lcm

input = open('day12.txt').read().splitlines()

Ship = dict[str, int]

def stepVelocity(s1: Ship, s2: Ship, dim: str) -> None:
  v1, v2 = s1[dim], s2[dim]
  vd = 'v' + dim
  if v1 < v2:
    s1[vd] += 1
    s2[vd] -= 1
  elif v2 < v1:
    s1[vd] -= 1
    s2[vd] += 1

def stepPosition(s: Ship, dim: str) -> None:
  s[dim] += s['v' + dim]

def step(ships: list[Ship]) -> None:
  for s1, s2 in combinations(ships, 2):
    stepVelocity(s1, s2, 'x')
    stepVelocity(s1, s2, 'y')
    stepVelocity(s1, s2, 'z')
  for s in ships:
    stepPosition(s, 'x')
    stepPosition(s, 'y')
    stepPosition(s, 'z')

def energy(s: Ship) -> int:
  pot = sum([abs(s[k]) for k in ['x', 'y', 'z']])
  kin = sum([abs(s[k]) for k in ['vx', 'vy', 'vz']])
  return pot * kin

def part1() -> None:
  ships = []
  for line in input:
    line = line[1:-1]
    v = line.split(', ')
    x = int(v[0][2:])
    y = int(v[1][2:])
    z = int(v[2][2:])
    ships.append({
      'x': x,
      'y': y,
      'z': z,
      'vx': 0,
      'vy': 0,
      'vz': 0,
    })
  print(ships)
  print(len(ships))

  for i in range(1000):
   step(ships)

  print('after')
  print(ships)

  print(sum([energy(s) for s in ships]))

def part2() -> None:
  print()
  ships = []
  for line in input:
    line = line[1:-1]
    v = line.split(', ')
    x = int(v[0][2:])
    y = int(v[1][2:])
    z = int(v[2][2:])
    ships.append({
      'x': x,
      'y': y,
      'z': z,
      'vx': 0,
      'vy': 0,
      'vz': 0,
    })
  print('initial:')
  print(ships)

  componentStates: dict[str, dict[tuple, int]] = {
    'x': {},
    'y': {},
    'z': {},
  }
  componentMatches: dict[str, tuple[tuple, int, int]] = {}

  stepNum = 0
  while True:
    for d in ['x','y','z']:
      componentState = tuple([(s[d], s['v'+d]) for s in ships])
      if componentState in componentStates[d]:
        if d not in componentMatches:
          componentMatches[d] = (
            componentState, # state
            componentStates[d][componentState], # last stepNum at this state
            stepNum, # this stepNum
          )
      else:
        # Store the stepNum for this (state, dimension) pair.
        componentStates[d][componentState] = stepNum

    if len(componentMatches) == 3:
      # Find the LCM of the repeated states of the x, y, and z dimensions.
      print('components matches:')
      print(componentMatches)
      print()
      print(lcm(*[componentMatches[d][2] - componentMatches[d][1] for d in componentMatches]))
      return

    step(ships)
    stepNum += 1

part2()
