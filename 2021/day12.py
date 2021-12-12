def addEdge(graph, start, end):
    if start not in graph:
        graph[start] = []
    graph[start].append(end)

def addPathIfNecessary(paths, path):
    pathStr = ','.join(path)
    if not pathStr in paths:
        paths.add(pathStr)

def visit(graph, paths, node, path):
    if node == 'end':
        addPathIfNecessary(paths, path)
        return

    if node.islower() and node in path:
        return

    path.append(node)
    for v in graph[node]:
        visit(graph, paths, v, path.copy())
    path.pop()

def hasMultipleLowerNodes(path):
    s = set()
    for node in path:
        if not node.islower():
            continue
        if node in s:
            return True
        s.add(node)
    return False

def canVisitLowerNode(node, path):
    assert node.islower(), 'Invalid node in canVisitLowerNode: %s' % node
    match node:
      case 'start':
        return node not in path
      case 'end':
        return node not in path
      case _:
        return node not in path or not hasMultipleLowerNodes(path)

def visit2(graph, paths, node, path):
    if node == 'end':
        path.append(node)
        addPathIfNecessary(paths, path)
        return

    if node.islower() and not canVisitLowerNode(node, path):
        return

    path.append(node)
    for v in graph[node]:
        visit2(graph, paths, v, path.copy())
    path.pop()

def part1():
    graph = {}
    f = open('day12.txt')
    for line in f.readlines():
        vertices = line[:-1].split('-')
        assert len(vertices) == 2, 'Bad line: %s' % line
        addEdge(graph, vertices[0], vertices[1])
        addEdge(graph, vertices[1], vertices[0])
    f.close()

    paths = set()
    visit(graph, paths, 'start', [])
    print(len(paths))

def part2():
    graph = {}
    f = open('day12.txt')
    for line in f.readlines():
        vertices = line[:-1].split('-')
        assert len(vertices) == 2, 'Bad line: %s' % line
        addEdge(graph, vertices[0], vertices[1])
        addEdge(graph, vertices[1], vertices[0])
    f.close()

    paths = set()
    visit2(graph, paths, 'start', [])
    print(len(paths))

part2()
