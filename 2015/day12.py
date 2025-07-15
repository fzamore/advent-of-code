from common.ints import ints
import json

data = open('day12.txt').read().rstrip()

Value = int | str | list | dict

def calc(d: int | str | list[Value] | dict[str, Value]) -> int:
  if isinstance(d, int):
    return d
  if isinstance(d, str):
    return 0
  if isinstance(d, list):
    return sum(calc(n) for n in d)
  assert isinstance(d, dict), 'bad input'
  if 'red' in d.values():
    return 0
  return sum(calc(v) for v in d.values())

def part1() -> None:
  print(sum(ints(data)))

def part2() -> None:
  d = json.loads(data)
  print(calc(d))

part2()
