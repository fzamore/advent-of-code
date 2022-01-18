from common.io import readfile

def part1():
  allergens = {}
  ingredientsWithDupes = []
  for line in readfile('day21.txt'):
    v = line.split('(contains ')
    assert len(v) == 2, 'bad line; %s' % line
    a = v[1].split(', ')
    a[-1] = a[-1][:-1] # chomp off trailing )
    ingredients = set(v[0].split())
    ingredientsWithDupes.extend(list(ingredients))
    
    for al in a:
      if al not in allergens:
        allergens[al] = ingredients.copy()
      else:
        allergens[al] &= ingredients
  print('allergens:', allergens)

  allergenIngredients = set()
  for als in allergens.values():
    allergenIngredients |= set(als)
  
  print('allergen ingredients', allergenIngredients)
  c = 0
  for i in ingredientsWithDupes:
    if i not in allergenIngredients:
      c += 1
  print(c)

def part2():
  allergens = {}
  for line in readfile('day21.txt'):
    v = line.split('(contains ')
    assert len(v) == 2, 'bad line; %s' % line
    a = v[1].split(', ')
    a[-1] = a[-1][:-1] # chomp off trailing )
    ingredients = set(v[0].split())
    
    for al in a:
      if al not in allergens:
        allergens[al] = ingredients.copy()
      else:
        allergens[al] &= ingredients
  print('allergens:', allergens)

  canonical = {}
  while len(allergens) > 0:
    temp = allergens.copy()
    for a in allergens.keys():
      if len(allergens[a]) == 1:
        (ingredient,) = allergens[a]
        canonical[a] = ingredient
        del temp[a]
        for a2 in temp:
          if ingredient in temp[a2]:
            temp[a2].remove(ingredient)
    allergens = temp
  print('canonical', canonical)

  print()
  print(','.join([canonical[x] for x in [k for k in sorted(canonical.keys())]]))
  
part2()
