from common.readfile import readfile

def speak(v, seen, spoken, i):
    #print('speak', i, v)
    spoken.append(v)
    if v not in seen:
        seen[v] = (None, i)
    else:
        seen[v] = (seen[v][1], i)

def part1():
    values = [int(x) for x in readfile('day15.txt')[0].split(',')]
    print(values)

    spoken = []
    seen = {}
    n = 30000000

    # starting numbers
    i = 1
    for v in values:
        speak(v, seen, spoken, i)
        i += 1

    while True:
        v = spoken[-1]
        if v not in seen:
            nv = 0
        else:
            s1, s2 = seen[v]
            assert s2 != None, 'value had not been spoken before: %d, %s' %(v, seen[v])
            if s1 == None:
                nv = 0
            else:
                nv = s2 - s1
        speak(nv, seen, spoken, i)
        if i == n:
            print('speak', i, nv)
            break
        i += 1

part1()
