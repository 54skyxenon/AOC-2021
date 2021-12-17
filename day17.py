def summation(n : int) -> int:
    ''' Closed form summation formula for integers 1..n '''
    return (n * (n + 1)) // 2

def part1(x_start : int, x_end : int, y_start : int, y_end : int) -> int:
    ''' Solve part 1 '''
    ans = 0

    for x in range(x_end + 1):
        # Assuming y_start <= y_end < 0, idk otherwise
        for y in range(y_start, -(y_start - 1) + 1):
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
        # Assuming y_start <= y_end < 0, idk otherwise
        for y in range(y_start, -(y_start - 1) + 1):
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