import z3
from typing import List

digits = [z3.BitVec(f'd_{i}', 64) for i in range(14)]
z3_zero, z3_one = z3.BitVecVal(0, 64), z3.BitVecVal(1, 64)

def get_constraints(insns : List[str]) -> z3.Optimize:
    ''' Add constraints after processing each instructions into a Z3 constraint solver (cheating).
        Referenced u/roboputin: https://www.reddit.com/r/adventofcode/comments/rnejv5/comment/hpshymr ''' 
    constraints = z3.Optimize()
    registers = {'w': z3_zero, 'x': z3_zero, 'y': z3_zero, 'z': z3_zero}
    digit_input = digits[::-1]
    
    for d in digits:
        constraints.add(1 <= d)
        constraints.add(d <= 9)
    
    for i, insn in enumerate(insns):
        tokens = insn.split()
        operator = tokens[0]

        a = tokens[1]
        if operator == 'inp':
            registers[a] = digit_input.pop()
            continue

        b = registers[tokens[2]] if tokens[2] in registers else z3.BitVecVal(int(tokens[2]), 64)
        var_uid = z3.BitVec(f'v_{i}', 64)

        if operator == 'add':
            constraints.add(var_uid == registers[a] + b)
        elif operator == 'mul':
            constraints.add(var_uid == registers[a] * b)
        elif operator == 'div':
            constraints.add(var_uid == registers[a] / b)
        elif operator == 'mod':
            constraints.add(var_uid == registers[a] % b)
        elif operator == 'eql':
            constraints.add(var_uid == z3.If(registers[a] == b, z3_one, z3_zero))

        registers[a] = var_uid

    ## the last value of z must be 0
    constraints.add(registers['z'] == z3_zero)
    return constraints

def get_optimal(insns : List[str], direction : str) -> int:
    ''' Get the optimal answer in either extreme. '''
    solver = get_constraints(insns)
    digit_sum = sum((10 ** i) * d for i, d in enumerate(digits[::-1]))

    if direction == 'max':
        solver.maximize(digit_sum)
    else:
        solver.minimize(digit_sum)
    
    ## solve the constraints
    solver.check()

    ## get the digit mappings from model
    m = solver.model()
    return int(''.join(str(m[d]) for d in digits))

def part1(insns : List[str]) -> int:
    ''' Solve part 1 '''
    return get_optimal(insns, 'max')

def part2(insns : List[str]) -> int:
    ''' Solve part 2 '''
    return get_optimal(insns, 'min')

with open('input/day24.txt') as f:
    lines = [line.rstrip('\n') for line in f.readlines()]
    print(part1(lines))
    print(part2(lines))