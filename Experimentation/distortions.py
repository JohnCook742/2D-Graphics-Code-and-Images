from PIL import Image
import math
import interpolations

image = Image.open("car.jpg")

data = image.load()
print(image.width)
print(image.height)

pixel = data[0,0]
print(pixel)
print(pixel[0])
print(pixel[1])
print(pixel[2])

red = pixel[0]
green = pixel[1]
blue = pixel[2]

# def nn_interpolation(data, x, y):
#     return data[math.floor(x), math.floor(y)]

# def interpolate(start, end, percent):
#     return(end-start) * percent + start

# def interpolateRGB(start, end, percent):
#     r_start = start[0]
#     g_start = start[1]
#     b_start = start[2]

#     r_end = end[0]
#     g_end = end[1]
#     b_end = end[2]

#     r = int(interpolate(r_start, r_end, percent))
#     g = int(interpolate(g_start, g_end, percent))
#     b = int(interpolate(b_start, b_end, percent))

#     return (r,g,b)

# def bilinear_interpolation(data, x, y):
#     x_start = int(math.floor(x))
#     x_end = int(x_start + 1)
#     x_percent = x - x_start

#     y_start = int(math.floor(y))
#     y_end = int(y_start + 1)
#     y_percent = y - y_start

#     top_left = data[x_start, y_start]
#     top_right = data[x_end, y_start]
#     bottom_left = data[x_start, y_end]
#     bottom_right = data[x_end, y_end]

#     top = interpolateRGB(top_left, top_right, x_percent)
#     bottom = interpolateRGB(bottom_left, bottom_right, x_percent)

#     result = interpolateRGB(top, bottom, y_percent)

#     return result

def wiggleX(original_image, shiftProportion, wiggles):
    temp_image = Image.new("RGB", (int(original_image.width * (1 + 2 * shiftProportion)), original_image.height))
    temp_data = temp_image.load()
    original_data = original_image.load()
    dx = original_image.width * shiftProportion

    for y in range(original_image.height):
        for x in range(original_image.width):
            offset = int(dx + dx * -(math.cos(wiggles * y/original_image.height)))
            pixel = original_data[x,y]
            temp_data[x+offset, y] = pixel
    
    return temp_image

def wiggleY(original_image, shiftProportion, wiggles):
    temp_image = Image.new("RGB", (original_image.width, int(original_image.height * (1 + 2 * shiftProportion))))
    temp_data = temp_image.load()
    original_data = original_image.load()
    dy = original_image.height * shiftProportion

    for y in range(original_image.height):
        for x in range(original_image.width):
            offset = int(dy + dy * -(math.cos(wiggles * x/original_image.width)))
            pixel = original_data[x,y]
            temp_data[x, y+offset] = pixel
    
    return temp_image

def wiggleXY(original_image, shiftProportion, wiggles):
    temp_image = wiggleX(original_image,shiftProportion,wiggles)
    temp_image = wiggleY(temp_image,shiftProportion,wiggles)
    
    return temp_image

def swirl(start_image, rotation):
    data = start_image.load()
    temp_image = Image.new("RGB", (start_image.width, start_image.height))
    temp_data = temp_image.load()
    
    center = (temp_image.width/2, temp_image.height/2)

    reference_radius = math.sqrt(temp_image.height**2 + temp_image.width**2)/2

    for y in range(start_image.height):
        #print(y)
        for x in range(start_image.width):
            reference_proportion = 1 - math.sqrt((x-center[0])**2 + (y-center[1])**2) / reference_radius
            
            cosine_theta = math.cos(-rotation * reference_proportion)
            sine_theta = math.sin(-rotation * reference_proportion)

            new_x = cosine_theta * x - sine_theta * y - cosine_theta * center[0] + sine_theta*center[1] + center[0]
            new_y = sine_theta * x + cosine_theta * y - sine_theta * center[0] - cosine_theta * center[1] + center[1]

            new_x //= 1
            new_y //= 1

            if 0<=new_x<start_image.width and 0<=new_y<start_image.height:
                temp_data[x,y] = data[new_x,new_y]
            else:
                temp_data[x,y] = (0,0,0)

    return temp_image

def swirl_progressive(start_image, rotation):
    data = start_image.load()
    temp_image = Image.new("RGB", (start_image.width, start_image.height))
    temp_data = temp_image.load()
    
    center = (temp_image.width/2, temp_image.height/2)

    reference_radius = math.sqrt(temp_image.height**2 + temp_image.width**2)/2

    for y in range(start_image.height):
        #print(y)
        for x in range(start_image.width):
            reference_proportion = 1 - math.sqrt(math.sqrt((x-center[0])**2 + (y-center[1])**2) / reference_radius)
            
            cosine_theta = math.cos(-rotation * reference_proportion)
            sine_theta = math.sin(-rotation * reference_proportion)

            new_x = cosine_theta * x - sine_theta * y - cosine_theta * center[0] + sine_theta*center[1] + center[0]
            new_y = sine_theta * x + cosine_theta * y - sine_theta * center[0] - cosine_theta * center[1] + center[1]

            new_x //= 1
            new_y //= 1

            if 0<=new_x<start_image.width and 0<=new_y<start_image.height:
                temp_data[x,y] = data[new_x,new_y]
            else:
                temp_data[x,y] = (0,0,0)

    return temp_image

def bulge(start_image, strength = 1, interpolation = 0, full_image = False):
    data = start_image.load()
    temp_image = Image.new("RGB", (int(start_image.width), int(start_image.height)))
    temp_data = temp_image.load()

    if (strength < 0):
        print("Invalid strength value")
        strength = 1
    
    min_dimension = min(temp_image.height, temp_image.width)

    centerX = temp_image.width/2
    centerY = temp_image.height/2

    for y in range(temp_image.height):
        for x in range(temp_image.width):
            pixel = data[x,y]

            xc = x - centerX
            yc = y - centerY

            radius = math.sqrt(xc**2+yc**2)
            theta = math.atan2(yc,xc)

            new_radius = (radius/(min_dimension/2))**(strength)

            if(radius > min_dimension/2 and full_image):
                new_radius = radius/(min_dimension/2)

            new_x = math.cos(theta)*new_radius*(min_dimension/2)
            new_y = math.sin(theta)*new_radius*(min_dimension/2)

            new_x += centerX
            new_y += centerY

            if new_x<0 or new_x >= temp_image.width-1 or new_y < 0 or new_y>= temp_image.height-1:
                temp_data[x,y] = (0,0,0)

            else:
                if interpolation == 1:
                    temp_data[x,y] = interpolations.nn_interpolation(data, new_x, new_y)
                elif interpolation == 2:
                    temp_data[x,y] = interpolations.bilinear_interpolation(data, new_x, new_y)
                else:
                    temp_data[x,y] = data[math.floor(new_x),math.floor(new_y)]

    return temp_image

def bulge_smooth(start_image, strength = 1, interpolation = 0, full_image = False):
    data = start_image.load()
    temp_image = Image.new("RGB", (int(start_image.width), int(start_image.height)))
    temp_data = temp_image.load()

    if (strength < 0):
        print("Invalid strength value")
        strength = 1
    
    min_dimension = min(temp_image.height, temp_image.width)

    centerX = temp_image.width/2
    centerY = temp_image.height/2

    for y in range(temp_image.height):
        for x in range(temp_image.width):
            pixel = data[x,y]

            xc = x - centerX
            yc = y - centerY

            radius = math.sqrt(xc**2+yc**2)
            theta = math.atan2(yc,xc)

            radius_proportion = radius/(min_dimension/2)

            new_radius = (radius_proportion)**(1 + (strength-1) * (radius_proportion)**(strength))

            if(radius > min_dimension/2 and full_image):
                new_radius = radius/(min_dimension/2)

            new_x = math.cos(theta)*new_radius*(min_dimension/2)
            new_y = math.sin(theta)*new_radius*(min_dimension/2)

            new_x += centerX
            new_y += centerY

            if new_x<0 or new_x >= temp_image.width-1 or new_y < 0 or new_y>= temp_image.height-1:
                temp_data[x,y] = (0,0,0)

            else:
                if interpolation == 1:
                    temp_data[x,y] = interpolations.nn_interpolation(data, new_x, new_y)
                elif interpolation == 2:
                    temp_data[x,y] = interpolations.bilinear_interpolation(data, new_x, new_y)
                else:
                    temp_data[x,y] = data[math.floor(new_x),math.floor(new_y)]
    return temp_image

# new_image = wiggleX(image, .1, 3*math.pi)
# new_image.save("wiggleX.png")

# new_image = wiggleY(image, .1, 3*math.pi)
# new_image.save("wiggleY.png")

# new_image = wiggleXY(image, .1, 3*math.pi)
# new_image.save("wiggleXY.png")

# new_image = swirl(image, 1*math.pi)
# new_image.save("swirl.png")

# new_image = swirl_progressive(image, 1*math.pi)
# new_image.save("swirl_progressive.png")

bulge_value = 2
interpolation_value = 2
full_image = 1
new_image = bulge(image,bulge_value, interpolation_value, full_image)
new_image.save("bulge.png")
new_image = bulge_smooth(image,bulge_value, interpolation_value, full_image)
new_image.save("bulge_smooth.png")


