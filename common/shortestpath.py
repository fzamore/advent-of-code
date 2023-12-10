from collections import defaultdict
from heapq import heappush, heappop
from typing import Any, Callable, DefaultDict, Dict, Hashable, Iterator, List, Tuple

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
    startNode: Hashable,
    getAdjacentNodes: Callable[[Hashable], Iterator[Tuple[Hashable, float]]],
    isDestNode: Callable[[Hashable], bool],
) -> Tuple[Hashable, float]:
    result = _dijkstraInner(startNode, getAdjacentNodes, isDestNode)
    return (result[0], result[1])

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
    startNode: Hashable,
    getAdjacentNodes: Callable[[Hashable], Iterator[Tuple[Hashable, float]]],
) -> Dict[Hashable, float]:
    result = _dijkstraInner(
        startNode,
        getAdjacentNodes,
        lambda node: False,
    )
    return result[2]

def _dijkstraInner(
    startNode: Hashable,
    getAdjacentNodes: Callable[[Hashable], Iterator[Tuple[Hashable, float]]],
    isDestNode: Callable[[Hashable], bool],
) -> Tuple[Hashable, float, Dict[Hashable, float]]:
    # min-heap priority queue of points with distance from start as the key
    q: list[Any] = []

    # map from point to distance from start
    d: DefaultDict[Hashable, float] = defaultdict(lambda: float('inf'))

    # set of visited nodes, so we don't visit nodes more than once
    # (because we can't update entries in the priority queue)
    visited = set()

    # initialize with the start point
    heappush(q, (0, startNode))
    d[startNode] = 0

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
            return (node, nodeDist, {})

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

    # There was no path from start to finish.
    return (None, float('inf'), d.copy())

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
