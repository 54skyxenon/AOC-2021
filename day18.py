from functools import reduce
from typing import Iterable, Union, List, Tuple

Expression = Union[Iterable['Expression'], int]
INT_TYPE = type(0)

def magnitude(operand : Expression) -> int:
    ''' Calculate the magnitude of a final sum of snailfish numbers '''
    if type(operand) == INT_TYPE:
        return operand
    else:
        return 3 * magnitude(operand[0]) + 2 * magnitude(operand[1])

def coalesce(element_stack : Tuple[int, int]) -> Expression:
    ''' Recoalesce the operands from stack element info. '''
    stack = []
    for val, depth in element_stack:
        stack.append((val, depth))
        while len(stack) >= 2 and stack[-2][1] == stack[-1][1]:
            curr_val, _ = stack.pop()
            old_val, old_depth = stack.pop()
            stack.append(([old_val, curr_val], old_depth - 1))
    
    return stack[0][0]

def explode(operand : Expression) -> Expression:
    ''' Try exploding a snailfash operand, if applicable. '''
    ## List of elements and their depths
    elements = []
    stack = [(operand, -1)]

    while stack:
        top, depth = stack.pop()
        if type(top) == INT_TYPE:
            elements.append((top, depth))
        else:
            stack.append((top[0], depth + 1))
            stack.append((top[1], depth + 1))
    
    elements.reverse()
    for i in range(len(elements) - 1):
        if elements[i][1] == elements[i + 1][1] == 4:
            left_val, _ = elements.pop(i)
            right_val, _ = elements.pop(i)
            left_half = elements[:i]
            right_half = elements[i:]

            if left_half:
                left_half[-1] = (left_half[-1][0] + left_val, left_half[-1][1])
            if right_half:
                right_half[0] = (right_half[0][0] + right_val, right_half[0][1])

            elements = left_half + [(0, 3)] + right_half
            break

    return coalesce(elements)

def split(operand : Expression) -> Expression:
    ''' Try splitting a snailfash operand, if applicable. '''
    ## List of elements and their depths
    elements = []
    stack = [(operand, -1)]

    while stack:
        top, depth = stack.pop()
        if type(top) == INT_TYPE:
            elements.append((top, depth))
        else:
            stack.append((top[0], depth + 1))
            stack.append((top[1], depth + 1))
    
    elements.reverse()
    for i in range(len(elements)):
        if elements[i][0] >= 10:
            val, depth = elements.pop(i)
            left_val, right_val = val // 2, val - (val // 2)
            elements.insert(i, (right_val, depth + 1))
            elements.insert(i, (left_val, depth + 1))
            break

    return coalesce(elements)

def simplify(operand : Expression) -> Expression:
    ''' Add two snailfish numbers in an expression pair. '''
    was_reduced = True
    while was_reduced:
        was_reduced = False

        was_exploded = True
        while was_exploded:
            was_exploded = False
            new_operand_explode = explode(operand)
            if new_operand_explode != operand:
                was_reduced = was_exploded = True
                operand = new_operand_explode

        new_operand_split = split(operand)
        if new_operand_split != operand:
            operand = new_operand_split
            was_reduced = True

    return operand

def part1(exps : List[Expression]) -> int:
    ''' Solve part 1 '''
    final_sum = reduce(lambda x, y: simplify([x, y]), exps)
    return magnitude(final_sum)

def part2(exps : List[Expression]) -> int:
    ''' Solve part 2 '''
    n = len(exps)
    ans = 0
    for i in range(n):
        for j in range(i + 1, n):
            ans = max(ans, magnitude(simplify([exps[i], exps[j]])))

    return ans

with open('day18.txt') as f:
    lines = [eval(line.rstrip('\n')) for line in f.readlines()]
    print(part1(lines))
    print(part2(lines))

assert magnitude([[1,2],[[3,4],5]]) == 143
assert magnitude([[[[0,7],4],[[7,8],[6,0]]],[8,1]]) == 1384
assert magnitude([[[[1,1],[2,2]],[3,3]],[4,4]]) == 445
assert magnitude([[[[3,0],[5,3]],[4,4]],[5,5]]) == 791
assert magnitude([[[[5,0],[7,4]],[5,5]],[6,6]]) == 1137
assert magnitude([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]) == 3488

assert explode([[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]) == [[[[0,7],4],[7,[[8,4],9]]],[1,1]]
assert explode([[[[0,7],4],[7,[[8,4],9]]],[1,1]]) == [[[[0,7],4],[15,[0,13]]],[1,1]]
assert explode([[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]) == [[[[0,7],4],[[7,8],[6,0]]],[8,1]]
assert explode([[[[[9,8],1],2],3],4]) == [[[[0,9],2],3],4]
assert explode([7,[6,[5,[4,[3,2]]]]]) == [7,[6,[5,[7,0]]]]
assert explode([[6,[5,[4,[3,2]]]],1]) == [[6,[5,[7,0]]],3]
assert explode([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]) == [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]
assert explode([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]) == [[3,[2,[8,0]]],[9,[5,[7,0]]]]

assert split([[[[0,7],4],[15,[0,13]]],[1,1]]) == [[[[0,7],4],[[7,8],[0,13]]],[1,1]]
assert split([[[[0,7],4],[[7,8],[0,13]]],[1,1]]) == [[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]

assert simplify([[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]) == [[[[0,7],4],[[7,8],[6,0]]],[8,1]]
assert simplify([[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]], [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]) == [[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]