from itertools import product
from typing import List
from copy import deepcopy

Grid = List[List[int]]

def step(grid : Grid) -> int:
    ''' Simulate energy gain step and report number of flashes achieved. '''
    m, n = len(grid), len(grid[0])

    for i, j in product(range(m), range(n)):
        grid[i][j] += 1

    has_flashed = True
    flashed = set()
    while has_flashed:
        has_flashed = False
        
        for i, j in product(range(m), range(n)):
            if grid[i][j] >= 10 and (i, j) not in flashed:
                has_flashed = True
                flashed.add((i, j))

                for ni, nj in [ # cardinal directions
                                (i + 1, j), (i - 1, j), (i, j - 1), (i, j + 1),
                                # diagonals
                                (i + 1, j + 1), (i - 1, j - 1), (i + 1, j - 1), (i - 1, j + 1)]:
                    if 0 <= ni < m and 0 <= nj < n:
                        grid[ni][nj] += 1

    for i, j in product(range(m), range(n)):
        if grid[i][j] >= 10:
            grid[i][j] = 0
    
    return len(flashed)

def part1(grid : Grid) -> int:
    ''' Solve part 1 '''
    return sum(step(grid) for _ in range(100))

def part2(grid : Grid) -> int:
    ''' Solve part 2 '''
    step_num = 1
    while step(grid) != 100:
        step_num += 1

    return step_num

with open('day11.txt') as f:
    lines = [line.rstrip('\n') for line in f.readlines()]
    lines = [list(map(int, list(line))) for line in lines]
    print(part1(deepcopy(lines)))
    print(part2(deepcopy(lines)))