import argos.io as io
import argos.plot as tplot
import matplotlib.pyplot as plt
import numpy as np
from sklearn import metrics
from sklearn.mixture import GMM

traj_list = io.load("1_traj_seg.dt")
traj_list = traj_list[:1000]

X = np.fromfile("gaussian_representation.dat", dtype=float)
D = io.load_distance_matrix("distance1.npz")

no_of_cluster = 12
gmm = GMM(n_components=no_of_cluster,  n_iter=1000)
labels = gmm.fit_predict(X)

#  Postprocessing

clusters = [[] for i in range(no_of_cluster)]
no = len(traj_list)
for i in range(no):
    label = int(labels[i])
    clusters[label].append(traj_list[i])

silhoutte_score = metrics.silhouette_score(D, labels, sample_size=1000)
print("Silhoutte Coefficient : %.3f" % silhoutte_score)

#  Plotting Clustered Trajectories
color_list = plt.rcParams['axes.prop_cycle'].by_key()['color']
for i in range(no_of_cluster):
    for traj in clusters[i]:
        next_color = color_list[i % len(color_list)]
        tplot.plot_traj(traj, next_color, alpha=1)

tplot.plot_map()
