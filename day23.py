from typing import List, Set, Dict
from collections import defaultdict
from heapdict import heapdict

import sys
sys.setrecursionlimit(100000)

Grid = List[List[str]]
Graph = Dict[str, Dict[str, int]]

ENERGY_OF_TYPE = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

def flatten(grid : Grid) -> str:
    ''' Flatten a grid into just a string (to be hashed). '''
    return ''.join(row for row in grid)

def set_grid(from_i : int, from_j : int, i : int, j : int, val : str, grid : Grid) -> Grid:
    ''' Assign a value to a specific cell of a grid and return a new grid from that. '''
    new_grid = [list(row) for row in grid]
    new_grid[from_i][from_j] = '.'
    new_grid[i][j] = val
    return [''.join(row) for row in new_grid]

def dijkstra(graph : Graph, start : str, end : str) -> int:
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

    nodes_in_Q = set()
    for u in graph:
        nodes_in_Q.add(u)

    while Q:
        # extract min
        u, dists[u] = Q.popitem()
        nodes_in_Q.remove(u)

        # consider outneighbors
        for v in graph[u]:
            if v in nodes_in_Q:
                dists[v] = lookups[v]
                if dists[v] > dists[u] + graph[u][v]:
                    Q[v] = dists[u] + graph[u][v]
                    lookups[v] = dists[u] + graph[u][v]

    return dists[end]

def part1(grid : Grid) -> int:
    ''' Solve part 1 '''
    graph = defaultdict(dict)
    
    def DFS(grid : Grid, seen : Set[str]) -> None:
        ''' Simulate all possible next states from an amphipod move. '''
        ## get all amphipods that are not in the right place
        amphipods = []
        for r in range(len(grid)):
            for c in range(len(grid[r])):
                if grid[r][c] == 'A':
                    if (r, c) != (3, 3) and not ((r, c) == (2, 3) and grid[3][3] == 'A'):
                        amphipods.append(('A', r, c))
                elif grid[r][c] == 'B':
                    if (r, c) != (3, 5) and not ((r, c) == (2, 5) and grid[3][5] == 'B'):
                        amphipods.append(('B', r, c))
                elif grid[r][c] == 'C':
                    if (r, c) != (3, 7) and not ((r, c) == (2, 7) and grid[3][7] == 'C'):
                        amphipods.append(('C', r, c))
                elif grid[r][c] == 'D':
                    if (r, c) != (3, 9) and not ((r, c) == (2, 9) and grid[3][9] == 'D'):
                        amphipods.append(('D', r, c))

        for type, r, c in amphipods:
            def try_move(cost : int, nr : int, nc : int) -> None:
                ''' Try a valid move and add it as an edge in a weighted graph of states. '''
                after_move = set_grid(r, c, nr, nc, type, grid)
                graph[flatten(grid)][flatten(after_move)] = cost
                graph[flatten(after_move)][flatten(grid)] = cost

                if flatten(after_move) not in seen:
                    seen.add(flatten(after_move))
                    DFS(after_move, seen)

            ## move amphipods on first row left or right, or into a hall if it matches theirs
            if r == 1:
                if type == 'A' and c in {2, 4}:
                    if grid[1][3] == '.':
                        if grid[2][3] + grid[3][3] == '..':
                            try_move(ENERGY_OF_TYPE[type] * 3, 3, 3)
                        if grid[2][3] + grid[3][3] == '.A':
                            try_move(ENERGY_OF_TYPE[type] * 2, 2, 3)
                
                if type == 'B' and c in {4, 6}:
                    if grid[1][5] == '.':
                        if grid[2][5] + grid[3][5] == '..':
                            try_move(ENERGY_OF_TYPE[type] * 3, 3, 5)
                        if grid[2][5] + grid[3][5] == '.B':
                            try_move(ENERGY_OF_TYPE[type] * 2, 2, 5)
                
                if type == 'C' and c in {6, 8}:
                    if grid[1][7] == '.':
                        if grid[2][7] + grid[3][7] == '..':
                            try_move(ENERGY_OF_TYPE[type] * 3, 3, 7)
                        if grid[2][7] + grid[3][7] == '.C':
                            try_move(ENERGY_OF_TYPE[type] * 2, 2, 7)
                
                if type == 'D' and c in {8, 10}:
                    if grid[1][9] == '.':
                        if grid[2][9] + grid[3][9] == '..':
                            try_move(ENERGY_OF_TYPE[type] * 3, 3, 9)
                        if grid[2][9] + grid[3][9] == '.D':
                            try_move(ENERGY_OF_TYPE[type] * 2, 2, 9)
                
                for nr, nc in [(r, c + 1), (r, c - 1)]:
                    if nc not in {3, 5, 7, 9} and 0 <= nr < len(grid) and 0 <= nc < len(grid[nr]) and grid[nr][nc] == '.':
                        try_move(ENERGY_OF_TYPE[type], nr, nc)

                for nr, nc in [(r, c + 2), (r, c - 2)]:
                    if nc not in {3, 5, 7, 9} and 0 <= nr < len(grid) and 0 <= nc < len(grid[nr]):
                        if grid[nr][nc] == grid[nr][(c + nc) // 2] == '.':
                            try_move(ENERGY_OF_TYPE[type] * 2, nr, nc)

            ## need to try moving out of second row
            elif r == 2:
                if grid[r - 1][c] == '.':
                    if grid[r - 1][c - 1] == '.':
                        try_move(ENERGY_OF_TYPE[type] * 2, r - 1, c - 1)
                    if grid[r - 1][c + 1] == '.':
                        try_move(ENERGY_OF_TYPE[type] * 2, r - 1, c + 1)

            ## need to try moving out of third row
            elif r == 3:
                if grid[r - 1][c] == '.':
                    try_move(ENERGY_OF_TYPE[type], r - 1, c)
    
    DFS(grid, set([flatten(grid)]))
    grid_done = [
        '#############',
        '#...........#',
        '###A#B#C#D###',
        '  #A#B#C#D#  ',
        '  #########  '
    ]

    return dijkstra(graph, flatten(grid), flatten(grid_done))

def part2(grid : Grid) -> int:
    ''' Solve part 1 '''
    grid.insert(3, '  #D#C#B#A#  ')
    grid.insert(4, '  #D#B#A#C#  ')
    graph = defaultdict(dict)
    
    def DFS(grid : Grid, seen : Set[str]) -> None:
        ''' Simulate all possible next states from an amphipod move. '''

        '''
        #############
        #...........#
        ###B#C#B#D###
          #D#C#B#A#
          #D#B#A#C#
          #A#D#C#A#
          #########
        '''

        ## get all amphipods that are not in the right place
        amphipods = []
        for r in range(len(grid)):
            for c in range(len(grid[r])):
                if grid[r][c] == 'A':
                    if (r, c) != (5, 3) and\
                    not ((r, c) == (4, 3) and grid[5][3] == 'A') and\
                    not ((r, c) == (3, 3) and grid[4][3] + grid[5][3] == 'AA') and\
                    not ((r, c) == (2, 3) and grid[3][3] + grid[4][3] + grid[5][3] == 'AAA'):
                        amphipods.append(('A', r, c))
                elif grid[r][c] == 'B':
                    if (r, c) != (5, 5) and\
                    not ((r, c) == (4, 5) and grid[5][5] == 'B') and\
                    not ((r, c) == (3, 5) and grid[4][5] + grid[5][5] == 'BB') and\
                    not ((r, c) == (2, 5) and grid[3][5] + grid[4][5] + grid[5][5] == 'BBB'):
                        amphipods.append(('B', r, c))
                elif grid[r][c] == 'C':
                    if (r, c) != (5, 7) and\
                    not ((r, c) == (4, 7) and grid[5][7] == 'C') and\
                    not ((r, c) == (3, 7) and grid[4][7] + grid[5][7] == 'CC') and\
                    not ((r, c) == (2, 7) and grid[3][7] + grid[4][7] + grid[5][7] == 'CCC'):
                        amphipods.append(('C', r, c))
                elif grid[r][c] == 'D':
                    if (r, c) != (5, 9) and\
                    not ((r, c) == (4, 9) and grid[5][9] == 'D') and\
                    not ((r, c) == (3, 9) and grid[4][9] + grid[5][9] == 'DD') and\
                    not ((r, c) == (2, 9) and grid[3][9] + grid[4][9] + grid[5][9] == 'DDD'):
                        amphipods.append(('D', r, c))

        for type, r, c in amphipods:
            def try_move(cost : int, nr : int, nc : int) -> None:
                ''' Try a valid move and add it as an edge in a weighted graph of states. '''
                after_move = set_grid(r, c, nr, nc, type, grid)
                graph[flatten(grid)][flatten(after_move)] = cost
                graph[flatten(after_move)][flatten(grid)] = cost

                if flatten(after_move) not in seen:
                    seen.add(flatten(after_move))
                    DFS(after_move, seen)

            ## move amphipods on first row left or right, or into a hall if it matches theirs
            if r == 1:
                if type == 'A' and c in {2, 4}:
                    if grid[1][3] == '.':
                        if grid[2][3] + grid[3][3] + grid[4][3] + grid[5][3] == '....':
                            try_move(5 * ENERGY_OF_TYPE[type], 5, 3)
                        if grid[2][3] + grid[3][3] + grid[4][3] + grid[5][3] == '...A':
                            try_move(4 * ENERGY_OF_TYPE[type], 4, 3)
                        if grid[2][3] + grid[3][3] + grid[4][3] + grid[5][3] == '..AA':
                            try_move(3 * ENERGY_OF_TYPE[type], 3, 3)
                        if grid[2][3] + grid[3][3] + grid[4][3] + grid[5][3] == '.AAA':
                            try_move(2 * ENERGY_OF_TYPE[type], 2, 3)
                
                if type == 'B' and c in {4, 6}:
                    if grid[1][5] == '.':
                        if grid[2][5] + grid[3][5] + grid[4][5] + grid[5][5] == '....':
                            try_move(5 * ENERGY_OF_TYPE[type], 5, 5)
                        if grid[2][5] + grid[3][5] + grid[4][5] + grid[5][5] == '...B':
                            try_move(4 * ENERGY_OF_TYPE[type], 4, 5)
                        if grid[2][5] + grid[3][5] + grid[4][5] + grid[5][5] == '..BB':
                            try_move(3 * ENERGY_OF_TYPE[type], 3, 5)
                        if grid[2][5] + grid[3][5] + grid[4][5] + grid[5][5] == '.BBB':
                            try_move(2 * ENERGY_OF_TYPE[type], 2, 5)

                if type == 'C' and c in {6, 8}:
                    if grid[1][7] == '.':
                        if grid[2][7] + grid[3][7] + grid[4][7] + grid[5][7] == '....':
                            try_move(5 * ENERGY_OF_TYPE[type], 5, 7)
                        if grid[2][7] + grid[3][7] + grid[4][7] + grid[5][7] == '...C':
                            try_move(4 * ENERGY_OF_TYPE[type], 4, 7)
                        if grid[2][7] + grid[3][7] + grid[4][7] + grid[5][7] == '..CC':
                            try_move(3 * ENERGY_OF_TYPE[type], 3, 7)
                        if grid[2][7] + grid[3][7] + grid[4][7] + grid[5][7] == '.CCC':
                            try_move(2 * ENERGY_OF_TYPE[type], 2, 7)

                if type == 'D' and c in {8, 10}:
                    if grid[1][9] == '.':
                        if grid[2][9] + grid[3][9] + grid[4][9] + grid[5][9] == '....':
                            try_move(5 * ENERGY_OF_TYPE[type], 5, 9)
                        if grid[2][9] + grid[3][9] + grid[4][9] + grid[5][9] == '...D':
                            try_move(4 * ENERGY_OF_TYPE[type], 4, 9)
                        if grid[2][9] + grid[3][9] + grid[4][9] + grid[5][9] == '..DD':
                            try_move(3 * ENERGY_OF_TYPE[type], 3, 9)
                        if grid[2][9] + grid[3][9] + grid[4][9] + grid[5][9] == '.DDD':
                            try_move(2 * ENERGY_OF_TYPE[type], 2, 9)
                
                for nr, nc in [(r, c + 1), (r, c - 1)]:
                    if nc not in {3, 5, 7, 9} and 0 <= nr < len(grid) and 0 <= nc < len(grid[nr]) and grid[nr][nc] == '.':
                        try_move(ENERGY_OF_TYPE[type], nr, nc)

                for nr, nc in [(r, c + 2), (r, c - 2)]:
                    if nc not in {3, 5, 7, 9} and 0 <= nr < len(grid) and 0 <= nc < len(grid[nr]):
                        if grid[nr][nc] == grid[nr][(c + nc) // 2] == '.':
                            try_move(2 * ENERGY_OF_TYPE[type], nr, nc)

            ## need to try moving out of second row
            elif r == 2:
                if grid[r - 1][c] == '.':
                    if grid[r - 1][c - 1] == '.':
                        try_move(2 * ENERGY_OF_TYPE[type], r - 1, c - 1)
                    if grid[r - 1][c + 1] == '.':
                        try_move(2 * ENERGY_OF_TYPE[type], r - 1, c + 1)

            ## need to try moving out of third row
            elif r == 3 or r == 4 or r == 5:
                if grid[r - 1][c] == '.':
                    try_move(ENERGY_OF_TYPE[type], r - 1, c)
    
    DFS(grid, set([flatten(grid)]))
    grid_done = [
        '#############',
        '#...........#',
        '###A#B#C#D###',
        '  #A#B#C#D#  ',
        '  #A#B#C#D#  ',
        '  #A#B#C#D#  ',
        '  #########  '
    ]

    return dijkstra(graph, flatten(grid), flatten(grid_done))

with open('input/day23.txt') as f:
    grid = [line.rstrip('\n').ljust(13) for line in f.readlines()]
    print(part1(grid))
    print(part2(grid))