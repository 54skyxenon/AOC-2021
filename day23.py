from typing import List, Callable, Tuple
from collections import defaultdict
from heapdict import heapdict

Grid = List[List[str]]
Edge = Tuple[int, str]

ENERGY_OF_TYPE = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

def flatten(grid : Grid) -> str:
    ''' Flatten a grid into just a string (to be hashed). '''
    return ''.join(row for row in grid)

def unflatten(grid_str : str) -> Grid:
    ''' Unflatten a grid string back into a 2D grid. '''
    as_grid = []
    for i in range(0, len(grid_str), 13):
        as_grid.append(grid_str[i:i + 13])
    return as_grid

def set_grid(from_i : int, from_j : int, i : int, j : int, val : str, grid : Grid) -> Grid:
    ''' Assign a value to a specific cell of a grid and return a new grid from that. '''
    new_grid = [list(row) for row in grid]
    new_grid[from_i][from_j] = '.'
    new_grid[i][j] = val
    return [''.join(row) for row in new_grid]

def dijkstra(get_neis : Callable[[Grid], List[Edge]], start : str, end : str) -> int:
    ''' Dijkstra's with a heap - O(n log n + m log n) time '''
    dists = defaultdict(lambda: float('inf'))
    dists[start] = 0
    
    # Let Q be a new heap
    Q = heapdict()
    Q[start] = 0
    visited = set()

    while True:
        # extract min
        u, dists[u] = Q.popitem()
        print('at dist =', dists[u])
        visited.add(u)
        if u == end:
            return dists[u]
        
        # consider outneighbors
        for cost, v in get_neis(unflatten(u)):
            if v not in visited:
                if dists[v] > dists[u] + cost:
                    Q[v] = dists[v] = dists[u] + cost

def part1(grid : Grid) -> int:
    ''' Solve part 1 '''
    
    def get_neis_p1(grid : Grid) -> List[Edge]:
        ''' Simulate all possible next states from an amphipod move. '''
        neis = []

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
            def try_move(cost : int, nr : int, nc : int) -> Edge:
                ''' Try a valid move and add it as an edge in a weighted graph of states. '''
                after_move = set_grid(r, c, nr, nc, type, grid)
                return (cost, flatten(after_move))
            
            ## move amphipods on first row left or right, or into a hall if it matches theirs
            if r == 1:
                if type == 'A' and c in {2, 4}:
                    if grid[1][3] == '.':
                        if grid[2][3] + grid[3][3] == '..':
                            neis.append(try_move(ENERGY_OF_TYPE[type] * 3, 3, 3))
                        if grid[2][3] + grid[3][3] == '.A':
                            neis.append(try_move(ENERGY_OF_TYPE[type] * 2, 2, 3))
                
                if type == 'B' and c in {4, 6}:
                    if grid[1][5] == '.':
                        if grid[2][5] + grid[3][5] == '..':
                            neis.append(try_move(ENERGY_OF_TYPE[type] * 3, 3, 5))
                        if grid[2][5] + grid[3][5] == '.B':
                            neis.append(try_move(ENERGY_OF_TYPE[type] * 2, 2, 5))
                
                if type == 'C' and c in {6, 8}:
                    if grid[1][7] == '.':
                        if grid[2][7] + grid[3][7] == '..':
                            neis.append(try_move(ENERGY_OF_TYPE[type] * 3, 3, 7))
                        if grid[2][7] + grid[3][7] == '.C':
                            neis.append(try_move(ENERGY_OF_TYPE[type] * 2, 2, 7))
                
                if type == 'D' and c in {8, 10}:
                    if grid[1][9] == '.':
                        if grid[2][9] + grid[3][9] == '..':
                            neis.append(try_move(ENERGY_OF_TYPE[type] * 3, 3, 9))
                        if grid[2][9] + grid[3][9] == '.D':
                            neis.append(try_move(ENERGY_OF_TYPE[type] * 2, 2, 9))
                
                for nr, nc in [(r, c + 1), (r, c - 1)]:
                    if nc not in {3, 5, 7, 9} and 0 <= nr < len(grid) and 0 <= nc < len(grid[nr]) and grid[nr][nc] == '.':
                        neis.append(try_move(ENERGY_OF_TYPE[type], nr, nc))

                for nr, nc in [(r, c + 2), (r, c - 2)]:
                    if nc not in {3, 5, 7, 9} and 0 <= nr < len(grid) and 0 <= nc < len(grid[nr]):
                        if grid[nr][nc] == grid[nr][(c + nc) // 2] == '.':
                            neis.append(try_move(ENERGY_OF_TYPE[type] * 2, nr, nc))

            ## need to try moving out of second-third rows
            elif r in {2, 3}:
                if all(grid[rr][c] == '.' for rr in range(1, r)):
                    if grid[1][c - 1] == '.':
                        neis.append(try_move(ENERGY_OF_TYPE[type] * r, 1, c - 1))
                    if grid[1][c + 1] == '.':
                        neis.append(try_move(ENERGY_OF_TYPE[type] * r, 1, c + 1))

        return neis
    
    grid_done = [
        '#############',
        '#...........#',
        '###A#B#C#D###',
        '  #A#B#C#D#  ',
        '  #########  '
    ]

    return dijkstra(get_neis_p1, flatten(grid), flatten(grid_done))

def part2(grid : Grid) -> int:
    ''' Solve part 1 '''
    grid.insert(3, '  #D#C#B#A#  ')
    grid.insert(4, '  #D#B#A#C#  ')

    def get_neis_p2(grid : Grid) -> List[Edge]:
        ''' Simulate all possible next states from an amphipod move. '''
        neis = []

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
            def try_move(cost : int, nr : int, nc : int) -> Edge:
                ''' Try a valid move and make a new edge in a weighted graph of states. '''
                after_move = set_grid(r, c, nr, nc, type, grid)
                return (cost, flatten(after_move))

            ## move amphipods on first row left or right, or into a hall if it matches theirs
            if r == 1:
                if type == 'A' and c in {2, 4}:
                    if grid[1][3] == '.':
                        if grid[2][3] + grid[3][3] + grid[4][3] + grid[5][3] == '....':
                            neis.append(try_move(5 * ENERGY_OF_TYPE[type], 5, 3))
                        if grid[2][3] + grid[3][3] + grid[4][3] + grid[5][3] == '...A':
                            neis.append(try_move(4 * ENERGY_OF_TYPE[type], 4, 3))
                        if grid[2][3] + grid[3][3] + grid[4][3] + grid[5][3] == '..AA':
                            neis.append(try_move(3 * ENERGY_OF_TYPE[type], 3, 3))
                        if grid[2][3] + grid[3][3] + grid[4][3] + grid[5][3] == '.AAA':
                            neis.append(try_move(2 * ENERGY_OF_TYPE[type], 2, 3))
                
                if type == 'B' and c in {4, 6}:
                    if grid[1][5] == '.':
                        if grid[2][5] + grid[3][5] + grid[4][5] + grid[5][5] == '....':
                            neis.append(try_move(5 * ENERGY_OF_TYPE[type], 5, 5))
                        if grid[2][5] + grid[3][5] + grid[4][5] + grid[5][5] == '...B':
                            neis.append(try_move(4 * ENERGY_OF_TYPE[type], 4, 5))
                        if grid[2][5] + grid[3][5] + grid[4][5] + grid[5][5] == '..BB':
                            neis.append(try_move(3 * ENERGY_OF_TYPE[type], 3, 5))
                        if grid[2][5] + grid[3][5] + grid[4][5] + grid[5][5] == '.BBB':
                            neis.append(try_move(2 * ENERGY_OF_TYPE[type], 2, 5))

                if type == 'C' and c in {6, 8}:
                    if grid[1][7] == '.':
                        if grid[2][7] + grid[3][7] + grid[4][7] + grid[5][7] == '....':
                            neis.append(try_move(5 * ENERGY_OF_TYPE[type], 5, 7))
                        if grid[2][7] + grid[3][7] + grid[4][7] + grid[5][7] == '...C':
                            neis.append(try_move(4 * ENERGY_OF_TYPE[type], 4, 7))
                        if grid[2][7] + grid[3][7] + grid[4][7] + grid[5][7] == '..CC':
                            neis.append(try_move(3 * ENERGY_OF_TYPE[type], 3, 7))
                        if grid[2][7] + grid[3][7] + grid[4][7] + grid[5][7] == '.CCC':
                            neis.append(try_move(2 * ENERGY_OF_TYPE[type], 2, 7))

                if type == 'D' and c in {8, 10}:
                    if grid[1][9] == '.':
                        if grid[2][9] + grid[3][9] + grid[4][9] + grid[5][9] == '....':
                            neis.append(try_move(5 * ENERGY_OF_TYPE[type], 5, 9))
                        if grid[2][9] + grid[3][9] + grid[4][9] + grid[5][9] == '...D':
                            neis.append(try_move(4 * ENERGY_OF_TYPE[type], 4, 9))
                        if grid[2][9] + grid[3][9] + grid[4][9] + grid[5][9] == '..DD':
                            neis.append(try_move(3 * ENERGY_OF_TYPE[type], 3, 9))
                        if grid[2][9] + grid[3][9] + grid[4][9] + grid[5][9] == '.DDD':
                            neis.append(try_move(2 * ENERGY_OF_TYPE[type], 2, 9))
                
                for nr, nc in [(r, c + 1), (r, c - 1)]:
                    if nc not in {3, 5, 7, 9} and 0 <= nr < len(grid) and 0 <= nc < len(grid[nr]) and grid[nr][nc] == '.':
                        neis.append(try_move(ENERGY_OF_TYPE[type], nr, nc))

                for nr, nc in [(r, c + 2), (r, c - 2)]:
                    if nc not in {3, 5, 7, 9} and 0 <= nr < len(grid) and 0 <= nc < len(grid[nr]) and grid[nr][nc] == grid[nr][(c + nc) // 2] == '.':
                        neis.append(try_move(2 * ENERGY_OF_TYPE[type], nr, nc))

            ## need to try moving out of second-fifth rows
            elif r in {2, 3, 4, 5} and all(grid[rr][c] == '.' for rr in range(1, r)):
                if grid[1][c - 1] == '.':
                    neis.append(try_move(r * ENERGY_OF_TYPE[type], 1, c - 1))
                if grid[1][c + 1] == '.':
                    neis.append(try_move(r * ENERGY_OF_TYPE[type], 1, c + 1))

        return neis
    
    grid_done = [
        '#############',
        '#...........#',
        '###A#B#C#D###',
        '  #A#B#C#D#  ',
        '  #A#B#C#D#  ',
        '  #A#B#C#D#  ',
        '  #########  '
    ]

    return dijkstra(get_neis_p2, flatten(grid), flatten(grid_done))

with open('input/day23.txt') as f:
    grid = [line.rstrip('\n').ljust(13) for line in f.readlines()]
    print(part1(grid))
    print(part2(grid))