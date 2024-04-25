
def linear_transform(x, old_min, old_max, new_min, new_max):
    x_new = new_min + (x - old_min) * scale_factor(old_min, old_max, new_min, new_max)
    return x_new

def scale_factor(old_min, old_max, new_min, new_max):
    return (new_max - new_min) / (old_max - old_min)
