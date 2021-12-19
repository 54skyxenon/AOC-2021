from typing import List, Tuple
from itertools import product, combinations
from collections import Counter, deque

Point3D = Tuple[int, int, int]

def rotate(beacon : Point3D, rx : int, ry : int, rz : int) -> Point3D:
    ''' Stolen from https://github.com/DannyCamenisch '''
    x, y, z = beacon
    for _ in range(rx):
        x, y, z = x, z, -y
    for _ in range(ry):
        x, y, z = z, y, -x
    for _ in range(rz):
        x, y, z = y, -x, z
    return (x, y, z)

def subtract(a : Point3D, b : Point3D) -> Point3D:
    ''' Subtract two 3d points element-wise. '''
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])

def add(a : Point3D, b : Point3D) -> Point3D:
    ''' Add two 3d points element-wise. '''
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])

def manhattan(a : Point3D, b : Point3D) -> Point3D:
    ''' Manhattan distance of two 3D points. '''
    return sum(abs(a_elt - b_elt) for a_elt, b_elt in zip(a, b))

def solve(beacons : List[List[Tuple[int, int, int]]]) -> int:
    ''' Solve part 1 and part 2, code reuse or doing them separately takes too long '''
    points = set()
    abs_posn = {0: (0, 0, 0)}
    worklist = deque([(0, beacons[0])])
    while worklist:
        beacon_id, a_beacs = worklist.popleft()
        for a_beac in a_beacs:
            points.add(add(abs_posn[beacon_id], a_beac))

        for beacon_num, old_b_beacs in enumerate(beacons):
            if beacon_num not in abs_posn:
                for i, j, k in product(range(4), range(4), range(4)):
                    b_beacs = [rotate(t, i, j, k) for t in old_b_beacs]

                    ds = Counter()
                    for b_beac in b_beacs:
                        for a_beac in a_beacs:
                            ds[tuple(subtract(a_beac, b_beac))] += 1

                    if ds.most_common()[0][1] >= 12:
                        d = Counter(ds).most_common()[0][0]
                        abs_posn[beacon_num] = add(abs_posn[beacon_id], d)
                        worklist.append((beacon_num, b_beacs))

    part1 = len(points)
    part2 = max(manhattan(a, b) for a, b in combinations(abs_posn.values(), r=2))
    print(part1)
    print(part2)

with open('day19.txt') as f:
    lines = [line.rstrip('\n') for line in f.readlines()]

    beacons = []
    for i, line in enumerate(lines):
        if line.startswith('---'):
            beacons.append([])
        elif len(line) > 0:
            beacons[-1].append(tuple(map(int, line.split(','))))
    
    solve(beacons)