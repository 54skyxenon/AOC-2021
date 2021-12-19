from typing import List
from collections import Counter

def invert(bit : str) -> str:
	''' Returns the inversion of a bit. '''
	return '1' if bit == '0' else '0'

def get_gamma(binary_nums : List[str]) -> List[str]:
	''' Returns the gamma from the given list of binary numbers, as a list of characters for flexibility. '''
	bit_length = len(binary_nums[0])

	gamma = []
	for i in range(bit_length):
		bit_counter = Counter(num[i] for num in binary_nums)
		if bit_counter['0'] > bit_counter['1']:
			gamma.append('0')
		else:
			gamma.append('1')
		
	return gamma

def get_epsilon(binary_nums : List[str]) -> List[str]:
	''' An epsilon is just a gamma, but inverted. '''
	return list(map(invert, get_gamma(binary_nums)))

def make_decimal_of(binary_digits : List[str]) -> int:
	''' Convert a list of binary digits to its decimal representation. '''
	return int(''.join(binary_digits), 2)

def part1(binary_nums : List[str]) -> int:
	''' Solve part 1. '''
	gamma = make_decimal_of(get_gamma(binary_nums))
	epsilon = make_decimal_of(get_epsilon(binary_nums))
	return gamma * epsilon

def part2(binary_nums : List[str]) -> int:
	''' Solve part 2. '''
	bit_length = len(binary_nums[0])
	binary_nums_oxygen = binary_nums[:]
	binary_nums_co2 = binary_nums[:]

	oxygen_bit_index = co2_bit_index = 0

	while len(binary_nums_oxygen) > 1:
		gamma = get_gamma(binary_nums_oxygen)
		binary_nums_oxygen = list(filter(lambda num: num[oxygen_bit_index] == gamma[oxygen_bit_index], binary_nums_oxygen))
		oxygen_bit_index = (oxygen_bit_index + 1) % bit_length
	
	while len(binary_nums_co2) > 1:
		epsilon = get_epsilon(binary_nums_co2)
		binary_nums_co2 = list(filter(lambda num: num[co2_bit_index] == epsilon[co2_bit_index], binary_nums_co2))
		co2_bit_index = (co2_bit_index + 1) % bit_length

	gen_rating = make_decimal_of(binary_nums_oxygen.pop())
	scrubber_rating = make_decimal_of(binary_nums_co2.pop())
	return gen_rating * scrubber_rating

with open('input/day03.txt') as f:
	lines = [line.rstrip('\n') for line in f.readlines()]
	print(part1(lines))
	print(part2(lines))