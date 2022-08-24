from common.readfile import readfile
from collections import defaultdict

def parseContainedBags(bagStr):
    bagStr = bagStr[:-1] # chomp off period
    result = {}

    if bagStr == 'no other bags':
        return result

    for bagS in bagStr.split(', '):
        v = bagS.split()
        assert len(v) == 4, 'bad line: %s' % bagStr
        assert v[3] == 'bag' or v[3] == 'bags', 'bag str should end with bag[s]: %s' % bagStr

        count = int(v[0])
        bagType = '%s %s' % (v[1], v[2])
        result[bagType] = count

    return result

def countSubBags(rules, bag):
    count = 0
    for subBag in rules[bag]:
        c = rules[bag][subBag]
        count += c
        count += c * countSubBags(rules, subBag)
    return count

def part1():
    rules = defaultdict(lambda: defaultdict(int))
    shinyGoldContainers = set()
    active = set()
    for line in readfile('day7.txt'):
        v = line.split(' bags contain ')
        container = v[0]
        bags = parseContainedBags(v[1])
        for bag in bags:
            rules[container][bag] += bags[bag]
            if bag == 'shiny gold':
                shinyGoldContainers.add(container)
                active.add(container)

    print(rules.keys())

    while len(active) > 0:
        new = set()
        for container in rules:
            for bag in rules[container]:
                if bag in active:
                    new.add(container)
                    shinyGoldContainers.add(container)
        print('next', new)
        active = new

    print(shinyGoldContainers)
    print(len(shinyGoldContainers))

def part2():
    rules = defaultdict(lambda: defaultdict(int))
    shinyGoldContained = defaultdict(int)
    for line in readfile('day7.txt'):
        v = line.split(' bags contain ')
        container = v[0]
        bags = parseContainedBags(v[1])
        for bag in bags:
            rules[container][bag] += bags[bag]
            if container == 'shiny gold':
                shinyGoldContained[bag] += bags[bag]

    print('top level', shinyGoldContained)

    count = 0
    for bag in shinyGoldContained:
        c = shinyGoldContained[bag]
        count += c
        count += c * countSubBags(rules, bag)
    print(count)

part2()
