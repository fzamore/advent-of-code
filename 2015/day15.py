from typing import Optional
from common.ints import ints
from collections import defaultdict
from math import prod

data = open('day15.txt').read().splitlines()

Ingredients = list[list[int]]

def computeScore(ingredients: Ingredients, ratios: list[int]) -> int:
  scores: dict[int, int] = defaultdict(int)
  for ri, ratio in enumerate(ratios):
    for ii in range(len(ingredients)):
      scores[ii] += ratio * ingredients[ri][ii]
  return prod(v if v > 0 else 0 for v in scores.values())

def comupteMaxGeneric(
  ingredients: Ingredients,
  calorieMatch: Optional[int] = None,
  n: int = 100,
) -> int:
  # This method computes the max score for any number of ingredients.
  bound = n - len(ingredients)
  mx = 0
  checks = 0
  # We explode all combinations of ingredients, but leave off one
  # ingredient, because the last ingredient is dependent on all the
  # others. This is still a brute force approach (trying all combinations
  # of ingredients).
  for c in range(pow(bound, len(ingredients) - 1)):
    ratios: list[int] = []
    # Compute the ratios for this iteration. Each ingredient is mapped to
    # a specific range of the iteration number. This is similar to
    # computing a number in a certain base (in our case, the base is the
    # number of ingredients minus 1).
    while len(ratios) < len(ingredients) - 1:
      ratios.append(c % bound)
      c //= bound

    if 0 in ratios or sum(ratios) >= n:
      # Skip cases we know can't be the solution.
      continue

    # Add the last ratio, which is dependent on the others.
    ratios.append(n - sum(ratios))

    # Assume calories is the last entry in each ingredient list.
    if calorieMatch is not None:
      calories = sum([ingredients[x][-1] * ratios[x] for x in range(len(ingredients))])
      if calories != calorieMatch:
        continue

    mx = max(mx, computeScore(ingredients, ratios))
    checks += 1

  print('checks:', checks)
  return mx

def computeMaxFixed(
  ingredients: Ingredients,
  calorieMatch: Optional[int] = None,
  n: int = 100,
) -> int:
  assert len(ingredients) == 4, 'must be four ingredients'
  mx = 0
  # Stupid stupid brute force. Crazy that this works.
  checks = 0
  for i in range(1, n - 2):
    for j in range(1, n - 2):
      for k in range(1, n - 2):
        if i + j + k >= n:
          continue
        l = n - i - j - k
        ratios = [i, j, k, l]

        # Assume calories is the last entry in each ingredient list.
        if calorieMatch is not None:
          calories = sum([ingredients[x][-1] * ratios[x] for x in range(len(ingredients))])
          if calories != calorieMatch:
            continue

        mx = max(mx, computeScore(ingredients, ratios))
        checks += 1

  print('checks:', checks)
  return mx

def part1() -> None:
  # Discard ingredient names and refer to them by index.
  ingredients = list(map(ints, data))
  print('ingredients:', len(ingredients))
  for i, values in enumerate(ingredients):
    print(i, values)

  # These two should print the same result.
  print(comupteMaxGeneric(ingredients))
  print(computeMaxFixed(ingredients))

def part2() -> None:
  ingredients = list(map(ints, data))

  # These two should print the same result.
  print(comupteMaxGeneric(ingredients, 500))
  print(computeMaxFixed(ingredients, 500))

part2()
