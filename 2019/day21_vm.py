from intcode import IntcodeVM

input = open('day21.txt').read().split(',')

def runAsciiProgram(program: list[str]) -> None:
  machine = IntcodeVM.initFromInput(input)
  for inst in program:
    machine.addAsciiInput(inst)

  for output in machine.run():
    assert output is not None, 'unexpected input request'
    if output >= 0x7F:
      print(output)
    else:
      print(chr(output), end='')

def part1() -> None:
  # Jump if (1, 2, or 3 spaces ahead is a hole) AND (4 spaces ahead is ground).
  #  (~A v ~B v ~C) ^ D
  program = [
    'NOT A J',
    'NOT B T',
    'OR T J',
    'NOT C T',
    'OR T J',
    'AND D J',
    'WALK',
  ]
  runAsciiProgram(program)

def part2() -> None:
  # Break the program into the next two jumps, and jump if both jumps are
  # possible.
  #
  # The condition for the first jump is the same as part 1: whether there
  # is a hole in the next three spaces and four spaces ahead is a hole.
  #
  # The condition for the second jump is whether the fifth space ahead is
  # ground (i.e., we don't need to jump right away and can walk at least
  # one step forward) OR the condition for the first jump translated four
  # steps forward (i.e., if any of the 5, 6, 7 spaces is a hole AND the 8
  # space is ground). Note that we don't use the 9-space (register I) at
  # all.
  #
  # This results in the following boolean expression:
  #   (D ^ (~A v ~B v ~C)) ^ (E v (H ^ (~E v ~F v ~G)))
  #
  # To simplify the second half: (E v (H ^ (~E v ~F v ~G))), consider two
  # cases: E is true or E is false. If E is true, then the entire
  # expression is trivially true. If E is false, then (~E v ~F v ~G) is
  # true, so we can remove it from the expression, leaving:
  #   (D ^ (~A v ~B v ~C)) ^ (E v H)
  #
  # This is equivalent to: (D ^ ~(A ^ B ^ C)) ^ (E v H)
  #   (fewer NOT operations)
  program = [
    # (D ^ ~(A ^ B ^ C))
    'OR C T',
    'AND B T',
    'AND A T',
    'NOT T T',
    'AND D T',

    # (E v H)
    'OR E J',
    'OR H J',

    # Combining the two above expressions.
    'AND T J',

    'RUN',
  ]
  runAsciiProgram(program)

part2()
