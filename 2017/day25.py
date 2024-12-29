from common.ints import ints
from collections import namedtuple, defaultdict

# w == write, m == move, n == next (state)
State = namedtuple('State', ['id', 'w0', 'm0', 'n0', 'w1', 'm1', 'n1'])

input = open('day25.txt').read().splitlines()

def parseStatePart(data: list[str], i: int) -> tuple[int, tuple[int, int, str]]:
  w = ints(data[i])[0]
  i += 1
  assert 'left' in data[i] or 'right' in data[i], 'bad input'
  m = -1 if 'left' in data[i] else 1
  i += 1
  n = data[i][-2]
  i += 2
  return i, (w, m, n)

def parseState(data: list[str], i: int) -> tuple[int, State]:
  id = data[i][-2]
  i += 2

  i, (w0, m0, n0) = parseStatePart(data, i)
  i, (w1, m1, n1) = parseStatePart(data, i)

  return i, State(id, w0, m0, n0, w1, m1, n1)

def parseInput() -> tuple[str, int, dict[str, State]]:
  i = 0

  start = input[i][-2]
  i += 1

  target = ints(input[i])[0]
  i += 2

  states = {}
  while i < len(input) and input[i] != '':
    i, state = parseState(input, i)
    states[state.id] = state

  return start, target, states

def part1() -> None:
  start, target, states = parseInput()
  print('data:', start, target, states.keys())

  tape: dict[int, int] = defaultdict(int)
  i = 0
  state = states[start]

  for _ in range(target):
    if tape[i] == 0:
      tape[i] = state.w0
      i += state.m0
      state = states[state.n0]
    else:
      assert tape[i] == 1, 'bad tape value'
      tape[i] = state.w1
      i += state.m1
      state = states[state.n1]

  print(sum(tape.values()))

part1()
