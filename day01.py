from typing import List

def part1(nums : List[int]) -> int:
	''' Solve part 1. '''
	return sum(nums[i] > nums[i - 1] for i in range(1, len(nums)))

def part2(nums : List[int]) -> int:
	''' Solve part 2. '''
	return sum(sum(nums[i:i+3]) > sum(nums[i-1:i+2]) for i in range(1, len(nums) - 2))

with open('input/day01.txt') as f:
	lines = [int(line.rstrip('\n')) for line in f.readlines()]
	print(part1(lines))
	print(part2(lines))