import math

map_width = 1639.74 * 1000  # in meters
map_height = 670.22 * 1000  # in meters

map_lon_left = 26
map_lon_right = 45
map_lon_delta = map_lon_right - map_lon_left

map_lat_bottom = 36
map_lat_bottom_degree = map_lat_bottom * math.pi / 180


def get_point(point, azimuth, distance):
    x = point[0] + distance * math.cos(azimuth)
    y = point[1] + distance * math.sin(azimuth)

    return x, y


def distance(point1, point2):
    x = abs(point1[0] - point2[0])
    y = abs(point1[1] - point2[1])
    d = math.sqrt(x ** 2 + y ** 2)
    return d


def geo_to_xy(lat, lon):

    # According to mercator projection it calculates x and y distances in meter relative to top left point
    # Taken from https://stackoverflow.com/questions/2103924/mercator-longitude-and-latitude-calculations-to-x-and-y-on-a-cropped-map-of-the/10401734#10401734
    x = (lon - map_lon_left) * (map_width / map_lon_delta)

    lat = lat * math.pi / 180
    world_map_width = ((map_width / map_lon_delta) * 360) / (2 * math.pi)
    map_offset_y = (world_map_width / 2 * math.log((1 + math.sin(map_lat_bottom_degree)) / (1 - math.sin(map_lat_bottom_degree))))
    y = map_height - ((world_map_width / 2 * math.log((1 + math.sin(lat)) / (1 - math.sin(lat)))) - map_offset_y)
    x = int(x)
    y = int(y)
    return x, y


def ft_to_m(ft):
    return 0.3048 * ft


def kt_to_kph(kt):
    return 1.852 * kt


def fpm_to_mps(fpm):
    return 0.0051 * fpm


def traj_dict_to_traj_list(traj_dict):
    traj_list = []
    for key in traj_dict.keys():
        traj_list.append( traj_dict[key]["path"])
    return traj_list


def summary_traj_list(traj_list):
    print("Total trajectories : %s" % len(traj_list))
    min = math.inf
    max = 0
    sum = 0
    for traj in traj_list:
        length = len(traj)
        if length > max:
            max = length
        if length < min:
            min = length
        sum += length

    avg = sum / len(traj_list)
    print("Average length : %s" % avg)
    print("Minimum length : %s" % min)
    print("Maximum length : %s" % max)


def summary_traj_dict(traj_dict):
    l = traj_dict_to_traj_list(traj_dict)
    summary_traj_list(l)