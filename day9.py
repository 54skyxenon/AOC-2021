from collections import Counter
from functools import reduce
from itertools import product
from typing import List, Tuple

Point = Tuple[int, int]
Grid = List[List[int]]

class DSU:
    ''' Union find class. '''
    def __init__(self, m : int, n : int) -> None:
        ''' Constructor for union find initially making every point's representative itself. '''
        self.rep = dict((pt, pt) for pt in product(range(m), range(n)))

    def find(self, x : Point) -> Point:
        ''' Find the representative of the given point (its low point). '''
        if self.rep[x] != x:
            self.rep[x] = self.find(self.rep[x])
        return self.rep[x]

    def union(self, x : Point, y : Point) -> None:
        ''' Union together the representatives of two points in a basin to make them connected. '''
        xr, yr = self.find(x), self.find(y)
        self.rep[xr] = self.rep[yr]

def part1(grid : Grid) -> int:
    ''' Solve part 1 '''
    low_points = []
    m, n = len(grid), len(grid[0])

    for r, c in product(range(m), range(n)):
        nei_heights = []
        for nr, nc in [(r + 1, c), (r, c + 1), (r - 1, c), (r, c - 1)]:
            if 0 <= nr < m and 0 <= nc < n:
                nei_heights.append(grid[nr][nc])
        
        if grid[r][c] < min(nei_heights):
            low_points.append(grid[r][c] + 1)

    return sum(low_points)

def part2(grid : Grid) -> int:
    ''' Solve part 2 '''
    m, n = len(grid), len(grid[0])
    uf = DSU(m, n)

    for r, c in product(range(m), range(n)):
        if grid[r][c] < 9:
            for nr, nc in [(r + 1, c), (r, c + 1), (r - 1, c), (r, c - 1)]:
                if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] < grid[r][c]:
                    uf.union((r, c), (nr, nc))

    basin_size = Counter()
    for r, c in product(range(m), range(n)):
        if grid[r][c] < 9:
            basin_size[uf.find((r, c))] += 1

    largest_three = sorted(basin_size.values())[-3:]
    return reduce(lambda a, b: a * b, largest_three, 1)

with open('day9.txt') as f:
    lines = [line.rstrip('\n') for line in f.readlines()]
    lines = [list(map(int, list(line))) for line in lines]
    print(part1(lines))
    print(part2(lines))

example_input = [
    [2, 1, 9, 9, 9, 4, 3, 2, 1, 0], 
    [3, 9, 8, 7, 8, 9, 4, 9, 2, 1], 
    [9, 8, 5, 6, 7, 8, 9, 8, 9, 2], 
    [8, 7, 6, 7, 8, 9, 6, 7, 8, 9], 
    [9, 8, 9, 9, 9, 6, 5, 6, 7, 8]
]
assert part1(example_input) == 15
assert part2(example_input) == 1134