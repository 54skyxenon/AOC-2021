from typing import List, Tuple
from itertools import product

Grid = List[List[str]]
Point = Tuple[int, int]

def move_down(grid : Grid, i : int, j : int) -> Point:
    ''' Return new location after trying to move a sea cucumber down. '''
    m = len(grid)
    new_i, new_j = (i + 1) % m, j
    if grid[new_i][new_j] == '.':
        return (new_i, new_j)
    else:
        return (i, j)

def move_right(grid : Grid, i : int, j : int) -> Point:
    ''' Return new location after trying to move a sea cucumber right. '''
    n = len(grid[0])
    new_i, new_j = i, (j + 1) % n
    if grid[new_i][new_j] == '.':
        return (new_i, new_j)
    else:
        return (i, j)

def part1(grid : Grid) -> int:
    ''' Solve part 1 '''
    m, n = len(lines), len(lines[0])

    steps = 0
    has_moved = True
    while has_moved:
        has_moved = False
        prev_rights = set()
        rights = set()

        for i, j in product(range(m), range(n)):
            if grid[i][j] == '>':
                prev_rights.add((i, j))
                if move_right(grid, i, j) != (i, j):
                    has_moved = True
                rights.add(move_right(grid, i, j))

        for i, j in prev_rights:
            grid[i][j] = '.'

        for i, j in rights:
            grid[i][j] = '>'

        prev_downs = set()
        downs = set()

        for i, j in product(range(m), range(n)):
            if grid[i][j] == 'v':
                prev_downs.add((i, j))
                if move_down(grid, i, j) != (i, j):
                    has_moved = True
                downs.add(move_down(grid, i, j))

        for i, j in prev_downs:
            grid[i][j] = '.'

        for i, j in downs:
            grid[i][j] = 'v'

        steps += has_moved

    return steps + 1

def part2() -> str:
    ''' Solve part 2 '''
    return 'Click on \'Remotely Start The Sleigh Again\'!'

with open('input/day25.txt') as f:
    lines = [list(line.rstrip('\n')) for line in f.readlines()]
    print(part1(lines))
    print(part2())