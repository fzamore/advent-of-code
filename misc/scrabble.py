from enum import Enum
from typing import Iterable, Iterator
from common.arraygrid import ArrayGrid
from PIL import Image # type: ignore

from common.graphtraversal import dfs

# This algorithm solves the "Hardscrabble" contest in the September 2026
# issue of GAMES Magazine by taking a list of clue answers and target
# scrabble scores as input, and places all the words on a scrabble board
# using a DFS. The input file is given as "<word> <target_score>" lines,
# with across entries listed first and a blank line between across and
# down entries. The included file "scrabble/clue_answers.txt" contains all
# the answers to the actual puzzle (spoiler alert!).
#
# Requires the PIL/Pillow library to display the board: `pip install
# pillow`

class Orientation(Enum):
  HORIZONTAL = 1
  VERTICAL = 2

class TileType(Enum):
  TRIPLE_WORD = 1
  DOUBLE_WORD = 2
  TRIPLE_LETTER = 3
  DOUBLE_LETTER = 4

# Each cell of the board stores a (letter, frozenset[WordPlacement]) tuple
# representing the letter at that cell and the words that contain the
# letter in that cell.
Board = ArrayGrid
Coords = tuple[int, int]
# Each clue answer stores a word, a target score, and an orientation.
Answer =  tuple[str, int, Orientation]
# A placement consists of a length (how long the word is), where it starts, and the orientation.
WordPlacement = tuple[int, Coords, Orientation]
# Each DFS node stores a board and a set of the words remaining.
DfsNode = tuple[Board, frozenset[str]]

BOARD_SIZE = 15
LETTER_IMG_SIZE = 38
BOARD_IMG_OFFSET = 62
BOARD_IMG_SPACING = 7.7
BOARD_IMG_DIVIDER_SIZE = 6
BOARD_IMG_DIVIDER_SPACING = 6.5
BOARD_IMG_CELL_SIZE = 45.8
BOARD_IMG_CELL_OFFSET = 56

def getTileScores() -> dict[Coords, TileType]:
  scores = {
    TileType.TRIPLE_WORD: [
      (0, 0),
      (0, 7),
      (0, 14),
      (7, 0),
      (7, 14),
      (14, 0),
      (14, 7),
      (14, 14)
    ],
    TileType.DOUBLE_WORD: [
      (7, 7),
      (1, 1),
      (2, 2),
      (3, 3),
      (4, 4),
      (13, 1),
      (12, 2),
      (11, 3),
      (10, 4),
      (1, 13),
      (2, 12),
      (3, 11),
      (4, 10),
      (13, 13),
      (12, 12),
      (11, 11),
      (10, 10),
    ],
    TileType.TRIPLE_LETTER: [
      (5, 1),
      (9, 1),
      (1, 5),
      (5, 5),
      (9, 5),
      (13, 5),
      (1, 9),
      (5, 9),
      (9, 9),
      (13, 9),
      (5, 13),
      (9, 13),
    ],
    TileType.DOUBLE_LETTER: [
      (3, 0),
      (11, 0),
      (6, 2),
      (8, 2),
      (0, 3),
      (7, 3),
      (14, 3),
      (2, 6),
      (6, 6),
      (8, 6),
      (12, 6),
      (3, 7),
      (11, 7),
      (3, 14),
      (11, 14),
      (6, 12),
      (8, 12),
      (0, 11),
      (7, 11),
      (14, 11),
      (2, 8),
      (6, 8),
      (8, 8),
      (12, 8),
    ],
  }
  ret = {}
  for type in scores:
    for coords in scores[type]:
      ret[coords] = type
  return ret

def placeWord(board: Board, word: str, start: Coords, orientation: Orientation) -> None:
  dx, dy = (0, 1) if orientation == Orientation.VERTICAL else (1, 0)
  sx, sy = start
  placement = (len(word), start, orientation)
  for i in range(len(word)):
    nx, ny = sx + dx * i, sy + dy * i
    value = board.getValue(nx, ny)
    if value is None:
      placements = frozenset([placement])
    else:
      # There is already a letter in this cell. Add the new placement.
      assert value[0] == word[i], 'overwriting different letter'
      placements = value[1]
      assert len(placements) == 1, 'must be at most 2 placements per cell'
      placements = placements.union([placement])
    board.setValue(nx, ny, (word[i], placements))

def getLetterScores() -> dict[str, int]:
  invScores = {
    1: 'aeilnorstu',
    2: 'dg',
    3: 'bcmp',
    4: 'fhvwy',
    5: 'k',
    8: 'jx',
    10: 'qz',
  }
  scores = {}
  for score in invScores:
    for let in invScores[score]:
      scores[let] = score
  assert len(scores) == 26, 'bad score compute'
  return scores

def scoreWord(word: str, start: Coords, orientation: Orientation) -> int:
  letterScores = getLetterScores()
  tileScores = getTileScores()
  startx, starty = start
  dx, dy = (0, 1) if orientation == Orientation.VERTICAL else (1, 0)
  wordMultiplier = 1
  score = 0
  for i in range(len(word)):
    x, y = startx + i * dx, starty + i * dy
    letterScore = letterScores[word[i]]
    match tileScores.get((x, y)):
      case TileType.TRIPLE_WORD:
        wordMultiplier *= 3
      case TileType.DOUBLE_WORD:
        wordMultiplier *= 2
      case TileType.TRIPLE_LETTER:
        letterScore *= 3
      case TileType.DOUBLE_LETTER:
        letterScore *= 2
    assert letterScore > 0, 'bad letter score'
    score += letterScore
  return score *  wordMultiplier

def canPlaceWord(board: Board, word: str, start: Coords, orientation: Orientation) -> bool:
  x, y = start
  dx, dy = (0, 1) if orientation == Orientation.VERTICAL else (1, 0)

  for i in range(len(word)):
    nx, ny = x + i * dx, y + i * dy
    if not board.areCoordsWithinBounds(nx, ny):
      # We've extended beyond the grid.
      return False

    if not board.hasValue(nx, ny):
      # This cell is empty, therefore fine.
      continue

    letter, placements = board.getValue(nx, ny)
    assert 1 <= len(placements) <= 2, 'incorrect number of placements in board'
    if len(placements) == 2:
      return False
    if letter != word[i] or orientation in [p[1][1] for p in placements]:
      # If the letter doesn't match or is part of the word in the same
      # orientation (i.e., overlapping), the word cannot be placed here.
      return False

  return True

def getPossiblePlacements(board: Board, answer: Answer) -> list[WordPlacement]:
  ret = []
  word, target, orientation = answer
  for x, y in board.getAllCoords():
    placement = len(word), (x, y), orientation
    if not canPlaceWord(board, word, (x, y), orientation):
      continue

    score = scoreWord(word, (x, y), orientation)
    if score == target:
      ret.append(placement)
  return ret

def getAnswers() -> list[Answer]:
  ret = []
  orientation = Orientation.HORIZONTAL
  for line in open('scrabble/clue_answers.txt').read().splitlines():
    if line == '':
      orientation = Orientation.VERTICAL
      continue
    word, target = line.split()
    ret.append((word, int(target), orientation))
  return ret

def getBarPositionsFromPlacement(placement: WordPlacement) -> tuple[Coords, Coords]:
  size, (x, y), orientation = placement
  match orientation:
    case Orientation.HORIZONTAL:
      return (
        (x, y),
        (x + size, y),
      )
    case Orientation.VERTICAL:
      return (
        (x, y),
        (x, y + size),
      )
    case _:
      assert False, 'bad orientation'

def getPlacementsFromBoard(board: Board) -> set[WordPlacement]:
  s = set()
  for placements in (v[1] for (_, __, v) in board.getItems() if v is not None):
    s.update(placements)
  return s

# Returns whether this board is rotationally symmetric.
def isRotationallySymmetric(board: Board) -> bool:
  placements = getPlacementsFromBoard(board)
  for size, (x, y), orientation in placements:
    match orientation:
      case Orientation.HORIZONTAL:
        nx, ny = board.getWidth() - 1 - x - (size - 1), board.getHeight() - 1 - y
      case Orientation.VERTICAL:
        nx, ny = board.getWidth() - 1 - x, board.getHeight() - 1 - y - (size - 1)
      case _:
        assert False, 'bad orientation'
    if (size, (nx, ny), orientation) not in placements:
      # We don't have a rotationally symmetric entry.
      return False
  return True

# Returns if the given word has at least one crossing word.
def doesWordHaveCrossingWord(board: Board, placement: WordPlacement) -> bool:
  size, (startx, starty), orientation = placement
  dx, dy = (1, 0) if orientation == Orientation.HORIZONTAL else (0, 1)
  for i in range(size):
    x, y = startx + i * dx, starty + i * dy
    if (value := board.getValue(x, y)) is not None and len(value[1]) > 1:
      return True
  return False

# Returns whether this board could possibly be rotationally symmetric
# (e.g., if more words were added).
def isRotationalSymmetryPossible(board: Board) -> bool:
  bars: set[tuple[tuple[int, int], Orientation]] = set()
  for placement in getPlacementsFromBoard(board):
    _, __, wordOrientation = placement
    barPositions = getBarPositionsFromPlacement(placement)
    bars.update((p, wordOrientation) for p in barPositions)

  for (x, y), wordOrientation in bars:
    match wordOrientation:
      case Orientation.HORIZONTAL:
        obx, oby = board.getWidth() - x, board.getHeight() - 1 - y
      case Orientation.VERTICAL:
        obx, oby = board.getWidth() - 1 - x, board.getHeight() - y
      case _:
        assert False, 'bad orientation'
    if ((obx, oby), wordOrientation) in bars:
      # We have the opposite bar. This cell is rotationally symmetric.
      continue

    if not board.areCoordsWithinBounds(obx, oby) or not board.hasValue(obx, oby):
      # There is no letter here. This cell is possibly rotationally symmetric.
      continue

    _, existingWordPlacements = board.getValue(obx, oby)
    if wordOrientation in [p[1][1] for p in existingWordPlacements]:
      # If there is a value in this cell and its word's orientation
      # matches the word whose bar we are checking, we are overlapping and
      # thus cannot be rotationally symmetric.
      return False

  return True

def displayBoard(board: Board) -> None:
  boardImg = Image.open('scrabble/board.jpg')

  horizBarImg = Image.open('scrabble/0.jpg') \
    .resize((round(BOARD_IMG_DIVIDER_SIZE), round(BOARD_IMG_CELL_SIZE)))
  vertBarImg = Image.open('scrabble/0.jpg') \
    .resize((round(BOARD_IMG_CELL_SIZE), round(BOARD_IMG_DIVIDER_SIZE)))

  # Add letters to board.
  for x, y, value in board.getItems():
    if value is None:
      continue
    letter, _ = value

    assert letter.islower() or letter == '0', 'invalid board value'
    letterImg = Image.open('scrabble/%s.jpg' % letter) \
      .resize((LETTER_IMG_SIZE, LETTER_IMG_SIZE))
    imgx = BOARD_IMG_OFFSET + x * (LETTER_IMG_SIZE + BOARD_IMG_SPACING)
    imgy = BOARD_IMG_OFFSET + y * (LETTER_IMG_SIZE + BOARD_IMG_SPACING)
    boardImg.paste(letterImg, ((round(imgx), round(imgy))))

  # Add bars to board.
  for placement in getPlacementsFromBoard(board):
    _, __, orientation = placement
    barImg = horizBarImg if orientation == Orientation.HORIZONTAL else vertBarImg
    for bx, by in getBarPositionsFromPlacement(placement):
      boardImg.paste(
        barImg,
        ((
          round(BOARD_IMG_CELL_OFFSET + bx * BOARD_IMG_CELL_SIZE),
          round(BOARD_IMG_CELL_OFFSET + by * BOARD_IMG_CELL_SIZE)
        )),
      )

  boardImg.show()

N = 0 # to help with debugging
def getAdjacentDfsNodes(
  answers: Iterable[Answer],
  allWordPlacements: dict[str, list[WordPlacement]],
  board: Board,
  wordsRemaining: frozenset[str],
) -> Iterator[tuple[Board, frozenset[str]]]:
  global N
  if len(wordsRemaining) == 0:
    # We have placed all words. This branch is finished.
    N += 1
    print('DONE', N)
    return

  # Find the best word to place during this iteration.
  fewestPlacements = 10_000
  placements = None
  word = None
  for answer in answers:
    w, _, __ = answer
    if w not in wordsRemaining:
      continue

    p = [e for e in allWordPlacements[w] if canPlaceWord(board, w, e[1], e[2])]
    numPlacements = len(p)
    if numPlacements == 0:
      # Nowhere to place this word. This branch is a dead end.
      return

    if numPlacements < fewestPlacements:
      # We've found a new best candidate.
      fewestPlacements = numPlacements
      word = w
      placements = p

  assert word is not None and placements is not None, 'did not find word to place'

  for _, start, orientation in placements:
    assert canPlaceWord(board, word, start, orientation), 'should have already ensured canPlaceWord'
    nboard = board.copy()
    placeWord(nboard, word, start, orientation)

    if isRotationalSymmetryPossible(nboard):
      # If this board is possibly rotationally symmetric, we keep going.
      yield nboard, wordsRemaining.difference([word])

def solve() -> None:
  board = Board(BOARD_SIZE, BOARD_SIZE)

  answers = getAnswers()

  allWordPlacements = {}
  wordsToPlace = []

  for answer in answers:
    word, _, orientation = answer
    placements = getPossiblePlacements(board, answer)
    allWordPlacements[word] = placements
    assert len(placements) > 0, 'nowhere to put answer: %s' % word
    wordsToPlace.append(word)

  for word in allWordPlacements:
    placements = allWordPlacements[word]
    assert len(placements) > 0, 'did not find placement for word'
    orientation = placements[0][2]
    print(word, orientation, len(placements))
  print()
  print('words to place:', len(wordsToPlace))

  def getAdj(node: DfsNode) -> Iterator[DfsNode]:
    board, wordsRemaining = node
    for result in getAdjacentDfsNodes(answers, allWordPlacements, board, wordsRemaining):
      yield result

  finishedBoards = []
  def visit(node: DfsNode) -> None:
    board, wordsRemaining = node
    if len(wordsRemaining) == 0:
      finishedBoards.append(board)

  dfs((board, frozenset(wordsToPlace)), getAdj, visitNode=visit)

  print()
  print('finished boards:', len(finishedBoards))
  if len(finishedBoards) == 0:
    print('No finished boards found.')
    return

  rotationallySymmetricBoards = [b for b in finishedBoards if isRotationallySymmetric(b)]
  print('finished rotationally symmetric boards:', len(rotationallySymmetricBoards))
  boardsWithAllWordsCrossing = [b for b in rotationallySymmetricBoards if \
    all(doesWordHaveCrossingWord(b, p) for p in getPlacementsFromBoard(b))]
  print('finished rotationally symmetric boards with all words crossing:', len(boardsWithAllWordsCrossing))
  for b in boardsWithAllWordsCrossing:
    displayBoard(b)

  if len(boardsWithAllWordsCrossing) == 0:
    print('No complete rotationally symmetric boards found. Displaying first finished board.')
    displayBoard(finishedBoards[0])

if __name__ ==  '__main__':
  solve()
