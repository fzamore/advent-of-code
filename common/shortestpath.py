from collections import defaultdict
from heapq import heappush, heappop
from typing import Any, Callable, DefaultDict, Dict, Hashable, Iterable, List, Optional, Tuple, TypeVar

T = TypeVar('T', bound=Hashable)

# Implementation of Dijkstra's shortest-path algorithm.
# Params:
#  startNode (hashable): start node. distance to this node will always be zero
#  getAdjacentNodes (node => list of (node, distance) tuples): nodes adjacent
#       to given node. distances cannot be negative
#  isDestNode (node => bool): whether this node is a destination, and the
#       algorithm can terminate
# Return value:
#  (node, distance) tuple for destination node and distance to that node
def dijkstra(
    startNode: T,
    getAdjacentNodes: Callable[[T], Iterable[Tuple[T, float]]],
    isDestNode: Callable[[T], bool],
) -> Tuple[Optional[T], float]:
    result = _dijkstraInner(startNode, getAdjacentNodes, isDestNode)
    return (result[0], result[1])

# Implementation of Dijkstra's shortest-path algorithm that returns
# all shortest paths in the graph to a single destination node.
# Params:
#  startNode (hashable): start node. distance to this node will always be zero
#  getAdjacentNodes (node => list of (node, distance) tuples): nodes adjacent
#       to given node. distances cannot be negative
#  isDestNode (node => bool): whether this node is a destination, and the
#       algorithm can terminate
# Return value:
#  (node, distance, paths) tuple for destination node, distance to that node,
#       and all shortest paths from start to finish
def dijkstraAllShortestPaths(
    startNode: T,
    getAdjacentNodes: Callable[[T], Iterable[Tuple[T, float]]],
    isDestNode: Callable[[T], bool],
) -> Tuple[Optional[T], float, Iterable[list[T]]]:
    result = _dijkstraInner(startNode, getAdjacentNodes, isDestNode)
    return (
        result[0],
        result[1],
        _convertPrevToPaths(result[0], startNode, [], result[3]),
    )

def _convertPrevToPaths(node: Optional[T], startNode: T, curpath: list[T], p: Dict[T, list[T]]) -> Iterable[list[T]]:
    if node is None:
        yield []
        return

    # We move backward toward the start node.
    curpath.insert(0, node)
    if node == startNode:
        yield curpath
        return

    for prev in p[node]:
        for path in _convertPrevToPaths(prev, startNode, curpath.copy(), p):
            yield path

# Implementation of Dijkstra's shortest-path algorithm which returns
# shortest-path distances to all connected nodes in the graph.
# Params:
#  startNode (hashable): start node. distance to this node will always be zero
#  getAdjacentNodes (node => list of (node, distance) tuples): nodes adjacent
#       to given node. distances cannot be negative
# Return value:
#  dict[node, float] dictionary of distances from the start node to each
#       connected node
def dijkstraAllNodes(
    startNode: T,
    getAdjacentNodes: Callable[[T], Iterable[Tuple[T, float | int]]],
) -> Dict[T, float | int]:
    result = _dijkstraInner(
        startNode,
        getAdjacentNodes,
        lambda node: False,
    )
    return result[2]

def _dijkstraInner(
    startNode: T,
    getAdjacentNodes: Callable[[T], Iterable[Tuple[T, float | int]]],
    isDestNode: Callable[[T], bool],
) -> Tuple[
        Optional[T],
        float | int,
        Dict[T, float | int],
        Dict[T, list[T]],
    ]:
    # min-heap priority queue of points with distance from start as the key
    q: list[Any] = []

    # map from point to distance from start
    d: DefaultDict[T, float] = defaultdict(lambda: float('inf'))

    # map from point to list of previous points in the shortest path(s)
    p: Dict[T, list[T]] = {}

    # set of visited nodes, so we don't visit nodes more than once
    # (because we can't update entries in the priority queue)
    visited = set()

    # initialize with the start point
    heappush(q, (0, startNode))
    d[startNode] = 0

    # The start node has no previous nodes.
    p[startNode] = []

    while len(q) > 0:
        node = heappop(q)[1]

        if node in visited:
            continue
        visited.add(node)

        nodeDist = d[node]
        assert nodeDist != float('inf'), 'Missing point in dict for node: %s' % str(node)

        if isDestNode(node):
            # Done. (The third tuple value is empty because we don't need
            # to return all distances in this case.)
            return (node, nodeDist, {}, p.copy())

        for adjNode, adjNodeDist in getAdjacentNodes(node):
            assert adjNodeDist >= 0, 'negative weights not allowed: %d' % adjNodeDist
            if adjNode in visited:
                # No need to traverse to nodes we've already seen.
                continue

            newDist = nodeDist + adjNodeDist
            if newDist < d[adjNode]:
                # We've improved the distance to this point. Update the queue
                # and distance map. We don't need to modify its existing entry
                # in the priority queue (if it exists) because the new entry
                # will always be lower, and thus will be popped off the queue
                # before the existing entry. The existing entry will be
                # subsequently ignored because it's part of the "visited" set.
                d[adjNode] = newDist
                heappush(q, (newDist, adjNode))

                # Replace any prior previous points in the path.
                p[adjNode] = [node]

            elif newDist == d[adjNode]:
                # If we have a point that's equally close, add it to our list.
                assert adjNode in p, 'should have already encountered adjacent node: %s' % adjNode
                p[adjNode].append(node)

    # There was no path from start to finish.
    return (None, float('inf'), d.copy(), p.copy())

# Computes the shortest distance between each pair of vertices. Edge weights
# can be negative, but there can be no negative cycles.
# Params:
#   vertices: list of vertices
#   edgeWeights: mapping of edges to weights. each edge is a (v1, v2) tuple
# Return value:
#    mapping of (v1, v2) tuples to the shortest distance from v1 to v2
def floydWarshall(
    vertices: List[Hashable],
    edgeWeights: Dict[Tuple[Hashable, Hashable], int],
) -> Dict[Tuple[Hashable, Hashable], float]:

    dist: Dict[Tuple[Hashable, Hashable], float] = \
        defaultdict(lambda: float('inf'))

    c = len(vertices)
    for i in range(c):
        v = vertices[i]
        dist[(v, v)] = 0

    for v1, v2 in edgeWeights:
        dist[(v1, v2)] = edgeWeights[(v1, v2)]

    for k in range(c):
        K = vertices[k]
        for i in range(c):
            I = vertices[i]
            for j in range(c):
                J = vertices[j]
                dist[(I, J)] = min(dist[(I, K)] + dist[(K, J)], dist[(I, J)])

    return dist.copy()
