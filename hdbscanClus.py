import argos.io as io
import argos.plot as tplot
import matplotlib.pyplot as plt
import numpy as np
import hdbscan
from sklearn import metrics

traj_list = io.load("1_traj_seg.dt")
traj_list = traj_list[:1000]
min_samples = 1
min_cluster_size = 2

D = io.load_distance_matrix("distance1.npz")

dbscan = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, min_samples=min_samples, metric="precomputed", memory="hdbscan_cache")
dbscan.fit(D)

#  Postprocessing
no_of_labels = np.max(dbscan.labels_) + 1

print("Total number of clusters : %s" % no_of_labels)

clusters = [[] for i in range(no_of_labels)]
outliers = []
no = len(traj_list)
for i in range(no):
    label = dbscan.labels_[i]
    if label == -1:
        outliers.append(traj_list[i])
    else:
        clusters[label].append(traj_list[i])

no_of_noise = len(outliers)
print("Number of noise points %s" % no_of_noise)
print("Noise Percentage : %.3f" % (no_of_noise / no))

silhoutte_score = metrics.silhouette_score(D, dbscan.labels_)
print("Silhoutte Coefficient : %.3f" % silhoutte_score)

#  Plotting Clustered Trajectories
color_list = plt.rcParams['axes.prop_cycle'].by_key()['color']
for i in range(no_of_labels):
    for traj in clusters[i]:
        next_color = color_list[0 % len(color_list)]
        tplot.plot_traj(traj, next_color, alpha=1)
        #tplot.plot_traj(traj)

for traj in outliers:
    tplot.plot_traj(traj, "r")

tplot.plot_map()
