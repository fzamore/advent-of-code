def isValidYear(vStr, minV, maxV):
    if len(vStr) != 4:
        return False
    year = int(vStr)
    return year >= minV and year <= maxV

def isValid(d):
    if len(d) != 7:
        return False

    for field in d:
        v = d[field]
        match field:
            case 'byr':
                if not isValidYear(v, 1920, 2002):
                    return False
            case 'iyr':
                if not isValidYear(v, 2010, 2020):
                    return False
            case 'eyr':
                if not isValidYear(v, 2020, 2030):
                    return False
            case 'hgt':
                unit = v[-2:]
                if unit == 'cm':
                    vi = int(v[:-2])
                    if vi < 150 or vi > 193:
                        return False
                elif unit == 'in':
                    vi = int(v[:-2])
                    if vi < 59 or vi > 76:
                        return False
                else:
                    return False
            case 'hcl':
                if len(v) != 7:
                    return False
                if v[0] != '#':
                    return False
                for c in v[1:]:
                    if c not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']:
                        return False
            case 'ecl':
                if v not in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
                    return False
            case 'pid':
                if len(v) != 9:
                    return False
                if not v.isdigit():
                    return False
            case _:
                assert False, 'bad field: %s' % field

    return True

def part1():
    with open('day4.txt') as f:
        fields = [
            'byr',
            'iyr',
            'eyr',
            'hgt',
            'hcl',
            'ecl',
            'pid',
            #'cid',
        ]

        count = 0
        cur = set()
        for line in f.read().splitlines():
            if line == '':
                # blank line. validate fields
                if len(cur) == len(fields):
                    # all fields present
                    count += 1
                cur = set()
                continue

            v = line.split()
            for e in v:
                field = e.split(':')[0]
                if field == 'cid':
                    continue
                assert field in fields, 'bad field: %s' % field
                cur.add(field)

        if len(cur) == len(fields):
            count += 1
        print(count)

def part2():
    with open('day4.txt') as f:
        fields = [
            'byr',
            'iyr',
            'eyr',
            'hgt',
            'hcl',
            'ecl',
            'pid',
            #'cid',
        ]

        count = 0
        d = {}
        for line in f.read().splitlines():
            if line == '':
                if isValid(d):
                    count += 1
                d = {}
                continue

            v = line.split()
            for e in v:
                field = e.split(':')[0]
                if field == 'cid':
                    continue
                assert field in fields, 'bad field: %s' % field
                assert field not in d, 'field already present %s, %s, %s' % (field, d, line)
                d[field] = e.split(':')[1]

        print(count)

part2()
