import argos.io as io
import argos.plot as tplot
import matplotlib.pyplot as plt
import numpy as np
import hdbscan
from sklearn import metrics
import argos.cluster as cluster

traj_list = io.load("1_traj_seg.dt")
traj_list = traj_list[:1000]

'''
D = io.load_distance_matrix("distance1.npz")
D = D[:1000,:1000]
'''

#D = cluster.calculate_dense_distance_matrix(traj_list)
#D.tofile("dense.dat")
D = np.fromfile("dense.dat", dtype=float)
print(D.shape)
D = D.reshape((1000, 1000))

K = 20
M, C = cluster.kMedoids(D, K)

#  Postprocessing

print("Total number of clusters : %s" % K)

labels = np.zeros((len(traj_list),))

lol = 0
for i in range(K):
    for index in C[i]:
        lol += 1
        labels[index] = i

print(lol)

clusters = [[] for i in range(K)]
no = len(traj_list)
for i in range(no):
    label = int(labels[i])
    clusters[label].append(traj_list[i])

silhoutte_score = metrics.silhouette_score(D, labels, sample_size=1000)
print("Silhoutte Coefficient : %.3f" % silhoutte_score)

sse_list = []
for h in range(2, 80):
    M, C = cluster.kMedoids(D, h)
    sse = 0
    for i in range(h):
        medoid_index = M[i]
        sse += np.sum(D[medoid_index,C[i]] ** 2)
    sse_list.append(sse)
    print(sse)

plt.plot(range(2, 80), sse_list)
plt.xlabel("K")
plt.ylabel("SSE")
plt.title("Sum of Squared Error")
plt.show()


#  Plotting Clustered Trajectories
color_list = plt.rcParams['axes.prop_cycle'].by_key()['color']
for i in range(K):
    for traj in clusters[i]:
        next_color = color_list[i % len(color_list)]
        tplot.plot_traj(traj, next_color, alpha=1)

tplot.plot_map()
