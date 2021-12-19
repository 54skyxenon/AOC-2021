from typing import List

def summation(x : int) -> int:
    ''' Closed form formula for summation. '''
    return (x * (x + 1)) // 2

def part1(xs : List[int]) -> int:
    ''' Solve part 1 '''
    left, right = min(xs), max(xs)
    return min(sum(abs(x - i) for x in xs) for i in range(left, right + 1))

def part2(xs : List[int]) -> int:
    ''' Solve part 2 '''
    left, right = min(xs), max(xs)
    return min(sum(summation(abs(x - i)) for x in xs) for i in range(left, right + 1))

with open('input/day07.txt') as f:
    lines = list(map(int, f.readlines()[0].rstrip('\n').split(',')))
    print(part1(lines))
    print(part2(lines))

example_input = [16,1,2,0,4,2,7,1,2,14]
assert part1(example_input) == 37
assert part2(example_input) == 168