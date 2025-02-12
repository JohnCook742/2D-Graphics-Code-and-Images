import math

def nn_interpolation(data, x, y):
    return data[math.floor(x), math.floor(y)]

def interpolate(start, end, percent):
    return(end-start) * percent + start

def interpolateRGB(start, end, percent):
    r_start = start[0]
    g_start = start[1]
    b_start = start[2]

    r_end = end[0]
    g_end = end[1]
    b_end = end[2]

    r = int(interpolate(r_start, r_end, percent))
    g = int(interpolate(g_start, g_end, percent))
    b = int(interpolate(b_start, b_end, percent))

    return (r,g,b)

def bilinear_interpolation(data, x, y):
    x_start = int(math.floor(x))
    x_end = int(x_start + 1)
    x_percent = x - x_start

    y_start = int(math.floor(y))
    y_end = int(y_start + 1)
    y_percent = y - y_start

    top_left = data[x_start, y_start]
    top_right = data[x_end, y_start]
    bottom_left = data[x_start, y_end]
    bottom_right = data[x_end, y_end]

    top = interpolateRGB(top_left, top_right, x_percent)
    bottom = interpolateRGB(bottom_left, bottom_right, x_percent)

    result = interpolateRGB(top, bottom, y_percent)

    return result