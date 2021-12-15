from collections import defaultdict
from itertools import product
from typing import List, Tuple, Dict, Set
from heapdict import heapdict
from copy import deepcopy

Grid = List[List[int]]
Node = Tuple[int, int]
Graph = Dict[Node, Set[Node]]

def dijkstra(graph : Graph, start : Node, end : Node) -> int:
    ''' Dijkstra's with a heap - O(n log n + m log n) time '''
    dists = dict((node, float('inf')) for node in graph)
    lookups = dict((node, float('inf')) for node in graph)
    dists[start] = 0
    lookups[start] = 0

    # Let Q be a new heap
    Q = heapdict()
    Q[start] = 0
    for u in graph:
        if u != start:
            Q[u] = float('inf')

    while Q:
        # extract min
        u, dists[u] = Q.popitem()

        # consider outneighbors
        for v in graph[u]:
            if v in Q:
                dists[v] = lookups[v]
                if dists[v] > dists[u] + graph[u][v]:
                    Q[v] = dists[u] + graph[u][v]
                    lookups[v] = dists[u] + graph[u][v]

    return dists[end]

def to_graph(grid : Grid) -> Graph:
    ''' Converts a grid into a weighted graph representation. '''
    m, n = len(grid), len(grid[0])
    graph = defaultdict(dict)

    for i, j in product(range(m), range(n)):
        for nr, nc in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
            if 0 <= nr < m and 0 <= nc < n:
                graph[(i, j)][(nr, nc)] = grid[nr][nc]
    
    return graph

def repeat(grid : Grid) -> Grid:
    ''' Copy a grid with all its grid cells incremented. '''
    m, n = len(grid), len(grid[0])
    new_grid = deepcopy(grid)

    for i, j in product(range(m), range(n)):
        new_grid[i][j] = (new_grid[i][j] % 9) + 1

    return new_grid

def part1(grid : Grid) -> int:
    ''' Solve part 1 '''
    m, n = len(grid), len(grid[0])
    return dijkstra(to_graph(grid), (0, 0), (m - 1, n - 1))

def part2(grid : Grid) -> int:
    ''' Solve part 2, this is super slow (around 15 seconds) '''
    m = len(grid)

    top_grids = [grid]
    for _ in range(4):
        top_grids.append(repeat(top_grids[-1]))

    top_row = top_grids[0]
    for j in range(m):
        top_row[j].extend(sum([top_grids[i][j] for i in range(1, 5)], []))

    entire_grid = [top_row]
    for _ in range(4):
        entire_grid.append(repeat(entire_grid[-1]))

    entire_grid = sum(entire_grid, [])
    return part1(entire_grid)

with open('day15.txt') as f:
    lines = [line.rstrip('\n') for line in f.readlines()]
    lines = [list(map(int, row)) for row in lines]
    print(part1(lines))
    print(part2(lines))