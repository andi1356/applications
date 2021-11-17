#!/bin/python3

import math
import os
import random
import re
import sys


#
# Complete the 'minimumDistance' function below.
#
# The function is expected to return an INTEGER.
# The function accepts 2D_INTEGER_ARRAY area as parameter.
#
import collections

def minimumDistance(area):
    start = 0, 0
    queue = collections.deque([[start]])
    print(queue)
    seen = set([start])
    while queue:
        print('' + str(queue))
        path = queue.popleft()
        print('path:' + str(path))
        print('\t' + str(queue))
        x, y = path[-1]
        if area[y][x] == 9:
            return len(path)-1
        for x2, y2 in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
            if 0 <= x2 < 3 and 0 <= y2 <3 and area[y2][x2] != 0 and (x2,y2) not in seen:
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))


if __name__ == '__main__':
    print(minimumDistance(area=[[1, 0, 0], [1, 0, 0], [1, 9, 1]]))
