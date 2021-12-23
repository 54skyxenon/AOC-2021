from typing import List, Tuple, Set
from functools import reduce

Grid = List[List[str]]

def all_good(grid : Grid) -> bool:
    ''' Have all amphipods moved into their intended halls '''
    grid_done = [
        '#############',
        '#...........#',
        '###A#B#C#D###',
        '  #A#B#C#D#',
        '  #########'
    ]

    return grid == grid_done

example_grid = [
    '#############',
    '#...........#',
    '###B#C#B#D###',
    '  #A#D#C#A#',
    '  #########'
]

def flatten(grid : Grid) -> str:
    ''' Flatten a grid into just a string (to be hashed). '''
    return ''.join(row for row in grid)

def set_grid(from_i : int, from_j : int, i : int, j : int, val : str, grid : Grid) -> Grid:
    ''' Assign a value to a specific cell of a grid and return a new grid from that. '''
    new_grid = [list(row) for row in grid]
    new_grid[from_i][from_j] = '.'
    new_grid[i][j] = val
    return [''.join(row) for row in new_grid]

def pretty_print(grid : Grid) -> None:
    print(*grid, sep='\n')
    print()

def part1(grid : Grid) -> int:
    ''' Solve part 1 '''
    least_energy = float('inf')
    energy_of_type = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
    
    def DFS(grid : Grid, energy : int, seen : Set[str]) -> None:
        if all_good(grid):
            nonlocal least_energy
            least_energy = min(least_energy, energy)
            print(least_energy)
            return

        ## all amphipods that are not in the right place
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

        for type, r, c in sorted(amphipods):
            def try_move(energy_gain : int, nr : int, nc : int) -> None:
                after_move = set_grid(r, c, nr, nc, type, grid)
                if flatten(after_move) not in seen:
                    seen.add(flatten(after_move))
                    DFS(after_move, energy + energy_gain, seen)
                    seen.remove(flatten(after_move))

            ## move amphipods on first row left or right, or into a hall if it matches theirs
            if r == 1:
                if type == 'A' and c in {2, 4}:
                    if grid[1][3] == '.':
                        if grid[2][3] + grid[3][3] == '..':
                            try_move(3 * energy_of_type[type], 3, 3)
                        if grid[2][3] + grid[3][3] == '.A':
                            try_move(2 * energy_of_type[type], 2, 3)
                
                if type == 'B' and c in {4, 6}:
                    if grid[1][5] == '.':
                        if grid[2][5] + grid[3][5] == '..':
                            try_move(3 * energy_of_type[type], 3, 5)
                        if grid[2][5] + grid[3][5] == '.B':
                            try_move(2 * energy_of_type[type], 2, 5)
                
                if type == 'C' and c in {6, 8}:
                    if grid[1][7] == '.':
                        if grid[2][7] + grid[3][7] == '..':
                            try_move(3 * energy_of_type[type], 3, 7)
                        if grid[2][7] + grid[3][7] == '.C':
                            try_move(2 * energy_of_type[type], 2, 7)
                
                if type == 'D' and c in {8, 10}:
                    if grid[1][9] == '.':
                        if grid[2][9] + grid[3][9] == '..':
                            try_move(3 * energy_of_type[type], 3, 9)
                        if grid[2][9] + grid[3][9] == '.D':
                            try_move(2 * energy_of_type[type], 2, 9)
                
                for nr, nc in [(r, c + 1), (r, c - 1)]:
                    if nc not in {3, 5, 7, 9} and 0 <= nr < len(grid) and 0 <= nc < len(grid[nr]) and grid[nr][nc] == '.':
                        try_move(energy_of_type[type], nr, nc)

                for nr, nc in [(r, c + 2), (r, c - 2)]:
                    if nc not in {3, 5, 7, 9} and 0 <= nr < len(grid) and 0 <= nc < len(grid[nr]):
                        if grid[nr][nc] == grid[nr][(c + nc) // 2] == '.':
                            try_move(2 * energy_of_type[type], nr, nc)

            # need to try moving out of second row
            elif r == 2:
                if grid[r - 1][c] == '.':
                    if grid[r - 1][c - 1] == '.':
                        try_move(2 * energy_of_type[type], r - 1, c - 1)
                    if grid[r - 1][c + 1] == '.':
                        try_move(2 * energy_of_type[type], r - 1, c + 1)

            # need to try moving out of third row
            elif r == 3:
                if grid[r - 1][c] == '.':
                    try_move(energy_of_type[type], r - 1, c)
    
    DFS(grid, 0, set([flatten(grid)]))
    return least_energy

with open('input/day23.txt') as f:
    grid = [line.rstrip('\n') for line in f.readlines()]
    print(part1(grid))