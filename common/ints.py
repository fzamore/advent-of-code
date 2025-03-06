import re

def ints(s: str) -> list[int]:
  pattern = r'-?\d+'
  return list(map(int, re.findall(pattern, s)))

def _test(s: str, expected: list[int]) -> None:
  print('Testing: "%s"' % s)
  actual = ints(s)
  assert actual == expected, 'test case failed. input: "%s"; expected: %s: actual: %s' % (s, expected, actual)

if __name__ == '__main__':
  testcases: list[tuple[str, list[int]]] = [
    ('I have 4 apples and 3 oranges', [4, 3]),
    ('-334 is the way from 12 to 47, -6, and 901', [-334, 12, 47, -6, 901]),
    ('Blueprint 19: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 2 ore and 17 clay. Each geode robot costs 3 ore and 11 obsidian.', [19, 4, 4, 2, 17, 3, 11]),
    ('no ints in this string', []),
    ('making sure that 3 5 can be parsed with a c=-7 newline\n', [3, 5, -7]),
    ('decimals are handled poorly: 4.5', [4, 5]),
    ('ranges are handled poorly: 4-5', [4, -5]),
  ]

  for s, expected in testcases:
    _test(s, expected)

  print('All tests passed.')
