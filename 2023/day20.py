from collections import defaultdict, namedtuple
from enum import Enum
from math import lcm

input = open('day20.txt').read().splitlines()

class ModuleType(Enum):
  BROADCASTER: int = 1
  FLIP_FLOP: int = 2
  CONJUNCTION: int = 3

Module = namedtuple('Module', ['name', 'type', 'value', 'dsts'])

Pulse = namedtuple('Pulse', ['src', 'moduleName', 'value'])

def parseInput() -> tuple[dict[str, Module], dict[str, dict[str, bool]]]:
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

  return modules, inputValues

def pulseStr(pulse: Pulse) -> str:
  src = pulse.src
  value = '-high' if pulse.value else '-low'
  output = pulse.moduleName
  return '%s %s-> %s' % (src, value, output)

def pulseModule(
  modules: dict[str, Module],
  inputValues: dict[str, dict[str, bool]],
  pulse: Pulse,
  buttonPressCount: int,
  conjunctionModulesToTrack: dict[str, int],
) -> list[Pulse]:

  name = pulse.moduleName
  if name not in modules:
    # this module is untyped, thus it forwards no pulses
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
      if pulse.value:
        return []
      modules[name] = Module(name, type, not value, dsts)
      for dst in dsts:
        r.append(Pulse(name, dst, not value))
    case ModuleType.CONJUNCTION:
      inputValues[name][pulse.src] = pulse.value
      if False in inputValues[name].values():
        output = True

        if name in conjunctionModulesToTrack:
          # This is one of the conjunction modules we're interested in
          # tracking when a high pulse is emitted. Record how many button
          # presses it took to get to this point.
          assert len(inputValues[name]) == 1, 'bad conj module tracking'
          conjunctionModulesToTrack[name] = buttonPressCount
      else:
        output = False
      for dst in dsts:
        r.append(Pulse(name, dst, output))
    case _:
      assert False, 'bad module type'

  return r

def pressButton(
  modules: dict[str, Module],
  inputValues: dict[str, dict[str, bool]],
  buttonPressCount: int = -1,
  conjunctionModulesToTrack: dict[str, int] = {}
) -> tuple[int, int]:
  highPulseCount = 0
  lowPulseCount = 0
  q = [Pulse('button', 'broadcaster', False)]
  while len(q) > 0:
    pulse = q.pop(0)
    value = pulse.value
    if value:
      highPulseCount += 1
    else:
      lowPulseCount +=1

    outputPulses = pulseModule(
      modules,
      inputValues,
      pulse,
      buttonPressCount,
      conjunctionModulesToTrack,
    )
    q.extend(outputPulses)

  return highPulseCount, lowPulseCount

def part1() -> None:
  modules, inputValues = parseInput()

  print(modules)
  print(inputValues)
  print('counts:', len(modules), len(inputValues))
  print()

  c = 1000
  high, low = 0, 0
  for i in range(c):
    print('button press', i)
    h, l = pressButton(modules, inputValues)
    high += h
    low += l
    print()

  print(modules)
  print()
  print(inputValues)
  print()
  print(high, low)
  print(high * low)

def part2() -> None:
  # This approach is heavily dependent on the following input structure.
  #
  # The target module is an untyped module (rx). This module has a single
  # input (call it L1), which is a conjunction module. This conjunction
  # module has four inputs (call them L2).
  #
  # To send a low pulse to the target, its input (L1) must receive all
  # high pulses, which means all four conjunction modules in L2 need to
  # emit high pulses in the same button press.
  #
  # It turns out that each L2 conjunction module emits a high pulse in a
  # consistent pattern: every X button presses, where X is different for
  # each module. So, we find this value for each module in L2 and take the
  # LCM of them all.

  modules, inputValues = parseInput()
  print('counts:', len(modules), len(inputValues))

  target = 'rx'
  print('target:', target)

  # L1
  assert len(inputValues[target]) == 1, 'target should only have one input'
  targetInput = list(inputValues[target].keys())[0]
  print('targetInput:', targetInput)
  assert modules[targetInput].type == ModuleType.CONJUNCTION, 'bad targetInput type'

  # L2
  conjunctionModulesToTrack = dict((n, -1) for n in inputValues[targetInput])
  print('conjunctionModulesToTrack:', conjunctionModulesToTrack)

  i = 1
  while True:
    pressButton(modules, inputValues, i, conjunctionModulesToTrack)
    i += 1

    if -1 not in conjunctionModulesToTrack.values():
      # If we've received a value for all relevant conjunction modules,
      # we're done.
      print('finished:', conjunctionModulesToTrack)
      print(lcm(*conjunctionModulesToTrack.values()))
      return

part2()
