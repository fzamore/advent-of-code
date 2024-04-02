from itertools import cycle

input = open('day1.txt').read().splitlines()

def part1() -> None:
	print(sum(map(int, input)))

def part2() -> None:
	c = 0
	seen = set([c])
	for v in cycle(input):
		c += int(v)
		if c in seen:
			print(c)
			return
		seen.add(c)
	assert False, 'not infinite cycle'

part2()
