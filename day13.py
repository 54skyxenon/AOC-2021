from typing import List, Tuple

Grid = List[List[str]]
Point = Tuple[int, int]

def pretty_print(grid : Grid) -> None:
    ''' Debug print a grid. '''
    for row in grid:
        print(''.join(row))

def merge_dots(dot_a : str, dot_b : str) -> str:
    ''' Return what dot is the result of folding two together. '''
    if dot_a == '#' or dot_b == '#':
        return '#'
    return '.'

def make_paper_grid(dots : List[Point]) -> Grid:
    ''' Make the starting grid from the given dots. '''
    y_bound = max(y for _x, y in dots)
    x_bound = max(x for x, _y in dots)

    grid = [['.'] * (x_bound + 1) for _ in range(y_bound + 1)]
    for x, y in dots:
        grid[y][x] = '#'

    return grid

def fold_x(grid : Grid, column : int) -> Grid:
    ''' Fold the grid left vertically and return a new grid. '''
    m, n = len(grid), len(grid[0])

    for fold_column in range(column + 1, n):
        for fold_row in range(m):
            grid[fold_row][column - (fold_column - column)] = merge_dots(grid[fold_row][fold_column], grid[fold_row][column - (fold_column - column)])
    
    return [row[:column] for row in grid]

def fold_y(grid : Grid, row : int) -> Grid:
    ''' Fold the grid up horizontally and return a new grid. '''
    m, n = len(grid), len(grid[0])
    
    for fold_row in range(row + 1, m):
        for fold_column in range(n):
            grid[row - (fold_row - row)][fold_column] = merge_dots(grid[row - (fold_row - row)][fold_column], grid[fold_row][fold_column])

    return grid[:row]

def apply_fold(grid : Grid, insn : str) -> Grid:
    ''' Parses a fold instruction and applies it to a grid. '''
    dir, posn = insn[11:].split('=')
    if dir == 'x':
        return fold_x(grid, int(posn))
    else:
        return fold_y(grid, int(posn))

def part1(dots : List[Point], insns : List[str]) -> int:
    ''' Solve part 1 '''
    grid = make_paper_grid(dots)
    grid = apply_fold(grid, insns[0])
    return sum(sum(dot == '#' for dot in row) for row in grid)

def part2(dots : List[Point], insns : List[str]) -> None:
    ''' Solve part 2 '''
    grid = make_paper_grid(dots)
    for insn in insns:
        grid = apply_fold(grid, insn)
    pretty_print(grid)

with open('input/day13.txt') as f:
    lines = [line.rstrip('\n') for line in f.readlines()]

    dots_read = False
    dots, insns = [], []
    for line in lines:
        if line == '':
            dots_read = True
        elif not dots_read:
            dots.append(tuple(map(int, line.split(','))))
        else:
            insns.append(line)

    print(part1(dots, insns))
    part2(dots, insns)