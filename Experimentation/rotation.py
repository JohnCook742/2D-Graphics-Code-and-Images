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

def rotation(start_image, rotation):
    data = start_image.load()
    temp_image = Image.new("RGB", (start_image.width, start_image.height))
    temp_data = temp_image.load()
    
    center = (temp_image.width/2, temp_image.height/2)

    cosine_theta = math.cos(-rotation)
    sine_theta = math.sin(-rotation)

    for y in range(start_image.height):
        #print(y)
        for x in range(start_image.width):
            new_x = cosine_theta * x - sine_theta * y - cosine_theta * center[0] + sine_theta*center[1] + center[0]
            new_y = sine_theta * x + cosine_theta * y - sine_theta * center[0] - cosine_theta * center[1] + center[1]

            new_x //= 1
            new_y //= 1

            if 0<=new_x<start_image.width and 0<=new_y<start_image.height:
                temp_data[x,y] = data[new_x,new_y]
            else:
                temp_data[x,y] = (0,0,0)

    return temp_image

def rotation_fit(start_image, rotation):
    cosine_theta = math.cos(-rotation)
    sine_theta = math.sin(-rotation)

    data = start_image.load()
    temp_image = Image.new("RGB", 
                           (int(start_image.width * math.fabs(cosine_theta) + 
                                start_image.height * math.fabs(sine_theta)), 
                            int(start_image.height * math.fabs(cosine_theta) + 
                                start_image.width * math.fabs(sine_theta))))
    temp_data = temp_image.load()
    
    temp_center = (temp_image.width/2, temp_image.height/2)
    start_center = (start_image.width/2, start_image.height/2)

    for y in range(temp_image.height):
        #print(y)
        for x in range(temp_image.width):
            new_x = (cosine_theta * x - sine_theta * y) - cosine_theta * temp_center[0] + sine_theta * temp_center[1] + start_center[0]
            new_y = (sine_theta * x + cosine_theta * y) - sine_theta * temp_center[0] - cosine_theta * temp_center[1] + start_center[1]

            new_x //= 1
            new_y //= 1

            if 0<=new_x<start_image.width and 0<=new_y<start_image.height:
                temp_data[x,y] = data[new_x,new_y]
            else:
                temp_data[x,y] = (0,0,0)

    return temp_image

def rotation_fill(start_image, rotation):
    cosine_theta = math.cos(-rotation)
    sine_theta = math.sin(-rotation)

    data = start_image.load()
    temp_image = Image.new("RGB", 
                           (int(abs(start_image.width * math.fabs(cosine_theta) - 
                                start_image.height * math.fabs(sine_theta))), 
                            int(abs(start_image.height * math.fabs(cosine_theta) - 
                                start_image.width * math.fabs(sine_theta)))))
    temp_data = temp_image.load()
    
    temp_center = (temp_image.width/2, temp_image.height/2)
    start_center = (start_image.width/2, start_image.height/2)

    for y in range(temp_image.height):
        #print(y)
        for x in range(temp_image.width):
            new_x = (cosine_theta * x - sine_theta * y) - cosine_theta * temp_center[0] + sine_theta * temp_center[1] + start_center[0]
            new_y = (sine_theta * x + cosine_theta * y) - sine_theta * temp_center[0] - cosine_theta * temp_center[1] + start_center[1]

            new_x //= 1
            new_y //= 1

            if 0<=new_x<start_image.width and 0<=new_y<start_image.height:
                temp_data[x,y] = data[new_x,new_y]
            else:
                temp_data[x,y] = (0,0,0)

    return temp_image

new_image = rotation(image, 1)
new_image.save("rotation.png")

new_image = rotation_fit(image, 1)
new_image.save("rotation_fit.png")

new_image = rotation_fill(image, 1)
new_image.save("rotation_fill.png")
