from scipy.sparse import lil_matrix
from scipy.spatial.distance import directed_hausdorff
import numpy as np
import math

def calculate_distance_matrix(traj_list, threshold):

    def hausdorf(traj1, traj2):
        d = max(directed_hausdorff(traj1, traj2)[0], directed_hausdorff(traj2, traj1)[0])
        return d

    size = len(traj_list)

    for i in range(size):
        traj_list[i] = np.array(traj_list[i])

    D = lil_matrix((size, size))

    for i in range(size):
        for j in range(i + 1, size):
            distance = hausdorf(traj_list[i], traj_list[j])
            if distance < threshold:
                D[i, j] = distance
                D[j, i] = distance

    return D

def calculate_dense_distance_matrix(traj_list):

    def hausdorf(traj1, traj2):
        d = max(directed_hausdorff(traj1, traj2)[0], directed_hausdorff(traj2, traj1)[0])
        return d

    size = len(traj_list)

    for i in range(size):
        traj_list[i] = np.array(traj_list[i])

    D = np.empty((size, size))

    for i in range(size):
        for j in range(i + 1, size):
            distance = hausdorf(traj_list[i], traj_list[j])
            D[i, j] = distance
            D[j, i] = distance

    return D

def kMedoids(D, k, tmax=100):
    # determine dimensions of distance matrix D
    m, n = D.shape

    #D = D.todense()
    #D[D == 0] = math.inf

    if k > n:
        raise Exception('too many medoids')
    # randomly initialize an array of k medoid indices
    M = np.arange(n)
    np.random.shuffle(M)
    M = np.sort(M[:k])

    # create a copy of the array of medoid indices
    Mnew = np.copy(M)

    # initialize a dictionary to represent clusters
    C = {}
    for t in range(tmax):
        # determine clusters, i. e. arrays of data indices
        J = np.argmin(D[:,M], axis=1)

        for kappa in range(k):
            C[kappa] = np.where(J==kappa)[0]
        # update cluster medoids
        for kappa in range(k):
            J = np.mean(D[np.ix_(C[kappa],C[kappa])],axis=1)
            j = np.argmin(J)
            Mnew[kappa] = C[kappa][j]
        np.sort(Mnew)
        # check for convergence
        if np.array_equal(M, Mnew):
            break
        M = np.copy(Mnew)
    else:
        # final update of cluster memberships
        J = np.argmin(D[:,M], axis=1)
        for kappa in range(k):
            C[kappa] = np.where(J==kappa)[0]

    # return results
    return M, C