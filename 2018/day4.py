from datetime import datetime
from enum import Enum
from collections import namedtuple, Counter, defaultdict

input = open('day4.txt').read().splitlines()

class Action(Enum):
  SLEEP = 1
  WAKE = 2

Event = namedtuple('Event', ['id', 'action', 'ts'])

def parseInput() -> list[Event]:
  # [1518-11-01 00:00] Guard #10 begins shift
  # [1518-11-01 00:05] falls asleep
  # [1518-11-01 00:25] wakes up
  def p(line: str):
    tss = line.split('] ')[0][1:]
    return datetime.strptime(tss, '%Y-%m-%d %H:%M')

  events: list[Event] = []
  id = None
  for line in sorted(input, key=lambda x: p(x)):
    v = line.split('] ')[1]
    match v:
      case 'falls asleep':
        action = Action.SLEEP
      case 'wakes up':
        action = Action.WAKE
      case _:
        id = int(v.split('#')[1].split()[0])
        continue
    ts = p(line)
    assert ts.hour == 0, 'sleep/wake should be at midnight'
    assert id is not None, 'id should be set'
    events.append(Event(id, action, ts))

  return events

def part1() -> None:
  events = parseInput()
  print('events:', len(events))

  lastEventTimes: dict[int, int] = defaultdict(int)
  asleepCount: dict[int, int] = Counter()
  for e in events:
    id = e.id
    duration = e.ts.minute - lastEventTimes[id]
    lastEventTimes[id] = e.ts.minute
    if e.action == Action.WAKE:
      asleepCount[id] += duration

  guard = max(asleepCount, key=asleepCount.__getitem__)
  print('max guard:', guard)

  lastTsForGuard = 0
  asleepMins: dict[int, int] = Counter()
  for e in events:
    id = e.id
    if id != guard:
      continue

    if e.action == Action.WAKE:
      for m in range(lastTsForGuard, e.ts.minute):
        asleepMins[m] += 1
    lastTsForGuard = e.ts.minute

  mostMinute = max(asleepMins, key=asleepMins.__getitem__)
  print('max min:', mostMinute)

  print(guard * mostMinute)

def part2() -> None:
  events = parseInput()
  print('events:', len(events))

  lastEventTimes: dict[int, int] = defaultdict(int)
  asleepMins: dict[int, dict[int, int]] = defaultdict(lambda: Counter())
  for e in events:
    id = e.id
    if e.action == Action.WAKE:
      for m in range(lastEventTimes[id], e.ts.minute):
        asleepMins[m][id] += 1
    lastEventTimes[id] = e.ts.minute

  mostMinutes = -1
  mostMinute = -1
  mostGuard = None
  for m in asleepMins:
    guard = max(asleepMins[m], key=asleepMins[m].__getitem__)
    minutes = asleepMins[m][guard]
    if minutes > mostMinutes:
      mostMinutes = minutes
      mostMinute = m
      mostGuard = guard

  print('max min:', mostMinute)
  print('max guard:', mostGuard)
  assert mostGuard is not None, 'did not find mostGuard'
  print(mostMinute * mostGuard)

part2()
