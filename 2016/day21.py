from collections import deque
from common.ints import ints

input = open('day21.txt').read().splitlines()

Seq = list[str]

def swap(s: Seq, i: int, j: int) -> Seq:
	# We don't need to do this in-place, but it's simple enough.
	t = s[i]
	s[i] = s[j]
	s[j] = t
	return s

def rotate(s: Seq, n: int) -> Seq:
	d = deque(s)
	d.rotate(n)
	return list(d)

def reverse(s: Seq, i: int, j: int) -> Seq:
	assert i < j, 'bad reverse'
	return s[:i] + s[i:j + 1][::-1] + s[j + 1:]

def move(s: Seq, i: int, j: int) -> Seq:
	t = s.pop(i)
	s.insert(j, t)
	return s

def findReverseRotation(s: Seq, instr: str):
	d = deque(s)
	# We brute force all possible starting rotations to see if a regular
	# rotate will yield the desired output. It's brute force, but it works
	# because the length of the sequence is small.
	for _ in range(len(d)):
		d.rotate(1)
		if executeInstr((p := list(d)), instr, rev=False) == s:
			return p
	assert False, 'did not find reverse rotation'

def executeInstr(s: Seq, instr: str, *, rev: bool = False):
	v = instr.split()
	d = ints(instr)
	match v[0]:
		case 'swap':
			match v[1]:
				case 'position':
					# Same forward and back.
					return swap(s, d[0], d[1])
				case 'letter':
					i, j = (5, 2) if rev else (2, 5)
					return swap(s, s.index(v[i]), s.index(v[j]))
				case _:
					assert False, 'bad swap instr'
		case 'rotate':
			match v[1]:
				case 'left':
					n = -d[0] if rev else d[0]
					return rotate(s, -n)
				case 'right':
					n = -d[0] if rev else d[0]
					return rotate(s, n)
				case 'based':
					if rev:
						return findReverseRotation(s, instr)
					n = s.index(v[-1])
					n += 1 if n < 4 else 2
					return rotate(s, n)
				case _:
					assert False, 'bad rotate instr'
		case 'reverse':
			# Same forward and back.
			return reverse(s, d[0], d[1])
		case 'move':
			i, j = (d[1], d[0]) if rev else (d[0], d[1])
			return move(s, i, j)
		case _:
			assert False, 'bad instr'

def part1() -> None:
	start = 'abcdefgh'

	print('instrs:', len(input))

	s = list(start)
	print('input:', ''.join(s))
	for instr in input:
		s = executeInstr(s, instr)
	print(''.join(s))

def part2() -> None:
	start = 'fbgdceah'

	print('instrs:', len(input))

	s = list(start)
	print('input:', ''.join(s))
	for instr in input[::-1]:
		s = executeInstr(s, instr, rev=True)
	print(''.join(s))

part2()
