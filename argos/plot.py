import matplotlib.pyplot as plt
import matplotlib.image as mpimg

_base_color = plt.rcParams['axes.prop_cycle'].by_key()['color'][0]


def plot_traj(x, color=_base_color, alpha=1.0):
    plt.plot([x[0] for x in x], [x[1] for x in x], c=color, alpha=alpha)

def plot_map():
    img = mpimg.imread("turkey.png")
    extent = [0, 1639740, 0, 670220]
    plt.axis(extent)
    plt.tight_layout()
    plt.imshow(img, zorder=0, extent=extent)
    plt.axes().invert_yaxis()
    plt.show()