from PIL import Image
import array as arr
import math
import color_spaces

image = Image.open("Rick.jpg")

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

def HSV_channel_isolation(test_image, channel = 0):
    data = test_image.load()
    temp_image = Image.new("RGB", (int(test_image.width), int(test_image.height)))
    temp_data = temp_image.load()

    for y in range(temp_image.height):
        for x in range(temp_image.width):
            pixel = color_spaces.rgb_to_hsv(data[x,y])
            if channel == 0:
                if pixel[1] != 0:
                    temp_data[x,y] = color_spaces.hsv_to_rgb((pixel[0], 1, 1))
                else:
                    temp_data[x,y] = (0,0,0)
            else:
                temp_data[x,y] = color_spaces.hsv_to_rgb((0,0,pixel[channel]))

    return temp_image

def HSV_channel_distribution(test_image, channel = 0, bins = 360, graph = False):
    data = test_image.load()
    temp_image = Image.new("RGB", (int(test_image.width), int(test_image.height)))
    temp_data = temp_image.load()

    channel_states = []
    for i in range(bins+1):
        channel_states.append(0)

    for y in range(temp_image.height):
        for x in range(temp_image.width):
            pixel = data[x,y]
            hsv_pixel = color_spaces.rgb_to_hsv(pixel)
            if hsv_pixel[1] != 0:
                state = int(hsv_pixel[channel] * (bins-1) + .5)
            else:
                state = bins
            channel_states[state] += 1

    cur_state = 0
    state_count = 0

    if(graph == True):
        graph_pow = 1
        size_scale = bins
        max_hue = max(channel_states)
        temp_image = Image.new("RGB", (int(size_scale), int(len(channel_states))))
        temp_data = temp_image.load()

        for y in range(temp_image.height):
            for x in range(int(bins * (channel_states[y]/max_hue)**graph_pow)):
                if y < len(channel_states):
                    if channel == 0:
                        if y < bins:
                                temp_data[x,y] = color_spaces.hsv_to_rgb((y/(bins-1),1,1))
                        else:
                            temp_data[x,y] = (128, 128, 128)
                    else:
                        temp_data[x,y] = (255, int(255*y/bins), int(255*y/bins))
                else:
                    print("Error: reached impossible state")
                    temp_data[x,y] = (0,255,255)

    else:
        for y in range(temp_image.height):
            for x in range(temp_image.width):
                while state_count >= channel_states[cur_state]:
                    cur_state += 1
                    state_count = 0

                if cur_state < len(channel_states):
                    if channel == 0:
                        if cur_state < bins:
                                temp_data[x,y] = color_spaces.hsv_to_rgb((cur_state/(bins-1),1,1))
                        else:
                            temp_data[x,y] = (128, 128, 128)
                    else:
                        temp_data[x,y] = (int(255*cur_state/bins), int(255*cur_state/bins), int(255*cur_state/bins))
                        
                    state_count += 1
                else:
                    print("Error: reached impossible hue")
                    temp_data[x,y] = (0,255,255)

    return temp_image

# def hue_distribution(test_image, hue_bins = 360, graph = False):
#     data = test_image.load()
#     temp_image = Image.new("RGB", (int(test_image.width), int(test_image.height)))
#     temp_data = temp_image.load()

#     bins = hue_bins

#     hues = []
#     for i in range(bins+1):
#         hues.append(0)

#     for y in range(temp_image.height):
#         for x in range(temp_image.width):
#             pixel = data[x,y]
#             hsv_pixel = color_spaces.rgb_to_hsv(pixel)
#             if hsv_pixel[1] != 0:
#                 hue = int(hsv_pixel[0] * (bins-1) + .5)
#             else:
#                 hue = bins
#             hues[hue] += 1

#     cur_hue = 0
#     hue_count = 0

#     if(graph == True):
#         size_scale = bins
#         max_hue = max(hues)
#         temp_image = Image.new("RGB", (int(size_scale), int(len(hues))))
#         temp_data = temp_image.load()

#         for y in range(temp_image.height):
#             for x in range(int(bins * (hues[y]/max_hue)**.5)):
#                 if y < len(hues):
#                     if y < bins:
#                         temp_data[x,y] = color_spaces.hsv_to_rgb((y/(bins-1),1,1))
#                     else:
#                         temp_data[x,y] = (128, 128, 128)
#                 else:
#                     print("Error: reached impossible hue")
#                     temp_data[x,y] = (0,255,255)

#     else:
#         for y in range(temp_image.height):
#             for x in range(temp_image.width):
#                 while hue_count >= hues[cur_hue]:
#                     cur_hue += 1
#                     hue_count = 0

#                 if cur_hue < len(hues):
#                     if cur_hue < bins:
#                         temp_data[x,y] = color_spaces.hsv_to_rgb((cur_hue/(bins-1),1,1))
#                     else:
#                         temp_data[x,y] = (128, 128, 128)
#                     hue_count += 1
#                 else:
#                     print("Error: reached impossible hue")
#                     temp_data[x,y] = (0,255,255)

#     return temp_image

# def saturation_distribution(test_image, sat_bins = 256, graph = False):
#     data = test_image.load()
#     temp_image = Image.new("RGB", (int(test_image.width), int(test_image.height)))
#     temp_data = temp_image.load()

#     bins = sat_bins

#     saturations = []
#     for i in range(bins):
#         saturations.append(0)

#     for y in range(temp_image.height):
#         for x in range(temp_image.width):
#             pixel = data[x,y]
#             saturation = int(color_spaces.rgb_to_hsv(pixel)[1] * (bins-1) + .5)
#             saturations[saturation] += 1

    

#     if(graph == True):
#         size_scale = bins
#         max_sat = max(saturations)
#         temp_image = Image.new("RGB", (int(size_scale), int(len(saturations))))
#         temp_data = temp_image.load()

#         for y in range(temp_image.height):
#             for x in range(int(size_scale * (saturations[y]/max_sat)**.5)):
#                 if y < len(saturations):
#                     temp_data[x,y] = (255, 
#                                       int(255 * y/bins), 
#                                       int(255 * y/bins))
#                 else:
#                     print("Error: reached impossible saturation")
#                     temp_data[x,y] = (0,255,255)

#     else:
#         cur_saturation = 0
#         saturation_count = 0

#         for y in range(temp_image.height):
#             for x in range(temp_image.width):
#                 while saturation_count >= saturations[cur_saturation]:
#                     cur_saturation += 1
#                     saturation_count = 0

#                 if cur_saturation < len(saturations):
#                     temp_data[x,y] = (int(255 * saturations[cur_saturation]/bins), 
#                                       int(255 * saturations[cur_saturation]/bins), 
#                                       int(255 * saturations[cur_saturation]/bins))
#                     saturation_count += 1
#                 else:
#                     print("Error: reached impossible saturation")
#                     temp_data[x,y] = (255,255,0)

#     return temp_image

# def value_distribution(test_image, val_bins = 256, graph = False):
    data = test_image.load()
    temp_image = Image.new("RGB", (int(test_image.width), int(test_image.height)))
    temp_data = temp_image.load()

    bins = val_bins

    values = []
    for i in range(bins):
        values.append(0)

    for y in range(temp_image.height):
        for x in range(temp_image.width):
            pixel = data[x,y]
            value = int(color_spaces.rgb_to_hsv(pixel)[2] * (bins-1) + .5)
            values[value] += 1

    if(graph == True):
        size_scale = bins
        max_val = max(values)
        temp_image = Image.new("RGB", (int(size_scale), int(len(values))))
        temp_data = temp_image.load()

        for y in range(temp_image.height):
            for x in range(int(size_scale * (values[y]/max_val)**.5)):
                if y < len(values):
                    temp_data[x,y] = (255, 
                                      int(255 * y/bins), 
                                      int(255 * y/bins))
                else:
                    print("Error: reached impossible saturation")
                    temp_data[x,y] = (0,255,255)

    else:
        cur_value = 0
        value_count = 0

        for y in range(temp_image.height):
            for x in range(temp_image.width):
                while value_count >= values[cur_value]:
                    cur_value += 1
                    value_count = 0

                if cur_value < len(values):
                    temp_data[x,y] = (cur_value, cur_value, cur_value)
                    value_count += 1
                else:
                    print("Error: reached impossible value")
                    temp_data[x,y] = (255,255,0)

    return temp_image

def averageRGB(test_image):
    data = test_image.load()
    avg_r = 0.0
    avg_g = 0.0
    avg_b = 0.0

    for y in range(test_image.height):
        # temp_r = 0.0
        # temp_g = 0.0
        # temp_b = 0.0

        for x in range(test_image.width):
            pixel = data[x,y]
            # temp_r += pixel[0]
            # temp_g += pixel[1]
            # temp_b += pixel[2]

            avg_r += pixel[0]
            avg_g += pixel[1]
            avg_b += pixel[2]

        # temp_r /= test_image.width
        # temp_g /= test_image.width
        # temp_b /= test_image.width

        # avg_r = (avg_r * y + temp_r) / (y+1)
        # avg_g = (avg_g * y + temp_g) / (y+1)
        # avg_b = (avg_b * y + temp_b) / (y+1)

    avg_r /= test_image.width * test_image.height
    avg_g /= test_image.width * test_image.height
    avg_b /= test_image.width * test_image.height
    
    return (int(avg_r),int(avg_g),int(avg_b))

def averageRGB_image(test_image):
    # data = test_image.load()
    temp_image = Image.new("RGB", (int(test_image.width), int(test_image.height)))
    temp_data = temp_image.load()

    pixel = averageRGB(test_image)

    for y in range(temp_image.height):
        for x in range(temp_image.width):
            temp_data[x,y] = pixel

    return temp_image

def averageRGB_row(test_image):
    data = test_image.load()
    temp_image = Image.new("RGB", (int(test_image.width), int(test_image.height)))
    temp_data = temp_image.load()

    for y in range(temp_image.height):
        temp_r = 0.0
        temp_g = 0.0
        temp_b = 0.0

        for x in range(temp_image.width):
            pixel = data[x,y]
            temp_r += pixel[0]
            temp_g += pixel[1]
            temp_b += pixel[2]

        temp_r /= temp_image.width
        temp_g /= temp_image.width
        temp_b /= temp_image.width

        row_average = (int(temp_r), int(temp_g), int(temp_b))

        for x in range(temp_image.width):
            temp_data[x,y] = row_average
    
    return temp_image

def averageRGB_column(test_image):
    data = test_image.load()
    temp_image = Image.new("RGB", (int(test_image.width), int(test_image.height)))
    temp_data = temp_image.load()

    for x in range(temp_image.width):
        temp_r = 0.0
        temp_g = 0.0
        temp_b = 0.0

        for y in range(temp_image.height):
            pixel = data[x,y]
            temp_r += pixel[0]
            temp_g += pixel[1]
            temp_b += pixel[2]

        temp_r /= temp_image.height
        temp_g /= temp_image.height
        temp_b /= temp_image.height

        row_average = (int(temp_r), int(temp_g), int(temp_b))

        for y in range(temp_image.height):
            temp_data[x,y] = row_average
    
    return temp_image

def average_axis(image1, image2):
    data1 = image1.load()
    data2 = image2.load()
    if (image1.height != image2.height or image1.width != image2.width):
        print("Error: image dimensions do not match")
        return image1
    temp_image = Image.new("RGB", (int(image1.width), int(image1.height)))
    temp_data = temp_image.load()

    for y in range(temp_image.height):
        for x in range(temp_image.width):
            pixel1 = data1[x,y]
            pixel2 = data2[x,y]

            r = int((pixel1[0] + pixel2[0])/2)
            g = int((pixel1[1] + pixel2[1])/2)
            b = int((pixel1[2] + pixel2[2])/2)

            temp_pixel = (r,g,b)
            temp_data[x,y] = temp_pixel
    
    return temp_image

def common_hues(test_image, return_size = 6, hue_bins = 36):
    data = test_image.load()

    bins = 1

    if hue_bins > 0:
        bins = hue_bins
    else:
        print(f"Error, not enough bins, defaulting to {bins}")

    hues = arr.array('i',[])
    for i in range(bins+1):
        hues.append(0)

    for y in range(test_image.height):
        for x in range(test_image.width):
            pixel = data[x,y]
            hsv_pixel = color_spaces.rgb_to_hsv(pixel)
            if hsv_pixel[1] != 0:
                hue = int(hsv_pixel[0] * (bins-1) + .5)
            else:
                hue = bins
            hues[hue] += 1

    temp_hues = []
    for i in range(return_size):
        temp_hues.append(0)
        for j in range(len(hues)):
            if temp_hues.__contains__(j) is False:
                    if hues[j] > hues[temp_hues[i]]:
                        temp_hues[i] = j
    top_hues = []
    for hue in temp_hues:
        corrected_hue = (hue * 1.0)/bins
        top_hues.append(corrected_hue)
    
    return top_hues

def common_saturations(test_image, return_size = 10, saturation_bins = 100):
    data = test_image.load()

    bins = 1

    if saturation_bins > 0:
        bins = saturation_bins
    else:
        print(f"Error, not enough bins, defaulting to {bins}")

    saturations = arr.array('i',[])
    for i in range(bins+1):
        saturations.append(0)

    for y in range(test_image.height):
        for x in range(test_image.width):
            pixel = data[x,y]
            hsv_pixel = color_spaces.rgb_to_hsv(pixel)
            if hsv_pixel[1] != 0:
                saturation = int(hsv_pixel[1] * (bins-1) + .5)
            else:
                saturation = bins
            saturations[saturation] += 1

    temp_saturations = []
    for i in range(return_size):
        temp_saturations.append(0)
        for j in range(len(saturations)):
            if temp_saturations.__contains__(j) is False:
                    if saturations[j] > saturations[temp_saturations[i]]:
                        temp_saturations[i] = j
    top_saturations = []
    for saturation in temp_saturations:
        corrected_saturation = (saturation * 1.0)/bins
        top_saturations.append(corrected_saturation)
    
    return top_saturations

def common_values(test_image, return_size = 10, value_bins = 100):
    data = test_image.load()

    bins = 1

    if value_bins > 0:
        bins = value_bins
    else:
        print(f"Error, not enough bins, defaulting to {bins}")

    values = arr.array('i',[])
    for i in range(bins+1):
        values.append(0)

    for y in range(test_image.height):
        for x in range(test_image.width):
            pixel = data[x,y]
            hsv_pixel = color_spaces.rgb_to_hsv(pixel)
            if hsv_pixel[1] != 0:
                value = int(hsv_pixel[1] * (bins-1) + .5)
            else:
                value = bins
            values[value] += 1

    temp_values = []
    for i in range(return_size):
        temp_values.append(0)
        for j in range(len(values)):
            if temp_values.__contains__(j) is False:
                    if values[j] > values[temp_values[i]]:
                        temp_values[i] = j
    top_values = []
    for value in temp_values:
        corrected_value = (value * 1.0)/bins
        top_values.append(corrected_value)
    
    return top_values

print(averageRGB(image))

new_image = HSV_channel_isolation(image, 0)
new_image.save("hue_only.png")

new_image = HSV_channel_isolation(image, 1)
new_image.save("sat_only.png")

new_image = HSV_channel_isolation(image, 2)
new_image.save("val_only.png")

# new_image = hue_distribution(image)
# new_image.save("hue_distribution.png")

# new_image = saturation_distribution(image)
# new_image.save("saturation_distribution.png")

# new_image = value_distribution(image)
# new_image.save("value_distribution.png")

new_image = HSV_channel_distribution(image, 0, 36)
new_image.save("hue_distribution.png")

new_image = HSV_channel_distribution(image, 1, 25)
new_image.save("saturation_distribution.png")

new_image = HSV_channel_distribution(image, 2, 25)
new_image.save("value_distribution.png")

# new_image = hue_distribution(image, 36, True)
# new_image.save("hue_graph.png")

# new_image = saturation_distribution(image, 30, True)
# new_image.save("saturation_graph.png")

# new_image = value_distribution(image, 30, True)
# new_image.save("value_graph.png")

new_image = HSV_channel_distribution(image, 0, 360, True)
new_image.save("hue_graph.png")

new_image = HSV_channel_distribution(image, 1, 255, True)
new_image.save("saturation_graph.png")

new_image = HSV_channel_distribution(image, 2, 255, True)
new_image.save("value_graph.png")

# new_image = averageRGB_image(image)
# new_image.save("averageRGB.png")

# avg_row_image = averageRGB_row(image)
# avg_row_image.save("averageRGB_row.png")

# avg_col_image = averageRGB_column(image)
# avg_col_image.save("averageRGB_column.png")

# new_image = average_axis(avg_row_image, avg_col_image)
# new_image.save("average_axis.png")

