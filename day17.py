from typing import Tuple

def summation(n : int) -> int:
    ''' Closed form summation formula for integers 1..n '''
    return (n * (n + 1)) // 2

def get_ys(width : int, y_start : int, y_end : int) -> Tuple[int, int]:
    ''' Get the range of y-coordinate we might need to search through. '''
    if y_start >= 0:
        return (0, y_end + 1)
    elif y_end >= 0: # y_start < 0 <= y_end
        return (y_start, 2 * (y_end - y_start + width))
    else: # y_start <= y_end < 0
        return (y_start, 2 * (y_end - y_start + width))

def part1(x_start : int, x_end : int, y_start : int, y_end : int) -> int:
    ''' Solve part 1 '''
    ans = 0

    for x in range(x_end + 1):
        for y in range(*get_ys(x_end - x_start + 1, y_start, y_end)):
            vx, vy = x, y
            curr_x = curr_y = 0
            while vy >= 0 or curr_y >= y_start:
                if x_start <= curr_x <= x_end and y_start <= curr_y <= y_end:
                    ans = max(ans, summation(y))
                curr_x, curr_y = curr_x + vx, curr_y + vy
                vx, vy = max(0, vx - 1), vy - 1
    
    return ans

def part2(x_start : int, x_end : int, y_start : int, y_end : int) -> int:
    ''' Solve part 2 '''
    ans = set()

    for x in range(x_end + 1):
        for y in range(*get_ys(x_end - x_start + 1, y_start, y_end)):
            vx, vy = x, y
            curr_x = curr_y = 0
            while vy >= 0 or curr_y >= y_start:
                if x_start <= curr_x <= x_end and y_start <= curr_y <= y_end:
                    ans.add((x, y))
                curr_x, curr_y = curr_x + vx, curr_y + vy
                vx, vy = max(0, vx - 1), vy - 1
    
    return len(ans)

with open('day17.txt') as f:
    vars = [line.rstrip('\n') for line in f.readlines()][0]
    vars = vars.replace('target area: x=', '').replace('..', ',').replace(' y=', '')
    print(part1(*map(int, vars.split(','))))
    print(part2(*map(int, vars.split(','))))

assert part1(20, 30, -10, -5) == 45
assert part2(20, 30, -10, -5) == 112