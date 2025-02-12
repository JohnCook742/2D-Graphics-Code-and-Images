from PIL import Image
import math

image = Image.open("car.jpg")
data = image.load()
new_image = Image.new("RGB", (image.width, image.height))
new_data = new_image.load()

center_x = image.width/2
center_y = image.height/2

for y in range(image.height):
    for x in range(image.width):
        new_x = x-center_x
        new_y = y-center_y

        if new_x < 0 or new_x >= image.width*2 or new_y < 0 or new_y >= image.width * 2:
            new_data[x, y] = (255,255,255)
        else:
            new_data[x,y] = data[math.floor(new_x), math.floor(new_y)]

new_image.save("edges.png")