#  Synthetic Demo

import random
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN
from argos.cluster import calculate_distance_matrix
from argos.tool.stopwatch import Stopwatch
from argos.synthetic import  generate_cluster
import argos.plot as aplt


if __name__ == "__main__":
    print("Synthetic Demo")
    s = Stopwatch()

    #  Parameters of Demo
    no_of_cluster = 20
    no_of_traj = 100
    traj_length = 100
    eps = 10
    min_samples = 5
    noise = 5

    #  Generating Trajectories
    no_of_outlier = int( no_of_traj * 0.05)
    no_of_traj_each_cluster = no_of_traj // no_of_cluster

    print("-----")
    print("No of Clusters : %s" % no_of_cluster)
    print("No of Outliers : %s" % no_of_outlier)
    print("-----")

    normal_traj_list = []
    for i in range(no_of_cluster):
        traj_list = generate_cluster(no_of_traj_each_cluster, traj_length, noise)
        normal_traj_list += traj_list

    outlier_traj_list = []
    for i in range(no_of_outlier):
        outlier_traj_list += generate_cluster(1, traj_length, noise)

    #  Plotting Generated Trajectories

    plt.figure(1)
    plt.subplot(121)

    for traj in normal_traj_list:
        aplt.plot_traj(traj)

    for traj in outlier_traj_list:
        aplt.plot_traj(traj, "r")

    #  Precomputation

    traj_list = normal_traj_list + outlier_traj_list
    random.shuffle(traj_list)

    #  Calculating Distance Matrix
    s.start()
    D = calculate_distance_matrix( traj_list, eps)
    s.stop("Distance matrix calculated")

    #  Clustering
    s.start()
    dbscan = DBSCAN(eps=eps, min_samples=min_samples, metric="precomputed")
    dbscan.fit(D)
    s.stop("Clustering is done")

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

    #  Plotting Clustered Trajectories
    plt.subplot(122)
    color_list = plt.rcParams['axes.prop_cycle'].by_key()['color']
    for i in range(no_of_labels):
        for traj in clusters[i]:
            next_color = color_list[i % len(color_list)]
            aplt.plot_traj(traj, next_color, alpha=0.3)

    for traj in outliers:
        aplt.plot_traj(traj, "k")

    plt.show()