import random
import math
import argos.util as util


def generate_traj(point_list, noise):
    traj = []
    for point in point_list:
        azimuth = random.random() * math.pi
        distance = random.random() * noise
        noised_point = util.get_point(point, azimuth, distance)
        traj.append(noised_point)

    return traj


def generate_cluster(n, length, noise):
    canvas_range = 100
    azimuth_range = math.pi / 6
    distance_range = 10

    x = random.random() * canvas_range - canvas_range * 0.5
    y = random.random() * canvas_range - canvas_range * 0.5
    azimuth = random.random() * math.pi * 2
    point = (x, y)

    point_list = []
    for i in range(length):
        distance = random.random() * distance_range
        point = util.get_point(point, azimuth, distance)
        azimuth = azimuth + random.random() * azimuth_range - azimuth_range * 0.5
        point_list.append(point)

    traj_list = []
    for i in range(n):
        traj_list.append(generate_traj(point_list, noise))
    return traj_list
