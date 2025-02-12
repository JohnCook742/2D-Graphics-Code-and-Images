from PIL import Image
import math

image = Image.open("chess.jpg")
data = image.load()
new_image = Image.new("RGB", (image.width, image.height))
new_data = new_image.load()

rotation = .5
center = (image.width / 2, image.height / 2)

for y in range(image.height):
    for x in range(image.width):

        dx = x-center[0]
        dy = y-center[1]

        original_radius = math.sqrt(dx**2+dy**2)
        oringinal_angle = math.atan2(dy,dx)
        new_angle = oringinal_angle - rotation
        sample_x = math.cos(new_angle) * original_radius + center[0]
        sample_y = math.sin(new_angle) * original_radius + center[1]

        sample_x //= 1
        sample_y //= 1

        if 0 <= sample_x < image.width and 0 <= sample_y < image.height:
            new_data[x,y] = data[sample_x,sample_y]
        else:
            new_data[x,y] = (0,0,0)

new_image.save("rotation.png")