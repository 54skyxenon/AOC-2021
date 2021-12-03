def part1(moves):
	x = y = 0
	for move in moves:
		direction, magnitude = move.split()
		magnitude = int(magnitude)

		if direction == 'forward':
			x += magnitude
		elif direction == 'down':
			y += magnitude
		elif direction == 'up':
			y = max(0, y - magnitude)
	
	return x * y

def part2(moves):
	x = y = aim = 0
	for move in moves:
		direction, magnitude = move.split()
		magnitude = int(magnitude)

		if direction == 'forward':
			x += magnitude
			y += aim * magnitude
		elif direction == 'down':
			aim += magnitude
		elif direction == 'up':
			aim -= magnitude
	
	return x * y

with open('day2.txt') as f:
	lines = [line.rstrip('\n') for line in f.readlines()]
	print(part1(lines))
	print(part2(lines))