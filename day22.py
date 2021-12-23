from typing import List, Tuple, Set
from functools import reduce

Cube = Tuple[str, int, int, int, int, int, int]

def part1(given_cubes : List[Cube]) -> int:
    ''' Solve part 1 '''
    cube = [[[False] * 101 for _ in range(101)] for _ in range(101)]

    for state, x1, x2, y1, y2, z1, z2 in given_cubes:
        for x in range(max(x1 + 50, 0), min(x2 + 51, 101)):
            for y in range(max(y1 + 50, 0), min(y2 + 51, 101)):
                for z in range(max(z1 + 50, 0), min(z2 + 51, 101)):
                    cube[x][y][z] = (state == 'on')

    return sum(sum(sum(row) for row in plane) for plane in cube)

def part2(given_cubes : List[Cube]) -> int:
    ''' Solve part 2, stolen + refactored from u/liviuc because I have compilers HW to finish:
        https://www.reddit.com/r/adventofcode/comments/rlxhmg/comment/hpjpvmt '''
    
    def combine(other_cubes : Set[Cube], cube : Cube) -> Set[Cube]:
        ''' Combines the given cube with a set of other cubes, calculating the necessary geometrical splits. '''
        _state, x1, x2, y1, y2, z1, z2 = cube
        to_del = set()
        to_add = set([cube])

        ## visit all other cubes and compute splits
        for other_state, other_x1, other_x2, other_y1, other_y2, other_z1, other_z2 in other_cubes:
            ## no intersection between this other cube and the cube we're trying to combine
            if other_x1 > x2 or other_x2 < x1 or other_y1 > y2 or other_y2 < y1 or other_z1 > z2 or other_z2 < z1:
                continue

            ## the common length on X
            new_x1, new_x2 = max(other_x1, x1), min(other_x2, x2)

            ## the common length on Y
            new_y1, new_y2 = max(other_y1, y1), min(other_y2, y2)

            ## the common length on Z
            new_z1, new_z2 = max(other_z1, z1), min(other_z2, z2)

            ## this cube no longer exists after splitting
            to_del.add((other_state, other_x1, other_x2, other_y1, other_y2, other_z1, other_z2))

            ## chop off what's outside common X
            if other_x1 < new_x1:
                to_add.add((other_state, other_x1, new_x1 - 1, other_y1, other_y2, other_z1, other_z2))

            if new_x2 < other_x2:
                to_add.add((other_state, new_x2 + 1, other_x2, other_y1, other_y2, other_z1, other_z2))

            ## chop off what's outside common Y
            if other_y1 < new_y1:
                to_add.add((other_state, new_x1, new_x2, other_y1, new_y1 - 1, other_z1, other_z2))

            if new_y2 < other_y2:
                to_add.add((other_state, new_x1, new_x2, new_y2 + 1, other_y2, other_z1, other_z2))

            ## chop off what's outside common Z
            if other_z1 < new_z1:
                to_add.add((other_state, new_x1, new_x2, new_y1, new_y2, other_z1, new_z1 - 1))

            if new_z2 < other_z2:
                to_add.add((other_state, new_x1, new_x2, new_y1, new_y2, new_z2 + 1, other_z2))

        return (other_cubes | to_add) - to_del

    net_volume = 0
    for state, x1, x2, y1, y2, z1, z2 in reduce(combine, given_cubes, set()):
        if state == 'on':
            width = x2 - x1 + 1
            height = y2 - y1 + 1
            depth = z2 - z1 + 1
            net_volume += width * height * depth

    return net_volume

with open('input/day22.txt') as f:
    lines = [line.rstrip('\n') for line in f.readlines()]

    cubes = []
    for line in lines:
        state = line[:3].strip()
        x, y, z = line[3:].strip().split(',')
        cubes.append((state, 
            *map(int, x[2:].split('..')), 
            *map(int, y[2:].split('..')), 
            *map(int, z[2:].split('..'))))

    print(part1(cubes))
    print(part2(cubes))