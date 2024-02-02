input = open('day1.txt').read().splitlines()

def getFuel(mass: int) -> int:
  return mass // 3 - 2

def getFuel2(mass: int) -> int:
  result = 0
  while (fuel := getFuel(mass)) > 0:
    result += fuel
    mass = fuel
  return result

def part1() -> None:
  result = 0
  for line in input:
    mass = int(line)
    fuel = getFuel(mass)
    print(mass, fuel)
    result += fuel
  print(result)

def part2() -> None:
  result = 0
  for line in input:
    mass = int(line)
    fuel = getFuel2(mass)
    print(mass, fuel)
    result += fuel
  print(result)

part2()
