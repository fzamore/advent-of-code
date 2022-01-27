from common.io import readfile

def transform(n, s=7):
  # Python has fast modular exponentiation by default
  return pow(s, n, 20201227)
  
# Squaring exponentiation algorithm copied from 
# https://en.wikipedia.org/wiki/Modular_exponentiation
'''
def transform2(n, s=7):
  m = 20201227
  result = 1
  while n > 0:
    if n % 2 == 1:
      result = (result * s) % m
    n = n >> 1
    s = (s * s) % m
  return result
'''

# Obvious approach I copied from reddit. How I did not think of this is beyond me.
def findLoopSize2(pub):
  v = 1
  n = 0
  while v != pub:
    v = (7 * v) % 20201227
    n += 1
  return n

# Good lord, what the heck was I doing? This is silly and slow.
'''
def findLoopSize(pub):
  for i in range(1, 100000000):
    if transform(i) == pub:
      return i
  assert False, 'did not find loop size for public key: %d' % pub
'''

def part1():
  lines = readfile('day25.txt')
  pub1 = int(lines[0])
  pub2 = int(lines[1])
  print('public keys', pub1, pub2)

  loop1 = findLoopSize2(pub1)
  print('loop size 1', loop1)
  loop2 = findLoopSize2(pub2)
  print('loop size 2', loop2)
  
  enc1 = transform(loop2, pub1)
  enc2 = transform(loop1, pub2)
  assert enc1 == enc2, 'bad encryption keys: %d, %d' % (enc1, enc2)
  print(enc1)

part1()
