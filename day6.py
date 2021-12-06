from collections import Counter
from typing import List

def part1(timers : List[int], days=80) -> int:
    ''' Solve part 1 '''
    fish_at_time = Counter(timers)

    for _ in range(days):
        new_fish_at_time = Counter()
        
        for timer_val in fish_at_time:
            if timer_val == 0:
                new_fish_at_time[8] += fish_at_time[timer_val]
                new_fish_at_time[6] += fish_at_time[timer_val]
            else: # timer_val > 0
                new_fish_at_time[timer_val - 1] += fish_at_time[timer_val]

        fish_at_time = new_fish_at_time

    return sum(fish_at_time.values())

def part2(timers : List[int]) -> int:
    ''' Solve part 2 '''
    return part1(timers, days=256)

with open('day6.txt') as f:
    lines = f.readlines()[0].rstrip('\n')
    nums = list(map(int, lines.split(',')))
    print(part1(nums))
    print(part2(nums))

example_input = [3, 4, 3, 1, 2]
assert part1(example_input) == 5934
assert part2(example_input) == 26984457539