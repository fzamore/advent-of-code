def readfile(filename):
    lines = None
    with open(filename) as f:
        lines = f.read().splitlines()
    return lines
