from collections import namedtuple
from itertools import cycle, permutations

input = open('day7.txt').read().split(',')

State = namedtuple('State', ['pc', 'processedPhase'])

def getParameterValues(memory: list[int], baseI: int) -> list[int]:
  value = memory[baseI]
  opcode = value % 100
  paramModes = str(value // 100)
  if opcode in [1, 2, 5, 6, 7, 8]: # all two-value-param opcodes
    if len(paramModes) == 1:
      paramModes = '0' + paramModes
    assert len(paramModes) == 2

  values = []
  for i in range(len(paramModes)):
    mode = paramModes[len(paramModes) - i - 1]
    match mode:
      case '0':
        address = memory[baseI + i + 1]
        value = memory[address]
      case '1':
        value = memory[baseI + i + 1]
      case _:
        assert False, 'bad mode: %s' % mode
    values.append(value)
  assert len(values) in [1, 2], 'bad values: %s' % values
  return values

# We need to save state (especially the program counter) from the previous
# execution on each amplifier.
def runMachine(
  memory: list[int],
  state: State,
  phase: int,
  chainedInput: int,
) -> tuple[int, State, int]: # (opcode, State, value)
  pc = state.pc
  processedPhase = state.processedPhase
  while (value := memory[pc]) != 99:
    opcode = value % 100
    paramValues = getParameterValues(memory, pc)
    match opcode:
      case 1:
        assert len(paramValues) == 2, 'bad addition: %s' % [pc, value, paramValues]
        dst = memory[pc + 3]
        memory[dst] = paramValues[0] + paramValues[1]
        pc += 4
      case 2:
        assert len(paramValues) == 2, 'bad multiplication: %s' % [pc, value, paramValues]
        dst = memory[pc + 3]
        memory[dst] = paramValues[0] * paramValues[1]
        pc += 4
      case 3:
        dst = memory[pc + 1]
        input = chainedInput if processedPhase else phase
        processedPhase = True
        print('input inst at:', pc, input)
        memory[dst] = input
        pc += 2
      case 4:
        assert len(paramValues) == 1, 'bad output: %s' % paramValues
        output = paramValues[0]
        print('OUTPUT:', output)
        pc += 2
        return opcode, State(pc, processedPhase), output
      case 5:
        assert len(paramValues) == 2, 'bad jump-if-true: %s' % [pc, value, paramValues]
        if paramValues[0] != 0:
          pc = paramValues[1]
        else:
          pc += 3
      case 6:
        assert len(paramValues) == 2, 'bad jump-if-false: %s' % [pc, value, paramValues]
        if paramValues[0] == 0:
          pc = paramValues[1]
        else:
          pc += 3
      case 7:
        assert len(paramValues) == 2, 'bad less than: %s' % [pc, value, paramValues]
        dst = memory[pc + 3]
        memory[dst] = 1 if paramValues[0] < paramValues[1] else 0
        pc += 4
      case 8:
        assert len(paramValues) == 2, 'bad equals: %s' % [pc, value, paramValues]
        dst = memory[pc + 3]
        memory[dst] = 1 if paramValues[0] == paramValues[1] else 0
        pc += 4
      case _:
        assert False, 'bad opcode: %s' % opcode

  assert value == 99, 'bad halt opcode'
  return value, State(pc, processedPhase), chainedInput

def runSequence(memory: list[int], seq: list[int]) -> int:
  assert len(seq) == 5, 'bad sequence'
  chainedValue = 0
  for seqValue in seq:
    _, _, chainedValue = runMachine(memory, State(0, False), seqValue, chainedValue)
  return chainedValue

def runLoop(memory: list[int], phases: list[int]) -> int:
  assert len(phases) == 5, 'bad phases'
  programs = [memory.copy() for _ in range(5)]
  states = [State(0, False) for _ in range(5)]

  input = 0
  for i in cycle(range(5)): # infinite cycle
    opcode, newState, output = runMachine(
      programs[i],
      states[i],
      phases[i],
      input,
    )
    if opcode == 99:
      return output

    input = output
    states[i] = newState

  assert False, 'should have hit halt opcode'

def part1() -> None:
  memory = list(map(int, input))
  print(max([runSequence(memory, list(s)) for s in permutations(range(5))]))

def part2() -> None:
  memory = list(map(int, input))
  print(max([runLoop(memory, list(s)) for s in permutations(range(5, 10))]))

part2()
