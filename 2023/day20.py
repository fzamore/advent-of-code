from collections import defaultdict, namedtuple
from enum import Enum

input = open('day20.txt').read().splitlines()

class ModuleType(Enum):
  BROADCASTER: int = 1
  FLIP_FLOP: int = 2
  CONJUNCTION: int = 3

Module = namedtuple('Module', ['name', 'type', 'value', 'dsts'])

Pulse = namedtuple('Pulse', ['src', 'moduleName', 'value'])

def pulseStr(pulse: Pulse) -> str:
  src = pulse.src
  value = '-high' if pulse.value else '-low'
  output = pulse.moduleName
  return '%s %s-> %s' % (src, value, output)

def pulseModule(
  modules: dict[str, Module],
  inputValues: dict[str, dict[str, bool]],
  name: str,
  srcModule: str,
  pulse: bool,
) -> list[Pulse]:

  if name not in modules:
    # this module is untyped, thus it forwards no pulses
    print('untyped module:', name)
    return []

  r = []
  dsts = modules[name].dsts
  type = modules[name].type
  value = modules[name].value
  match type:
    case ModuleType.BROADCASTER:
      for dst in dsts:
        r.append(Pulse(name, dst, value))
    case ModuleType.FLIP_FLOP:
      if pulse:
        return []
      modules[name] = Module(name, type, not value, dsts)
      for dst in dsts:
        r.append(Pulse(name, dst, not value))
    case ModuleType.CONJUNCTION:
      inputValues[name][srcModule] = pulse
      if False in inputValues[name].values():
        output = True
      else:
        output = False
      for dst in dsts:
        r.append(Pulse(name, dst, output))
      if len(inputValues[name]) > 1:
        print('conj values:', name, inputValues[name], output)
    case _:
      assert False, 'bad module type'

  return r

def button(
  modules: dict[str, Module],
  inputValues: dict[str, dict[str, bool]],
) -> tuple[int, int]:
  highPulseCount = 0
  lowPulseCount = 0
  q = [Pulse('button', 'broadcaster', False)]
  while len(q) > 0:
    pulse = q.pop(0)
    moduleName = pulse.moduleName
    src = pulse.src
    value = pulse.value

    print(pulseStr(pulse))

    if value:
      highPulseCount += 1
    else:
      lowPulseCount +=1

    q.extend(pulseModule(modules, inputValues, moduleName, src, value))

  return highPulseCount, lowPulseCount

def part1() -> None:
  modules = {}
  inputValues: dict[str, dict[str, bool]] = defaultdict(dict)

  for line in input:
    v = line.split(' -> ')
    assert len(v) == 2, 'bad input'
    dsts = v[1].split(', ')
    assert len(dsts) > 0, 'not enough dsts'

    if v[0] == 'broadcaster':
      name = v[0]
      type = ModuleType.BROADCASTER
    elif v[0][0] == '%':
      name = v[0][1:]
      type = ModuleType.FLIP_FLOP
    elif v[0][0] == '&':
      name = v[0][1:]
      type = ModuleType.CONJUNCTION
    modules[name] = Module(name, type, False, dsts)

    for dst in dsts:
      inputValues[dst][name] = False

  # delete non-conjunctions from inputValues for easier debugging
  keys = list(inputValues.keys())
  for key in keys:
    if key not in modules or modules[key].type != ModuleType.CONJUNCTION:
      del inputValues[key]

  print(modules)
  print(inputValues)
  print('counts:', len(modules), len(inputValues))
  print()

  c = 1000
  high, low = 0, 0
  for i in range(c):
    print('button press', i)
    h, l = button(modules, inputValues)
    high += h
    low += l
    print()

  print(modules)
  print()
  print(inputValues)
  print()
  print(high, low)
  print(high * low)

part1()
