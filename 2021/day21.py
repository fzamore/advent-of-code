import functools

# input: rollData: (rollNum, rollValue), playerData(position, score)
# return: (player1WinCount, player2WinCount)
@functools.cache
def rollQuantumDie(player, rollData, player1Data, player2Data):
    rollNum, rollValue = rollData

    # increment position with each die roll (position is zero-indexed)
    position, score = player1Data if player == 1 else player2Data
    position = (position + rollValue) % 10

    if rollNum == 2:
        # increment score at the end of the turn
        score += position + 1
        if score >= 21:
            # we have a winner
            return (1, 0) if player == 1 else (0, 1)

    if player == 1:
        player1Data = (position, score)
        player2Data = player2Data
    else:
        player1Data = player1Data
        player2Data = (position, score)

    if rollNum == 2:
        # switch players if this is the last roll of the turn
        player = 1 if player == 2 else 2

    rollNum = (rollNum + 1) % 3

    roll1Result = rollQuantumDie(player, (rollNum, 1), player1Data, player2Data)
    roll2Result = rollQuantumDie(player, (rollNum, 2), player1Data, player2Data)
    roll3Result = rollQuantumDie(player, (rollNum, 3), player1Data, player2Data)

    return (
        roll1Result[0] + roll2Result[0] + roll3Result[0],
        roll1Result[1] + roll2Result[1] + roll3Result[1],
    )

def part1():
    positions = {}
    with open('day21.txt') as f:
        line = f.readline()
        values = line.split()
        positions[int(values[1])] = int(values[4]) - 1

        line = f.readline()
        values = line.split()
        positions[int(values[1])] = int(values[4]) - 1

    print(positions)

    die = 100
    spaces = 10
    roll = die
    scores = {1: 0, 2: 0}
    playerTurn = 1
    count = 0
    while True:
        advance = 0
        for _ in range(3):
            roll = roll % die + 1
            count += 1
            advance += roll
        positions[playerTurn] = (positions[playerTurn] + advance) % spaces
        scores[playerTurn] += positions[playerTurn] + 1
        print(playerTurn, roll, count, advance, positions[playerTurn], scores[playerTurn])
        if scores[1] >= 1000 or scores[2] >= 1000:
            break

        playerTurn = 1 if playerTurn == 2 else 2

    assert scores[playerTurn] >= 1000, 'bad end state: %s' % scores
    losingScore = scores[1 if playerTurn == 2 else 2]
    print(losingScore, count)
    print(count * losingScore)

def part2():
    positions = {}
    with open('day21.txt') as f:
        line = f.readline()
        values = line.split()
        positions[int(values[1])] = int(values[4]) - 1

        line = f.readline()
        values = line.split()
        positions[int(values[1])] = int(values[4]) - 1

    # positions are zero-indexed
    print(positions)
    print()

    # input: rollData: (rollNum, rollValue), playerData(position, score)
    # return: (player1WinCount, player2WinCount)
    result1 = rollQuantumDie(1, (0, 1), (positions[1], 0), (positions[2], 0))
    result2 = rollQuantumDie(1, (0, 2), (positions[1], 0), (positions[2], 0))
    result3 = rollQuantumDie(1, (0, 3), (positions[1], 0), (positions[2], 0))

    result = (
        result1[0] + result2[0] + result3[0],
        result1[1] + result2[1] + result3[1],
    )

    print(result)
    print(result[0] if result[0] > result[1] else result[1])

part2()
