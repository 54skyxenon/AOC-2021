from typing import List, Tuple
from collections import defaultdict
from heapdict import heapdict

Grid = List[List[str]]
Edge = Tuple[int, str]

ENERGY_OF_TYPE = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
HALLWAY_INDEX = {'A': 3, 'B': 5, 'C': 7, 'D': 9}

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

def get_neis(grid : Grid, height : int) -> List[Edge]:
    ''' Simulate all possible next states from an amphipod move on a grid with a given hallway height. '''
    neis = []

    ## get all amphipods that are not in the right place
    amphipods = []
    for r in range(1, len(grid) - 1):
        for c in range(1, len(grid[0]) - 1):
            if grid[r][c] in HALLWAY_INDEX:
                amphipod = grid[r][c]
                hall = HALLWAY_INDEX[amphipod]
                if r == 1 or not (c == hall and all(grid[rr][hall] == amphipod for rr in range(r, height + 1))):
                    amphipods.append((amphipod, r, c))
    
    for amphipod, r, c in amphipods:
        def try_move(cost : int, nr : int, nc : int) -> Edge:
            ''' Try a valid move and add it as an edge in a weighted graph of states. '''
            after_move = set_grid(r, c, nr, nc, amphipod, grid)
            return (cost, flatten(after_move))
        
        ## try moving amphipods on first row into a hallway
        if r == 1:
            hall = HALLWAY_INDEX[amphipod]
            if (c < hall and all(grid[r][cc] == '.' for cc in range(c + 1, hall + 1))) or\
                (c > hall and all(grid[r][cc] == '.' for cc in range(c - 1, hall - 1, -1))):
                hallway_state = ''.join(grid[rr][hall] for rr in range(2, height + 1))
                acceptable_states = {'.' * (height - 1)}
                for i in range(1, height - 1):
                    acceptable_states.add('.' * i + amphipod * (height - 1 - i))

                if hallway_state in acceptable_states:
                    moves = abs(hall - c) + hallway_state.count('.')
                    neis.append(try_move(
                        moves * ENERGY_OF_TYPE[amphipod],
                        hallway_state.count('.') + 1,
                        hall))
        
        ## need to try moving amphipods out of hallway rows
        elif 2 <= r <= height and all(grid[rr][c] == '.' for rr in range(1, r)):
            for cc in range(c - 1, 0, -1):
                if grid[1][cc] != '.':
                    break
                if cc not in HALLWAY_INDEX.values() and grid[1][cc] == '.':
                    neis.append(try_move((r - 1 + abs(cc - c)) * ENERGY_OF_TYPE[amphipod], 1, cc))
            
            for cc in range(c + 1, len(grid[1])):
                if grid[1][cc] != '.':
                    break
                if cc not in HALLWAY_INDEX.values() and grid[1][cc] == '.':
                    neis.append(try_move((r - 1 + abs(cc - c)) * ENERGY_OF_TYPE[amphipod], 1, cc))
    
    return neis

def dijkstra(height : int, start : str, end : str) -> int:
    ''' Dijkstra's algorithm without a graph, just finding neighbors until we reach the end with least cost! '''
    dists = defaultdict(lambda: float('inf'))
    dists[start] = 0
    
    # Let Q be a new heap
    Q = heapdict()
    Q[start] = 0
    visited = set()

    while True:
        # extract min
        u, dists[u] = Q.popitem()
        visited.add(u)
        if u == end:
            return dists[u]
        
        # consider outneighbors
        for cost, v in get_neis(unflatten(u), height):
            if v not in visited:
                if dists[v] > dists[u] + cost:
                    Q[v] = dists[v] = dists[u] + cost

def part1(grid : Grid) -> int:
    ''' Solve part 1 '''
    grid_done = [
        '#############',
        '#...........#',
        '###A#B#C#D###',
        '  #A#B#C#D#  ',
        '  #########  '
    ]
    return dijkstra(3, flatten(grid), flatten(grid_done))

def part2(grid : Grid) -> int:
    ''' Solve part 1 '''
    grid.insert(3, '  #D#C#B#A#  ')
    grid.insert(4, '  #D#B#A#C#  ')
    grid_done = [
        '#############',
        '#...........#',
        '###A#B#C#D###',
        '  #A#B#C#D#  ',
        '  #A#B#C#D#  ',
        '  #A#B#C#D#  ',
        '  #########  '
    ]
    return dijkstra(5, flatten(grid), flatten(grid_done))

with open('input/day23.txt') as f:
    grid = [line.rstrip('\n').ljust(13) for line in f.readlines()]
    print(part1(grid))
    print(part2(grid))