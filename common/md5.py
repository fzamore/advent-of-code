try:
  # This seems to work in both Python and pypy, but we wrap it in a
  # try-catch, because I don't think it's advertised as being supported in
  # Python.
  from _md5 import md5 # type: ignore
except ModuleNotFoundError:
  from hashlib import md5

def md5hash(s: str) -> str:
  return str(md5(s.encode('utf-8')).hexdigest())

def _test(s: str, expected: str) -> None:
  print('Testing: "%s"' % s)
  actual = md5hash(s)
  assert len(actual) == 32, 'hash was incorrect length: %d' % len(actual)
  assert actual == expected, 'test case failed. input: "%s"; expected: %s: actual: %s' % (s, expected, actual)

if __name__ == '__main__':
  testcases: list[tuple[str, str]] = [
    ('abc', '900150983cd24fb0d6963f7d28e17f72',),
    ('', 'd41d8cd98f00b204e9800998ecf8427e'),
    ('inflammable means flammable? what a country!', 'dd8e6395d574a9988ef7b57ced3ecf67'),
  ]

  for s, expected in testcases:
    _test(s, expected)

  print('All tests passed.')

