# Unzip a list from [(1, 2), (3, 4), (5, 6)] to [(1, 3, 5), (2, 4, 6)]
pairs = [(1, 2), (3, 4), (5, 6)]
zip(*pairs)
