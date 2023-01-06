input = open('day25.txt').read().splitlines()

def snafuToDecimal(snafu: str) -> int:
  place = 1
  result = 0
  for i in range(len(snafu) - 1, -1, -1):
    c = snafu[i]
    if c.isdigit():
      assert int(c) in [0, 1, 2], 'bad snafu digit: %s' % c
      v = int(c)
    else:
      match c:
        case '-': v = -1
        case '=': v = -2
        case _: assert False, 'bad snafu char: %s' % c
    result += v * place
    place *= 5
  return result

def decimalToSnafu(decimal: int) -> str:
  table = {
    0: '0',
    1: '1',
    2: '2',
    3: '1=',
    4: '1-',
    5: '10',
    6: '11',
    7: '12',
    8: '2=',
    9: '2-',
  }
  result = ''
  while decimal not in table:
    decdigit = decimal % 5
    if decdigit < 3:
      snafudigit = str(decdigit)
      carry = 0
    elif decdigit == 4:
      snafudigit = '-'
      carry = 1
    else:
      snafudigit = '='
      carry = 2
    result = snafudigit + result
    decimal += carry
    decimal //= 5

  return table[decimal] + result

def part1():
  decimalSum = 0
  for snafu in input:
    decimal = snafuToDecimal(snafu)
    assert decimal > 0, 'bad result: %s, %d' % (snafu, decimal)
    print(snafu, decimal)
    decimalSum += decimal
  print('decimal sum:', decimalSum)
  print()

  print(decimalToSnafu(decimalSum))

part1()
