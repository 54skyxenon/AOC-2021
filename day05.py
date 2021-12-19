from typing import List, Tuple

def parse_vents(vents : List[str]) -> List[Tuple[int, int, int, int]]:
    ''' Return vents as four element tuples. '''
    coordinates = []

    for vent in vents:
        vent = vent.replace(' -> ', ',')
        coordinates.append(tuple(map(int, vent.split(','))))
    
    return coordinates

def vent_sum(vents : List[str], count_diagonals=False) -> int:
    ''' Returns the number of points where at least two vents overlap. '''
    coordinates = parse_vents(vents)
    
    max_x = max_y = 0
    for x1, y1, x2, y2 in coordinates:
        max_x = max(max_x, x1, x2)
        max_y = max(max_y, y1, y2)

    field = [[0] * (max_x + 1) for _ in range(max_y + 1)]

    for x1, y1, x2, y2 in coordinates:
        if x1 == x2:
            if y2 < y1:
                y1, y2 = y2, y1
            for i in range(y1, y2 + 1):
                field[i][x1] += 1
        elif y1 == y2:
            if x2 < x1:
                x1, x2 = x2, x1
            for j in range(x1, x2 + 1):
                field[y1][j] += 1
        elif count_diagonals and abs(x1 - x2) == abs(y1 - y2):
            xs = list(range(x1, x2 - 1, -1) if x2 < x1 else range(x1, x2 + 1))
            ys = list(range(y1, y2 - 1, -1) if y2 < y1 else range(y1, y2 + 1))
            for y, x in zip(ys, xs):
                field[y][x] += 1

    return sum(sum(col >= 2 for col in row) for row in field)

def part1(vents : List[str]) -> int:
    ''' Solve part 1 '''
    return vent_sum(vents)

def part2(vents : List[str]) -> int:
    ''' Solve part 2 '''
    return vent_sum(vents, count_diagonals=True)

with open('input/day05.txt') as f:
    lines = [line.rstrip('\n') for line in f.readlines() if line != '\n']
    print(part1(lines))
    print(part2(lines))