from intcode import IntcodeVM

inp = open('day25.txt').read().split(',')

def part1() -> None:
  # I got pretty lucky when exploring the maze manually and drawing out
  # the maze on paper. I manually determined the correct combination if
  # items I needed to get past the checkpoint: mug, prime number, food
  # ration, and fuel cell.

  # Through manual exploration, I found the following sequence of commmands.
  commands = [
    'east',
    'take food ration',
    'south',
    'take prime number',
    'north',
    'east',
    'east',
    'north',
    'north',
    'take fuel cell',
    'south',
    'south',
    'west',
    'west',
    'west',
    'north',
    'north',
    'west',
    'take mug',
    'east',
    'south',
    'west',
    'north',
    'west',
    'north',
  ]
  # Uncomment to play the game interactively.
  # commands = []

  machine = IntcodeVM.initFromInput(inp)
  for output in machine.run():
    if output is not None:
      print(chr(output), end='')
      continue

    if len(commands) > 0:
      command = commands.pop(0)
    else:
      command = input('--> ')
    machine.addAsciiInput(command)

part1()
