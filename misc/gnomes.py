# Interview question. You have a queue of gnomes. Each gnome is wearing
# either a red hat or a blue hat. Each gnome cannot see their own hat, but
# can see the hats of all the gnomes in front of them. The arbiter starts
# at the back of the line and asks each gnome what color their own hat is.
# All gnomes can hear all guesses, but cannot otherwise communicate. What
# strategy guarantees the highest number of correct guesses?
#
# Answer: By keeping track of polarity (i.e., for each gnome, keep track
# of whether they can see an even number of red hats). The optimal
# strategy is that each gnome except the first one (at the back of the
# line) will guess correctly.

from typing import Sequence

# Front of the queue is index 0.
_data_ = 'rrbbrbrbbbrrbbrbbrbbr'

# ------ Begin user code

class Gnome:
  # Passed an ordered sequence of what this gnome can see.
  def __init__(self, seq: str):
    print('gnome init:', seq)
    # Polarity is true if there are an even number of reds.
    self.polarity = self._computePolarity(seq)
    self.guesses: list[str] = []

  def _computePolarity(self, seq: Sequence[str]) -> bool:
    return seq.count('r') % 2 == 0

  def guessColor(self) -> str:
    # If the polarity of the guesses hasn't changed, then it's blue.
    return 'b' if self._computePolarity(self.guesses) == self.polarity else 'r'

  def colorAnnounced(self, i: int, color: str) -> None:
    # As long as the guesses are made from back to the front, we don't
    # care about maintaining the order of guesses, nor do we care which
    # gnome made which guess.
    self.guesses.append(color)

# ------ End user code

def execute(data: str) -> None:
  n = len(data)
  print('data:', n, data)
  gnomes = [Gnome(data[:i]) for i in range(n)]

  correct = 0
  # Iterate from back to front.
  for i in range(n - 1, -1, -1):
    color = gnomes[i].guessColor()
    if color == data[i]:
      print('correct:', i, color)
      correct += 1
    else:
      print('incorrect:', i, color)

    for gnome in gnomes:
      gnome.colorAnnounced(i, color)

  print('correct: %d, incorrect: %d' % (correct, n - correct))

  for gnome in gnomes:
    assert len(gnome.guesses) == n, 'bad number of guesses'

execute(_data_)
