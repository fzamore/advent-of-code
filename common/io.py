from typing import Iterable

def readfile(filename: str) -> Iterable[str]:
    with open(filename) as f:
        return f.read().splitlines()
