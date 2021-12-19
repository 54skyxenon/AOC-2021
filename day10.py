from functools import reduce
from statistics import median
from typing import List

PAIRING = {')': '(', '}': '{', ']': '[', '>': '<'}
PAIRING_INV = dict(kv[::-1] for kv in PAIRING.items())
SCORE_P1 = {')': 3, ']': 57, '}': 1197, '>': 25137}
SCORE_P2 = {')': 1, ']': 2, '}': 3, '>': 4}

def part1(chunks : List[str]) -> int:
    ''' Solve part 1 '''
    error = 0
    for chunk in chunks:
        stack = []
        for c in chunk:
            if c not in PAIRING:
                stack.append(c)
            elif not stack or PAIRING[c] != stack[-1]:
                error += SCORE_P1[c]
                break
            else:
                stack.pop()

    return error

def part2(chunks : List[str]) -> int:
    ''' Solve part 2 '''
    incomplete = []

    for chunk in chunks:
        malformed = False
        stack = []
        for c in chunk:
            if c not in PAIRING:
                stack.append(c)
            elif not stack or PAIRING[c] != stack[-1]:
                malformed = True
                break
            else:
                stack.pop()

        if not malformed:
            incomplete.append(stack)
    
    completion_scores = []

    for stack in incomplete:
        completion_scores.append(reduce(
            lambda total, paren: 5 * total + SCORE_P2[PAIRING_INV[paren]],\
            stack[::-1], 0))

    return median(completion_scores)

with open('input/day10.txt') as f:
    lines = [line.rstrip('\n') for line in f.readlines()]
    print(part1(lines))
    print(part2(lines))