from itertools import product
from typing import List

Grid = List[str]

def enhance(algorithm : str, image : Grid, parity : int, parity_matters : bool) -> Grid:
    ''' Create a new enchanced image given an existing image (ignoring infinite borders). '''
    m, n = len(image), len(image[0])
    new_image = [['.' for _ in range(n + 2)] for _ in range(m + 2)]

    def get_cell(i : int, j : int) -> str:
        ''' Get value of cell from old image, guarding against out of bounds.
            If we are on an odd iteration and the 0-index of the algorithm indicates a #, be careful! '''
        if 0 <= i < m and 0 <= j < n:
            return image[i][j]
        elif parity_matters:
            return '.' if parity % 2 == 0 else '#'
        else:
            return '.'

    def map_cell(kernel : Grid) -> str:
        ''' Find new value of cell from 3x3 convolution kernel from algorithm string. '''
        kernel = ''.join(kernel)
        kernel = ''.join(str(int(c == '#')) for c in kernel)
        return algorithm[int(kernel, 2)]

    for i, j in product(range(m + 2), range(n + 2)):
        kernel = [['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']]
        kernel[0][0] = get_cell(i - 2, j - 2)
        kernel[0][1] = get_cell(i - 2, j - 1)
        kernel[0][2] = get_cell(i - 2, j)
        kernel[1][0] = get_cell(i - 1, j - 2)
        kernel[1][1] = get_cell(i - 1, j - 1)
        kernel[1][2] = get_cell(i - 1, j)
        kernel[2][0] = get_cell(i, j - 2)
        kernel[2][1] = get_cell(i, j - 1)
        kernel[2][2] = get_cell(i, j)
        new_image[i][j] = map_cell([''.join(row) for row in kernel])

    return [''.join(row) for row in new_image]

def part1(algorithm : str, image : Grid) -> int:
    ''' Solve part 1 '''
    parity_matters = (algorithm[0] == '#')
    i1 = enhance(algorithm, image, 0, parity_matters)
    i2 = enhance(algorithm, i1, 1, parity_matters)
    return ''.join(i2).count('#')

def part2(algorithm : str, image : Grid) -> int:
    ''' Solve part 2 '''
    parity_matters = (algorithm[0] == '#')
    for i in range(50):
        image = enhance(algorithm, image, i, parity_matters)
    return ''.join(image).count('#')

with open('input/day20.txt') as f:
    lines = [line.rstrip('\n') for line in f.readlines()]
    print(part1(lines[0], lines[2:]))
    print(part2(lines[0], lines[2:]))