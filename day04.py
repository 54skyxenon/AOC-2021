from typing import List, Optional

def has_won(board_marked : List[List[bool]], r=5, c=5) -> bool:
    ''' Has the given board (according to its markings) won? '''
    for row in range(r):
        if all(board_marked[row][col] for col in range(c)):
            return True

    for col in range(c):
        if all(board_marked[row][col] for row in range(r)):
            return True

    return False

def process_move(move : str, board : List[List[str]], board_markings : List[List[bool]], r=5, c=5) -> Optional[int]:
    ''' Updates a board's state after a move, returns the score if this board wins after the move. '''
    for row in range(r):
        for col in range(c):
            if board[row][col] == move:
                board_markings[row][col] = True
    
    if has_won(board_markings):
        unmarked_sum = 0

        for row in range(r):
            for col in range(c):
                if not board_markings[row][col]:
                    unmarked_sum += int(board[row][col])
        
        return unmarked_sum * int(move)

    return None

def part1(moves : List[str], boards : List[List[List[str]]], r=5, c=5) -> Optional[int]:
    ''' Solve part 1 '''
    board_markings = [[[False] * c for _ in range(r)] for _ in boards]

    for move in moves:
        for board_num, board in enumerate(boards):
            result = process_move(move, board, board_markings[board_num])
            if result is not None:
                return result

def part2(moves : List[str], boards : List[List[List[str]]], r=5, c=5) -> int:
    ''' Solve part 2 '''
    board_markings = [[[False] * c for _ in range(r)] for _ in boards]
    scores = []

    for move in moves:
        boards_not_won = []
        board_markings_not_won = []

        for board_num, board in enumerate(boards):
            result = process_move(move, board, board_markings[board_num])
            if result is not None:
                scores.append(result)
            else:
                boards_not_won.append(board)
                board_markings_not_won.append(board_markings[board_num])

        boards, board_markings = boards_not_won, board_markings_not_won

    return scores[-1]

with open('day4.txt') as f:
    lines = [line.rstrip('\n') for line in f.readlines() if line != '\n']
    moves = lines[0].split(',')

    boards = []
    for i in range(1, len(lines), 5):
        board_here = []
        for j in range(i, i + 5):
            board_here.append(lines[j].split())
        boards.append(board_here)
    
    print(part1(moves, boards))
    print(part2(moves, boards))