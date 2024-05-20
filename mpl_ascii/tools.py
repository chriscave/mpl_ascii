
def linear_transform(x, old_min, old_max, new_min, new_max):
    x_new = new_min + (x - old_min) * scale_factor(old_min, old_max, new_min, new_max)
    return x_new

def scale_factor(old_min, old_max, new_min, new_max):
    return (new_max - new_min) / (old_max - old_min)

def get_xrange(ax):
    x_range = ax.get_xlim()
    if x_range[1] < x_range[0]:
        x_range = x_range[1], x_range[0]
    return x_range

def get_yrange(ax):
    y_range = ax.get_ylim()
    if y_range[1] < y_range[0]:
        y_range = y_range[1], y_range[0]
    return y_range