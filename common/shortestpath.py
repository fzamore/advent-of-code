from collections import defaultdict
from heapq import heappush, heappop
from typing import Any, Callable, DefaultDict, Hashable, Iterator, Tuple

# Implementation of Dijkstra's shortest-path algorithm.
# Params:
#  startNode (hashable): start node. distance to this node will always be zero
#  getAdjacentNodes (node => list of (node, distance) tuples): nodes adjacent
#       to given node
#  isDestNode (node => Boolean): whether this node is a destination, andM the
#       algorithm can terminate
# Return value:
#  (node, distance) tuple for destination node and distance to that node
def dijkstra(
    startNode: Hashable,
    getAdjacentNodes: Callable[[Hashable], Iterator[Tuple[Hashable, float]]],
    isDestNode: Callable[[Hashable], bool],
) -> Tuple[Hashable, float]:

    # min-heap priority queue of points with distance from start as the key
    q: list[Any] = []

    # map from point to distance from start
    d: DefaultDict[Hashable, float] = defaultdict(lambda: float('inf'))

    # set of visited nodes, so we don't visit nodes more than once
    # (because we can't updated entries in the priority queue)
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
            # done
            return (node, nodeDist)

        for adjNode, adjNodeDist in getAdjacentNodes(node):
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
    return (None, float('inf'))
