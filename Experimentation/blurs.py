from PIL import Image
import math

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

def box_blur_basic(start_image, radius):
    data = start_image.load()
    temp_image = Image.new("RGB", (start_image.width, start_image.height))
    temp_data = temp_image.load()

    for y in range(start_image.height):
        #print(y)
        for x in range(start_image.width):
            neighbors = []
            new_x = x-radius
            new_y = y-radius
            for move_y in range(1+2*radius):
                sample_y = new_y+move_y
                for move_x in range(1+2*radius):
                    sample_x = new_x+move_x
                    if 0<=(sample_x)<start_image.width and 0<=(sample_y)<start_image.height:
                        neighbors.append(data[(sample_x),(sample_y)])
                    else:
                        neighbors.append((0,0,0))
            temp_data[x,y] = neighbor_avg(neighbors)
            

    return temp_image

def box_blur_fast(start_image, radius):
    data = start_image.load()
    temp_image = Image.new("RGB", (start_image.width, start_image.height))
    temp_data = temp_image.load()


    for y in range(start_image.height):
        #print(y)
        for x in range(start_image.width):
            neighbors = []
            # capture axese
            for move_x in range(1+2*radius):
                sample_x = x+move_x-radius
                if 0<=(sample_x)<start_image.width and 0<=(y)<start_image.height:
                    neighbors.append(data[(sample_x),(y)])
                else:
                    neighbors.append((0,0,0))
                
            for move_y in range(1+2*radius):
                sample_y = y+move_y-radius
                if 0<=(x)<start_image.width and 0<=(sample_y)<start_image.height:
                    neighbors.append(data[(x),(sample_y)])
                else:
                    neighbors.append((0,0,0))
            
            # capture diagonals
            for move_diag in range(1+2*radius):
                sample_y = y+move_diag-radius
                sample_x = x+move_diag-radius
                if 0<=(sample_x)<start_image.width and 0<=(sample_y)<start_image.height:
                    neighbors.append(data[(sample_x),(sample_y)])
                else:
                    neighbors.append((0,0,0))
            
            for move_diag in range(1+2*radius):
                sample_y = y+move_diag-radius
                sample_x = x-move_diag+radius
                if 0<=(sample_x)<start_image.width and 0<=(sample_y)<start_image.height:
                    neighbors.append(data[(sample_x),(sample_y)])
                else:
                    neighbors.append((0,0,0))
            
            temp_data[x,y] = neighbor_avg(neighbors)
            

    return temp_image

def neighbor_avg(pixels):
    count = 0
    red_total = 0
    green_total = 0
    blue_total = 0
    red_avg = 0
    green_avg = 0
    blue_avg = 0
    for pixel in pixels:
        red_total += pixel[0]
        green_total += pixel[1]
        blue_total += pixel[2]
        count += 1
    
    if(count > 0):
        red_avg = red_total/count
        green_avg = green_total/count
        blue_avg = blue_total/count

    # red_avg //= 1
    # green_avg //= 1
    # blue_avg //= 1

    return (int(red_avg), int(green_avg), int(blue_avg))
    
print("starting basic")
new_image = box_blur_basic(image, 4)
new_image.save("box_blur.png")

print("starting fast")
new_image = box_blur_fast(image, 4)
new_image.save("box_blur_fast.png")