from PIL import Image
from io import StringIO

image = Image.open("Christmas.jpg")
data = image.load()

ppm_file = StringIO()
ppm_file.write(f"P3\n{image.width} {image.height}\n255\n")

for y in range(image.height):
  for x in range(image.width):
    pixel = data[x,y]
    ppm_file.write(f"{pixel[0]} {pixel[1]} {pixel[2]} ")
  ppm_file.write("\n")

with open("P3.ppm", "w") as text_file:
  text_file.write(ppm_file.getvalue())

ppm_values = ppm_file.getvalue().split()

index = 0

front = ppm_values[index]
index += 1
assert front == "P3"

width = int(ppm_values[index])
index += 1
height = int(ppm_values[index])
index += 1
_ = ppm_values[index]
index += 1

print(width)
print(height)

image_out = Image.new("RGB", (width, height))
data_out = image_out.load()

for y in range(height):
  for x in range(width):
    r = int(ppm_values[index])
    g = int(ppm_values[index+1])
    b = int(ppm_values[index+2])
    index += 3
    
    data_out[x,y] = (r, g, b)

image_out.save("P3.png")
