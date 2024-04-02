from collections import Counter
from itertools import combinations

input = open('day2.txt').read().splitlines()

def part1() -> None:
	twos, threes = set(), set()
	for s in input:
		c = Counter(s)
		for k in c:
			if c[k] == 2:
				twos.add(s)
			elif c[k] == 3:
				threes.add(s)
	print(len(twos) * len(threes))

def part2() -> None:
	for s1, s2 in combinations(input, 2):
		assert len(s1) == len(s2), 'strings should be same length'
		# Differing index
		di = -1
		for i, c1 in enumerate(s1):
			if c1 != s2[i]:
				if di != -1:
					di = -1
					break
				di = i

		if di != -1:
			print('done:', di)
			print(s1)
			print(s2)
			ans1 = s1[:di] + s1[di + 1:]
			ans2 = s2[:di] + s2[di + 1:]
			assert ans1 == ans2, 'removing digit from both strings should be same string'
			print()
			print(ans1)

part2()
