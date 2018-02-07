import math
import matplotlib.pyplot as plt
import random
import time
import numpy as np
from scipy.spatial.distance import directed_hausdorff

def distance(point1, point2):
    retval = (point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2
    retval = math.sqrt(retval)
    return retval


def hausdorf_oneway(traj1, traj2):
    # It is a slow implementation. This guy has the fast version:
    # https://github.com/mavillan/py-hausdorff

    max = 0

    for point1 in traj1:

        min = math.inf
        for point2 in traj2:

            d = distance(point1, point2)
            if d < min:
                min = d

        if min > max:
            max = min

    return max


def hausdorf(traj1, traj2):
    d1 = hausdorf_oneway(traj1, traj2)
    d2 = hausdorf_oneway(traj2, traj1)

    if d1 > d2:
        return d1

    return d2

def scipy_hausdorff( u, v):

    #  Trajectories are assumed to be given as np array
    d = max(directed_hausdorff(u, v)[0], directed_hausdorff(v, u)[0])
    return d


if __name__ == "__main__":
    print("hi")

    traj_list = []
    traj_count = 1000
    traj_length = 100

    start = time.time()
    for i in range(traj_count):
        traj_list.append([])
        for j in range(traj_length):
            x = random.random() * 100
            y = random.random() * 100
            traj_list[i].append( (x, y))

    end = time.time()
    elapsed = end - start
    print("Creating trajectories took %s seconds" % elapsed)

    start = time.time()
    for i in range(len(traj_list)):
        traj_list[i] = np.array(traj_list[i])

    end = time.time()
    elapsed = end - start
    print("Numpifing trajectories took %s seconds" % elapsed)

    start = time.time()

    for i in range(traj_count):
        for j in range(i, traj_count):
            scipy_hausdorff(traj_list[i], traj_list[j])

    end = time.time()
    elapsed = end - start
    print("Calculating hausdorf distances took %s seconds" % elapsed)
