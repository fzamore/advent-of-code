from typing import Iterable
from common.ints import ints
from common.shortestpath import dijkstra

data = open('day10.txt').read().splitlines()

State = tuple[bool, ...]
Button = list[int]

def parse() -> list[tuple[State, list[Button]]]:
  r = []
  for line in data:
    assert line.count(']') == 1, 'bad input line'
    target = tuple(c == '#' for c in line[1:line.index(']')])

    v = line.split()
    assert len(v) >= 3, 'bad input line'
    buttons = [ints(e) for e in v[1:-1]]
    r.append((target, buttons))

  return r

def toggle(state: State, button: Button) -> State:
  return tuple(not state[i] if i in button else state[i] for i in range(len(state)))

def solve(target: State, buttons: list[Button]) -> int:
  n = len(target)
  start = tuple(False for _ in range(n))

  def getAdj(state: State) -> Iterable[tuple[State, int]]:
    for button in buttons:
      yield toggle(state, button), 1

  def isDone(state: State) -> bool:
    return state == target

  r = dijkstra(start, getAdj, isDone)
  return int(r[1])

def part1() -> None:
  parsed = parse()
  print('data:', len(parsed))
  ans = 0
  for target, buttons in parsed:
    result = solve(target, buttons)
    print('result:', result)
    ans += result
  print(ans)

part1()

