from PIL import Image
# import array as arr
import image_stats
import color_spaces
import math
import random
from get_palette import get_palette
from print_palette import print_palette
from remap import remap
from remap import remap_dither

image = Image.open("Rick.jpg")
data = image.load()
new_image = Image.new("RGB", (image.width, image.height))
new_data = new_image.load()

def random_color():
    r = int(random.random() * 255)
    g = int(random.random() * 255)
    b = int(random.random() * 255)
    return (r,g,b)

def color_distance(one, two):
    return math.sqrt((one[0]-two[0])**2+(one[1]-two[1])**2+(one[2]-two[2])**2)

def kmc(test_image, clusters = 64, steps = 2, filename = "example_kmc.png"):
    test_data = test_image.load()
    entries = get_palette(test_image, test_data)

    count_cluster = clusters

    cluster_centers = []

    for i in range(count_cluster):
        cluster_centers.append(random_color())

    # print(cluster_centers)

    closest_pixels = [[] for i in range(count_cluster)]
    # print(closest_pixels)

    for _ in range(steps):
        print("Step")

        cluster_center_distances = []
        for i in range(count_cluster):
            row = []
            for j in range(count_cluster):
                distance = color_distance(cluster_centers[i], cluster_centers[j])
                row.append(distance)
            cluster_center_distances.append(row)

        for pixel in entries:
            min_distance = 100000
            min_index = 0
            for i in range(count_cluster):
                center = cluster_centers[i]
                center_to_center_distance = cluster_center_distances[min_index][i]
                if center_to_center_distance > 2 * min_distance:
                    continue

                distance = color_distance(pixel[0], center)
                if distance < min_distance:
                    min_distance = distance
                    min_index = i

                closest_pixels[min_index].append(pixel)

        # print(closest_pixels[0][:10])

        for i in range(count_cluster):
            sum_r = 0
            sum_g = 0
            sum_b = 0

            pixel_count = 0
            for j in range(len(closest_pixels[i])):
                sum_r += closest_pixels[i][j][0][0] * closest_pixels[i][j][1]
                sum_g += closest_pixels[i][j][0][1] * closest_pixels[i][j][1]
                sum_b += closest_pixels[i][j][0][2] * closest_pixels[i][j][1]
                pixel_count += closest_pixels[i][j][1]

            if pixel_count > 0:
                sum_r //= pixel_count
                sum_g //= pixel_count
                sum_b //= pixel_count

                cluster_centers[i] = (sum_r, sum_g, sum_b)
            else:
                cluster_centers[i] = (0,0,0)


    # raw_clusters = len(cluster_centers)
    # cluster_centers = list(set(cluster_centers))
    # optimized_clusters = len(cluster_centers)
    # print(cluster_centers)
    # print(f"Reduced clusters down to {optimized_clusters} from {raw_clusters}")

    print("Remapping image")
    remap(test_image, test_data, cluster_centers, filename)

def reduced_hsv(test_image, 
                hue_steps = 6, sat_steps = 4, val_steps = 4, 
                start_hue = 0.0, hue_list = None, sat_list = None, val_list = None, 
                filename = "example_reduced_HSV.png", 
                dither = False):
    test_data = test_image.load()

    hues = []
    if hue_list == None:
        hues.append(start_hue)
        if hue_steps < 1:
            print("Error, invalid hue step value: %d", hue_steps)
        for i in range(hue_steps):
            new_hue = start_hue + ((i+1)/hue_steps)
            new_hue %= 1
            new_hue += 1
            new_hue %= 1
            hues.append(new_hue)

    else:
        for hue in hue_list:
            new_hue = hue
            new_hue %= 1
            new_hue += 1
            new_hue %= 1
            hues.append(new_hue)

    sats = []
    if sat_list == None:
        sats.append(0.0)
        if sat_steps < 1:
            print("Error, invalid saturation step value: %d", sat_steps)
        for i in range(sat_steps):
            new_sat = ((i+1)/sat_steps)
            sats.append(new_sat)

    else:
        for sat in sat_list:
            new_sat = sat
            sats.append(new_sat)

    vals = []
    if val_list == None:
        vals.append(0.0)
        if val_steps < 1:
            print("Error, invalid value step value: %d", val_steps)
        for i in range(val_steps):
            new_val = ((i+1)/val_steps)
            vals.append(new_val)

    else:
        for val in val_list:
            new_val = val
            vals.append(new_val)
    
    colors = []

    for hue in hues:
        for sat in sats:
            for val in vals:
                hsv_color = (hue, sat, val)
                rgb_color = color_spaces.hsv_to_rgb(hsv_color)
                colors.append(rgb_color)
                # print(f"Added HSV{hsv_color} -> RGB{rgb_color} to palette")

    # raw_colors = len(colors)
    # colors = list(set(colors))
    # optimized_colors = len(colors)

    # print(f"Reduced color palette to {optimized_colors} colors from {raw_colors}")
    
    print("Remapping image")
    if (dither):
        remap_dither(test_image, test_data, colors, filename)
    else:
        remap(test_image, test_data, colors, filename)

# Inspired by description of harmonic palettes from: https://youtu.be/fv-wlo8yVhk?si=fXsCbHPLTJ_9VLzU&t=1680

def mono_palette_generator(start_hue = 0, sat_step = .1, val_step = .1):
    if sat_step <= 0 or val_step <= 0:
        print("Error, invalid saturation and/or value step")
        sat_step = 1
        val_step = 1
    
    palette = []
    total_steps = int(min(1/sat_step, 1/val_step))
    hue = start_hue
    for i in range(total_steps):
        new_sat = i*sat_step
        new_val = i*val_step
        new_hsv = (hue, new_sat, new_val)
        new_rgb = color_spaces.hsv_to_rgb(new_hsv)
        palette.append(new_rgb)

    return palette

def harmonic_palette_generator(start_hue = 0.0, end_hue = 1.0, sat = .5, val_step = .1):
    if val_step <= 0:
        print("Error, invalid value step")
        val_step = 1
    
    palette = []
    total_steps = int(1/val_step)
    hue_dif = end_hue-start_hue
    if hue_dif < 0:
        hue_dif += 1
    hue_step = hue_dif / total_steps
    for i in range(total_steps):
        new_hue = start_hue + i*hue_step
        new_hue %= 1
        new_val = i*val_step
        new_hsv = (new_hue, sat, new_val)
        new_rgb = color_spaces.hsv_to_rgb(new_hsv)
        palette.append(new_rgb)

    return palette
    

def simple_recolor(test_image, colors, filename="example_recolor.png", dither = False):
    test_data = test_image.load()

    # grayscale_values = []
    for x in range(test_image.width):
        # row = []
        for y in range(test_image.height):
            pixel = test_data[x,y]
            gray_pixel = int(pixel[0]*.2 + pixel[1]*.7 + pixel[2]*.1)
            test_data[x,y] = (gray_pixel, gray_pixel, gray_pixel)


    print("Remapping image")
    if (dither):
        remap_dither(test_image, test_data, colors, filename)
    else:
        remap(test_image, test_data, colors, filename)


mono_palette = mono_palette_generator(.1,1/50, 1/25)
simple_recolor(image, mono_palette, "mono_palette.png",False)

harmonic_palette = harmonic_palette_generator(.6,.1,.25,1/25)
simple_recolor(image, harmonic_palette, "harmonic_palette.png",False)

mono_palette = mono_palette_generator(.1,1/50, 1/25)
simple_recolor(image, mono_palette, "mono_palette_dither.png",True)

harmonic_palette = harmonic_palette_generator(.6,.1,.25,1/25)
simple_recolor(image, harmonic_palette, "harmonic_palette_dither.png",True)

clusters = 256
# new_image = kmc(image, clusters, 2, filename=f"kmc_{clusters}.png")

# custom_hues = image_stats.common_hues(image, 8, 12)
# custom_sats = image_stats.common_saturations(image, 7, 9)
# custom_vals = image_stats.common_values(image, 7, 9)

# custom_hues = [1/36, 4/36, 7/36, 24/36, 26/36, 28/36, 31/36, 35/36]
# custom_sats = [0, .1, .2, .4, .5, .6, .8, 1]
# custom_vals = [0, .1, .3, .5, .7, .8, .9, 1]

# reduced_hsv(image, 
#             hue_list= custom_hues, sat_list= custom_sats, val_list= custom_vals, 
#             filename="reduced_hsv.png",
#             dither=False)

# reduced_hsv(image, 
#             hue_list= custom_hues, sat_list= custom_sats, val_list= custom_vals, 
#             filename="reduced_hsv_dither.png",
#             dither=True)

# reduced_hsv(image, 
#             hue_steps= 12, sat_steps= 5, val_steps= 5, 
#             filename="reduced_hsv_steps.png",
#             dither=False)

# reduced_hsv(image, 
#             hue_steps= 12, sat_steps= 5, val_steps= 5, 
#             filename="reduced_hsv_steps_dither.png",
#             dither=True)