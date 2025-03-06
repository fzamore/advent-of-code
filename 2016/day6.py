from collections import Counter, defaultdict

input = open('day6.txt').read().splitlines()

def computeCounts() -> dict[int, Counter[str]]:
	n = len(input[0])
	counts: dict[int, Counter[str]] = defaultdict(Counter)
	for line in input:
		assert len(line) == n, 'bad input line'
		for i, c in enumerate(line):
			counts[i][c] += 1
	return counts

def part1() -> None:
	n = len(input[0])
	counts = computeCounts()
	ans = ''.join([counts[i].most_common(1)[0][0] for i in range(n)])
	print(ans)

def part2() -> None:
	n = len(input[0])
	counts = computeCounts()
	ans = ''.join([counts[i].most_common()[-1][0] for i in range(n)])
	print(ans)

part2()

