from dataclasses import dataclass
import math
from typing import Optional

@dataclass
class Node:
    depth: int
    value: int = -1
    leftChild: Optional['Node'] = None
    rightChild: Optional['Node'] = None
    inorderPrev: Optional['Node'] = None
    inorderNext: Optional['Node'] = None

def increaseDepths(node):
    if node == None:
        return

    node.depth += 1
    increaseDepths(node.leftChild)
    increaseDepths(node.rightChild)

def findNodeToExplode(node):
    if node == None:
        return None

    #assert node.depth < 5, 'Node depth too high for explode'

    if node.depth == 4 and node.value == -1:
        return node

    result = findNodeToExplode(node.leftChild)
    if result:
        return result
    return findNodeToExplode(node.rightChild)

def explodeSingleStep(toExplode):
    assert toExplode.value == -1, 'bad node to explode: %d' % toExplode.value
    assert toExplode.leftChild.value != -1, 'bad left child of node to explode'
    assert toExplode.rightChild.value != -1, 'bad right child of node to explode'

    inorderPrev = toExplode.leftChild.inorderPrev
    inorderNext = toExplode.rightChild.inorderNext
    if inorderPrev:
        inorderPrev.value += toExplode.leftChild.value
        inorderPrev.inorderNext = toExplode
    if inorderNext:
        inorderNext.value += toExplode.rightChild.value
        inorderNext.inorderPrev = toExplode

    toExplode.value = 0
    toExplode.depth = 4
    toExplode.leftChild = None
    toExplode.rightChild = None
    toExplode.inorderPrev = inorderPrev
    toExplode.inorderNext = inorderNext

def findNodeToSplit(node):
    if node == None:
        return None

    #assert node.depth < 6, 'Node depth too high for split'

    if node.value >= 10:
        return node

    result = findNodeToSplit(node.leftChild)
    if result:
        return result
    return findNodeToSplit(node.rightChild)

def splitSingleStep(toSplit):
    assert toSplit.value >= 10, 'bad node to split: %d' % toSplit.value

    n1 = Node(toSplit.depth + 1)
    n2 = Node(toSplit.depth + 1)

    n1.value = math.floor(toSplit.value / 2)
    n2.value = math.ceil(toSplit.value / 2)

    n1.inorderPrev = toSplit.inorderPrev
    n1.inorderNext = n2

    n2.inorderPrev = n1
    n2.inorderNext = toSplit.inorderNext

    if toSplit.inorderPrev:
        toSplit.inorderPrev.inorderNext = n1
    if toSplit.inorderNext:
        toSplit.inorderNext.inorderPrev = n2

    toSplit.leftChild = n1
    toSplit.rightChild = n2
    toSplit.value = -1
    toSplit.inorderPrev = None
    toSplit.inorderNext = None

def isReduced(node):
    return findNodeToExplode(node) == None and findNodeToSplit(node) == None

def addNumbers(n1, n2):
    n = Node(0)
    n.leftChild = n1
    n.rightChild = n2

    n1Last = n1
    while n1Last.value == -1:
        n1Last = n1Last.rightChild
    n2First = n2
    while n2First.value == -1:
        n2First = n2First.leftChild

    n1Last.inorderNext = n2First
    n2First.inorderPrev = n1Last

    # increase depths of all nodes
    increaseDepths(n1)
    increaseDepths(n2)

    while not isReduced(n):
        toExplode = findNodeToExplode(n)
        if toExplode != None:
            explodeSingleStep(toExplode)
        else:
            toSplit = findNodeToSplit(n)
            if toSplit != None:
                splitSingleStep(toSplit)

    return n

def printIndent(s, indent):
    print('%s%s' % (' ' * indent, s))

def printNode(node, indent):
    if node.value == -1:
        assert node.leftChild != None and node.rightChild != None, 'Missing children for node: %s' % node

        printIndent('InternalNode (depth: %d)' % node.depth, indent)

        printIndent('LeftChild:', indent)
        printNode(node.leftChild, indent + 2)

        printIndent('RightChild:', indent)
        printNode(node.rightChild, indent + 2)

    else:
        s = '%d, inorderPrev: %d, inorderNext: %d' % (
            node.value,
            node.inorderPrev.value if node.inorderPrev else -1,
            node.inorderNext.value if node.inorderNext else -1,
        )
        printIndent(s, indent)


def printTree(root):
    print()
    print('***Tree***')
    printNode(root, 0)
    print()

def printNodeInorder(node):
    if node == None:
        return

    printNodeInorder(node.leftChild)
    if node.value != -1:
        print('%s ' % node.value, end='')
    printNodeInorder(node.rightChild)

def printTreeInorder(root):
    print()
    print('***Tree Inorder: ', end='')
    printNodeInorder(root)
    print()

def verifyTreeInorder(root):
    nodeList = []
    createNodeList(root, nodeList)

    #print([x.value for x in nodeList])

    inorderFirst = root
    while inorderFirst.value == -1:
        inorderFirst = inorderFirst.leftChild

    i = 0
    n = inorderFirst
    while n != None:
        #assert n.value != -1, 'Bad node value in inorder linkage'
        assert n.value == nodeList[i].value, 'Mismatched inorder values %d %d %d' % (
            i, n.value, nodeList[i].value
        )
        n = n.inorderNext
        i += 1

    for i in range(0, len(nodeList)):
        if i > 0:
            assert nodeList[i].inorderPrev == nodeList[i - 1], 'Incorrect prev link, %d %d %d' % (
                i, nodeList[i].value, nodeList[i - 1].value
            )
        if i < len(nodeList) - 1:
            #print(nodeList[i].inorderNext.value)
            assert nodeList[i].inorderNext == nodeList[i + 1], 'Incorrect next link, %d %d %d' % (
                i, nodeList[i].value, nodeList[i + 1].value
            )

def printNodeStr(node):
    if node == None:
        return

    if node.leftChild != None:
        print('[', end='')
    printNodeStr(node.leftChild)
    if node.value != -1:
        print(node.value, end='')
    else:
        print(',', end='')
    printNodeStr(node.rightChild)
    if node.rightChild != None:
        print(']', end='')

def printTreeStr(root):
    print()
    print('***Tree str: ', end='')
    printNodeStr(root)
    print()

def parseIntoNodes(numberStr, i=0, d=0):
    pos = i

    #assert d < 5, 'Node depth too high in input'
    result = Node(d)

    if numberStr[pos].isdigit():
        result.value = int(numberStr[pos])
        return pos + 1, result

    if numberStr[pos] == '[':
        pos += 1
        pos, subtree = parseIntoNodes(numberStr, pos, d + 1)
        result.leftChild = subtree

        assert numberStr[pos] == ',', 'did not find comma between nodes: %s, %d' % (numberStr, pos)

        pos += 1
        pos, subtree = parseIntoNodes(numberStr, pos, d + 1)
        result.rightChild = subtree

        assert numberStr[pos] == ']', 'did not find closing for node %s, %d' % (numberStr, pos)
        pos += 1

    return pos, result

def createNodeList(node, nodeList=[]):
    if node == None:
        return

    createNodeList(node.leftChild, nodeList)

    if node.value != -1:
        nodeList.append(node)

    createNodeList(node.rightChild, nodeList)

def createInorderLinks(root):
    nodeList = []
    createNodeList(root, nodeList)

    #print([x.value for x in nodeList])

    for i in range(len(nodeList)):
        if i > 0:
            nodeList[i].inorderPrev = nodeList[i - 1]
        if i < len(nodeList) - 1:
            nodeList[i].inorderNext = nodeList[i + 1]

def parseIntoTree(line):
    pos, number = parseIntoNodes(line)
    createInorderLinks(number)
    return number

def computeMagnitude(node):
    if node.value != -1:
        return node.value

    return \
        3 * computeMagnitude(node.leftChild) + \
        2 * computeMagnitude(node.rightChild)

def part1():
    numbers = []
    with open('day18.txt') as f:
        for line in f.read().splitlines():
            number = parseIntoTree(line)
            numbers.append(number)

    numberSum = numbers[0]
    for i in range(1, len(numbers)):
        numberSum = addNumbers(numberSum, numbers[i])

    printTreeInorder(numberSum)
    printTreeStr(numberSum)

    print(computeMagnitude(numberSum))

def part2():
    lines = open('day18.txt').read().splitlines()
    m = -float('inf')
    for i in range(0, len(lines)):
        for j in range(i + 1, len(lines)):
            assert i != j, 'i and j wrong'
            # parse the number each time because addition is apparently destructive
            n1 = parseIntoTree(lines[i])
            n2 = parseIntoTree(lines[j])
            numberSum = addNumbers(n1, n2)
            mag = computeMagnitude(numberSum)
            if mag > m:
                m = mag

            n1 = parseIntoTree(lines[j])
            n2 = parseIntoTree(lines[i])
            numberSum = addNumbers(n1, n2)
            mag = computeMagnitude(numberSum)
            if mag > m:
                m = mag


    print(m)

part2()
