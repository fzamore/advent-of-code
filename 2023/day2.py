from collections import namedtuple

input = open('day2.txt').read().splitlines()

Game = namedtuple('Game', ['id', 'red', 'green', 'blue'])

def parseCubeSet(cubeSetS: str) -> tuple[int, int, int]:
  cubesL = cubeSetS.split(', ')
  assert len(cubesL) <= 3, 'too many cubes in line: %s' % cubeSetS
  red, green, blue = 0, 0, 0
  for cubeS in cubesL:
    cubeL = cubeS.split(' ')
    assert len(cubeL) == 2, 'bad cube spec: %s' % cubeS
    match cubeL[1]:
      case 'red':
        assert red == 0, 'too many red spec'
        red = int(cubeL[0])
      case 'green':
        assert green == 0, 'too many green spec'
        green = int(cubeL[0])
      case 'blue':
        assert blue == 0, 'too many blue spec'
        blue = int(cubeL[0])
      case _:
        assert False, 'bad cube color: %s' % cubeL[1]
  return (red, green, blue)

# Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
def parseLine(line: str) -> Game:
  idS, cubesSetsS = line.split(': ')
  id = int(idS.split(' ')[1])
  cubeSetsL = cubesSetsS.split('; ')
  red, green, blue = 0, 0, 0
  for cubeSetS in cubeSetsL:
    result = parseCubeSet(cubeSetS)
    red = max(red, result[0])
    green = max(green, result[1])
    blue = max(blue, result[2])

  return Game(id, red, green, blue)

def part1():
  sum = 0
  for line in input:
    print(line)
    game = parseLine(line)
    print(game)
    # only 12 red cubes, 13 green cubes, and 14 blue cubes
    if game.red <= 12 and game.green <= 13 and game.blue <= 14:
      sum += game.id
  print(sum)

def part2():
  sum = 0
  for line in input:
    print(line)
    game = parseLine(line)
    power = game.red * game.green * game.blue
    print(power, game)
    sum += power
  print(sum)

part2()

