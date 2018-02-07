import argos.io as io
import math
import argos.plot as tplot
import argos.util as util
import argos.noise as reduc
import argos.cluster as cluster
from argos.tool.stopwatch import Stopwatch

id = 0
id_list = []
traj_list = []
for i in range(7):
    filename = "%s.traj" % i
    traj_dict = io.load(filename)

    reduc.shorten(traj_dict)
    reduc.remove_noise(traj_dict)

    for key in traj_dict:
        id_list.append( (id, key))
        id += 1
        path = traj_dict[key]["path"]
        traj_list.append(path)

    io.save(traj_list, "%s_traj.dt" % i)

    reduc.segmentation_list(traj_list)

    io.save(traj_list, "%s_traj_seg.dt" % i)
    traj_list = []
io.save(id_list, "id_list.dt")
exit(0)


s = Stopwatch()
n = 100

traj_dict = io.load("1.traj")

util.summary_traj_dict(traj_dict)

reduc.shorten(traj_dict)


util.summary_traj_dict(traj_dict)

reduc.remove_noise(traj_dict)

util.summary_traj_dict(traj_dict)

reduc.remove_noise(traj_dict)
reduc.shorten(traj_dict)

util.summary_traj_dict(traj_dict)

traj_list = util.traj_dict_to_traj_list(traj_dict)

util.summary_traj_list(traj_list)

s.start()
D1 = cluster.calculate_distance_matrix(traj_list[:n], 80000)
s.stop()

reduc.segmentation_list(traj_list)

util.summary_traj_list(traj_list)


traj_list = traj_list[:n]

s.start()
D2 = cluster.calculate_distance_matrix(traj_list, 80000)
s.stop()

sum = 0
diff_count = 0
for i in range(n):
    for j in range(i, n):
        diff = abs( D1[i,j] - D2[i, j])
        sum += diff
        if diff > 1000:
            diff_count += 1

print(diff_count)

print(sum)
exit(0)

countFlied = 0
countFlied2 = 0
traj_list = []
suspi = None
for key in traj_dict.keys():
    path = traj_dict[key]["path"]
    count = 0
    flied = False

    start = path[0]
    end = path[len(path) - 1]
    if abs(start[0] - end[0]) > 30000 or abs(start[1] - end[1]) > 30000:
        countFlied2 += 1

    for point in path:
        if point[2] < 1 and point[5] < 1:
            count += 1
        if not flied and point[5] > 5:
            flied = True
            countFlied += 1

    if not flied:
        suspi = path

    traj_list.append(path)

print(countFlied)
print(countFlied2)

'''
for traj in traj_list:
    tplot.plot_traj(traj)
'''

print(suspi)
tplot.plot_traj(suspi)

tplot.plot_map()

exit(0)


filename1 = "3.traj"
filename2 = "6.traj"

d1 = io.load(filename1)
d2 = io.load(filename2)

key1 = set(d1.keys())
key2 = set(d2.keys())
common = key1.intersection(key2)

print(len(common))

for key in common:
    d1[key]["path"] = d1[key]["path"] + d2[key]["path"]
    d1[key]["count"] = d1[key]["count"] + d2[key]["count"]
    d2.pop(key)

io.save(d1, filename1)
io.save(d2, filename2)
