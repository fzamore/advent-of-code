def getBoardCell(board, x, y):
    if x < 0 or y < 0 or x > 4 or y > 4:
        return None
    return board[x * 5 + y]

def findBoardCellForGuess(board, n):
    for x in range(0, 5):
        for y in range(0, 5):
            cell = getBoardCell(board, x, y)
            if cell and cell['n'] == n:
                return cell
    return None

def isBoardWinner(board):
    for x in range(0, 5):
        for y in range(0, 5):
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    winner = True
                    for i in range(0, 5):
                        cell = getBoardCell(board, x + i * dx, y + i * dy)
                        if not cell or cell['v'] == 0:
                            winner = False
                    if winner:
                        return True

    return False

def part1():
    f = open('day4.txt')
    lines = f.readlines()
    f.close()

    guesses = [int(x) for x in lines[0][:-1].split(',')]
    boards = []

    i = 2
    while i < len(lines):
        board = []
        for x in range(0, 5):
            row = lines[i + x].split()
            for n in row:
                board.append({
                    'n': int(n),
                    'v': 0,
                })
        boards.append(board)
        i += 6

    for guess in guesses:
        for board in boards:
            cell = findBoardCellForGuess(board, guess)
            if cell:
                cell['v'] = 1
                if isBoardWinner(board):
                    score = guess * sum([x['n'] for x in board if x['v'] == 0])
                    print(guesses)
                    print(board)
                    print(guess, score)
                    return

def part2():
    f = open('day4.txt')
    lines = f.readlines()
    f.close()

    guesses = [int(x) for x in lines[0][:-1].split(',')]
    boards = []

    i = 2
    while i < len(lines):
        board = []
        for x in range(0, 5):
            row = lines[i + x].split()
            for n in row:
                board.append({
                    'n': int(n),
                    'v': 0,
                })
        boards.append(board)
        i += 6

    winners = []
    for guess in guesses:
        for board in boards:
            if isBoardWinner(board):
                continue
            cell = findBoardCellForGuess(board, guess)
            if cell:
                cell['v'] = 1
                if isBoardWinner(board):
                    score = guess * sum([x['n'] for x in board if x['v'] == 0])
                    winners.append(score)

    print(winners[len(winners) - 1])

part2()
