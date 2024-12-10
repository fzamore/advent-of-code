from typing import Optional

input = open('day9.txt').read().strip()

Freelist = list[tuple[int, int]] # Each freelist entry is (start, size)

def findFreelistEntry(freelist: Freelist, minSize: int, maxI: int) -> Optional[int]:
  for i, (pos, size) in enumerate(freelist):
    if pos >= maxI:
      return None
    if size >= minSize:
      return i
  return None

def part1() -> None:
  print('len', len(input))

  freeptr = -1
  id = 0
  blocks: list[int | None] = []
  for lastDataPtr, c in enumerate(input):
    digit = int(c)
    if lastDataPtr % 2 == 0:
      blocks.extend([id] * digit)
      id += 1
    else:
      if freeptr == -1:
        freeptr = len(blocks)
      blocks.extend([None] * digit)

  print('freeptr:', freeptr)
  n = len(blocks)
  lastDataPtr = n - 1
  while True:
    # Decrease the last data pointer.
    while blocks[lastDataPtr] is None:
      lastDataPtr -= 1

    if lastDataPtr <= freeptr:
      break

    assert blocks[freeptr] is None, 'freeptr points to data'
    assert blocks[lastDataPtr] is not None, 'empty block past freeptr'

    # Swap the blocks
    blocks[freeptr] = blocks[lastDataPtr]
    blocks[lastDataPtr] = None

    # Increase the free pointer.
    while blocks[freeptr] is not None:
      freeptr += 1

  print(sum([i * b for (i, b) in enumerate(blocks) if b is not None]))

def part2() -> None:
  print('len', len(input))

  freelist = []
  files = {}
  id = 0
  blockCount = 0
  for fileI, c in enumerate(input):
    digit = int(c)
    entry = (blockCount, digit)
    if fileI % 2 == 0:
      files[id] = entry
      id += 1
    else:
      freelist.append(entry)
    blockCount += digit

  # Move through files from right to left.
  for id in range(max(files.keys()), -1, -1):
    fileI, fileSize = files[id]
    freelistI = findFreelistEntry(freelist, fileSize, fileI)
    if freelistI is None:
      continue

    # We found an appropriate freelist entry.
    freelistPos, freelistSize = freelist[freelistI]
    assert freelistSize >= fileSize and freelistPos < fileI, 'bad freelist entry for file'

    # Move the file to the beginning of the freelist entry.
    files[id] = freelistPos, fileSize

    # Update the freelist.
    if freelistSize == fileSize:
      # The file occupies the entire freelist entry. Remove the entry.
      freelist.pop(freelistI)
    else:
      # Otherwise, trim the freelist entry to remove the file size from its left.
      freelist[freelistI] = (freelistPos + fileSize, freelistSize - fileSize)

  checksum = 0
  for id in files:
    pos, fileSize = files[id]
    assert fileSize >= 1, 'file should have size at least 1'
    for fileI in range(pos, pos + fileSize):
      checksum += id * fileI

  print(checksum)

part2()
