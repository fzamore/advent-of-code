from collections import defaultdict

def part1():
    with open('day6.txt') as f:
        group = set()
        total = 0
        for line in f.read().splitlines():
            if line == '':
                # blank line
                total += len(group)
                group = set()
                continue

            for c in line:
                group.add(c)

        total += len(group)
        print(total)

def part2():
    with open('day6.txt') as f:
        counts = defaultdict(int)
        peopleCount = 0
        total = 0
        for line in f.read().splitlines():
            if line == '':
                # blank line
                for c in counts:
                    if counts[c] == peopleCount:
                        total += 1

                counts = defaultdict(int)
                peopleCount = 0
                continue

            for c in line:
                counts[c] += 1
            peopleCount += 1

        for c in counts:
            if counts[c] == peopleCount:
                total += 1
        print(total)

part2()
