from PIL import Image
from io import StringIO

image = Image.open("car.jpg")
data = image.load()
# Making the ppm file
string = StringIO()

string.write(f"P3\n{image.width} {image.height}\n255\n")

for y in range(image.height):
    for x in range(image.width):
        pixel = data[x,y]
        string.write(f"{pixel[0]} {pixel[1]} {pixel[2]} ")
    string.write("\n")

with open("p3.ppm", "w") as file:
    file.write(string.getvalue())

# reading the ppm file
ppm_string = string.getvalue()
parts = ppm_string.split()

assert parts[0] == "P3"
width = int(parts[1])
height = int(parts[2])
assert parts[3] == "255"

new_image = Image.new("RGB", (width, height))
new_data = new_image.load()

for i in range(int((len(parts) - 4)/3)):
    index = 3*i+4
    r = int(parts[index])
    g = int(parts[index+1])
    b = int(parts[index+2])
    new_y = int(i / new_image.width)
    new_x = i % new_image.width
    new_data[new_x,new_y] = (r,g,b)

new_image.save("car.png")