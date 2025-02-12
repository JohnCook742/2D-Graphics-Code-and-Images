from io import StringIO
from PIL import Image

image = Image.open("Christmas.jpg")
data = image.load()

string = StringIO()
string.write(f"P3\n{image.width} {image.height}\n255\n")

for y in range(image.height):
  for x in range(image.width):
    pixel = data[x,y]
    string.write(f"{pixel[0]} {pixel[1]} {pixel[2]} ")
  string.write("\n")

with open("p3_2.ppm", "w") as file:
  file.write(string.getvalue())
