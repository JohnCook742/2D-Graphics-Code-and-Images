from PIL import Image
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

image = Image.open("car.jpg")
data = image.load()
new_image = Image.new("RGB", (image.width, image.height))
new_data = new_image.load()

rotation = .5
center = (image.width/2, image.height/2)

cosine_theta = math.cos(-rotation)
sine_theta = math.sin(-rotation)

for y in range(image.height):
    for x in range(image.width):
        new_x = cosine_theta * x - sine_theta * y - cosine_theta * center[0] + sine_theta*center[1] + center[0]
        new_y = sine_theta * x + cosine_theta * y - sine_theta * center[0] - cosine_theta * center[1] + center[1]

        # new_x //= 1
        # new_y //= 1

        if 0<=new_x<image.width-1 and 0<=new_y<image.height-1:
            new_data[x,y] = bilinear_interpolation(data, new_x, new_y)
        else:
            new_data[x,y] = (0,0,0)

new_image.save("rotation_bilinear.png")