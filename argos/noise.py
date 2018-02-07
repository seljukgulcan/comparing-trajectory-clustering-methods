import argos.util as util

_moved_threshold = 10000  # If a plane does not move longer than this distance (meter) then this flight is removed.
_speed_threshold = 50  # If a plane moves slower than this (m/sec), then it is considered stopped.
_length_threshold = 20  # Path should contain this many points

_segmentation_angle_threshold = 5  # In degree

def remove_noise( traj_dict):

    keys_to_removed = []

    for key in traj_dict.keys():
        path = traj_dict[key]["path"]

        length = len(path)

        if length < _length_threshold:
            keys_to_removed.append(key)

        else:
            start = path[0]
            middle = path[length // 2]
            end = path[length - 1]

            d1 = util.distance(start, middle)
            d2 = util.distance(middle, end)

            if d1 < _moved_threshold and d2 < _moved_threshold:
                keys_to_removed.append(key)

    for key in keys_to_removed:
        traj_dict.pop(key)


def _shorten_traj( traj):

    retval = [x for x in traj if x[2] > _speed_threshold]
    return retval


def shorten(traj_dict):

    for key in traj_dict.keys():
        path = traj_dict[key]["path"]
        path = _shorten_traj(path)
        traj_dict[key]["path"] = path
        traj_dict[key]["count"] = len(path)


def _segmentation(traj):
    retval = []

    azimuth = 1000
    for point in traj:
        d_azimuth = abs( azimuth - point[3])
        if d_azimuth > _segmentation_angle_threshold:
            azimuth = point[3]
            retval.append(point)

    retval.append( traj[len(traj) - 1])

    return retval


def segmentation_list(traj_list):

    for i in range(len(traj_list)):
        traj_list[i] = _segmentation(traj_list[i])