from functools import lru_cache
from itertools import product
from typing import Tuple

def incr_dice(dice : int) -> int:
    ''' Increment the next roll of a deterministic dice. '''
    return dice % 100 + 1

def add(a : Tuple[int, int], b : Tuple[int, int]) -> Tuple[int, int]:
    ''' Add two tuples element-wise. '''
    return [a[0] + b[0], a[1] + b[1]]

def move_player(posn : int, x : int) -> int:
    ''' Returns the new position of the player after moving x spots. '''
    return (posn + x - 1) % 10 + 1

def part1(p1_posn : int, p2_posn : int) -> int:
    ''' Solve part 1 '''
    dice = 1
    rolls = p1_score = p2_score = 0

    while p1_score < 1000 and p2_score < 1000:
        p1_movement = 0
        for _ in range(3):
            p1_movement += dice
            rolls += 1
            dice = incr_dice(dice)

        p1_posn = move_player(p1_posn, p1_movement)
        p1_score += p1_posn

        if p1_score >= 1000:
            break
        
        p2_movement = 0
        for _ in range(3):
            p2_movement += dice
            rolls += 1
            dice = incr_dice(dice)

        p2_posn = move_player(p2_posn, p2_movement)
        p2_score += p2_posn

    return rolls * min(p1_score, p2_score)

def part2(p1_posn : int, p2_posn : int) -> int:
    ''' Solve part 2 '''
    move_combinations = list(product(range(1, 4), range(1, 4), range(1, 4)))

    @lru_cache(None)
    def dp(p1_posn : int, p2_posn : int, p1_score : int, p2_score : int, p1_move : bool) -> Tuple[int, int]:
        ''' Tuple indicating how many times [p1 won, p2 won] given both player positions, scores, and whose turn it is. '''
        if p1_score >= 21:
            return [1, 0]

        if p2_score >= 21:
            return [0, 1]

        wins = [0, 0]

        if p1_move:
            for moves in move_combinations:
                new_p1_posn = move_player(p1_posn, sum(moves))
                wins = add(wins, dp(new_p1_posn, p2_posn, p1_score + new_p1_posn, p2_score, False))
        else:
            for moves in move_combinations:
                new_p2_posn = move_player(p2_posn, sum(moves))
                wins = add(wins, dp(p1_posn, new_p2_posn, p1_score, p2_score + new_p2_posn, True))

        return [wins[0], wins[1]]

    return max(dp(p1_posn, p2_posn, 0, 0, True))

with open('input/day21.txt') as f:
    lines = [line.rstrip('\n') for line in f.readlines()]
    p1_start = int(lines[0][-2:])
    p2_start = int(lines[1][-2:])
    print(part1(p1_start, p2_start))
    print(part2(p1_start, p2_start))

assert part1(4, 8) == 739785
assert part2(4, 8) == 444356092776315