import zlib
from PIL import Image

image = Image.open("Christmas.jpg")
data = image.load()


header = f"P6\n{image.width}\n{image.height}\n255\n"

ppm_file = bytearray(header.encode())

for y in range(image.height):
  for x in range(image.width):
    pixel = data[x,y]
    ppm_file.append(pixel[0])
    ppm_file.append(pixel[1])
    ppm_file.append(pixel[2])

with open("p6.ppm", "wb") as text_file:
  text_file.write(ppm_file)


#Decode our P6 file

assert chr(ppm_file[0]) == "P"; 
assert chr(ppm_file[1]) == "6"; 
assert chr(ppm_file[2]).isspace(); 

index = 3
#Get width
width_string = ""
while  chr(ppm_file[index]).isdigit():
  width_string += chr(ppm_file[index])
  index += 1

width = int(width_string)
print(width)

# Move forward one since we found whitespace
index+=1

#Get height
height_string = ""
while chr(ppm_file[index]).isdigit():
  height_string += chr(ppm_file[index])
  index += 1
  
height = int(height_string)
print(height)

# Move forward one since we found whitespace
index+=1

#Get size
size_string = ""
while chr(ppm_file[index]).isdigit():
  size_string += chr(ppm_file[index])
  index += 1

size = int(size_string)
print(size)

# Move forward one since we found whitespace
index+=1

# Now read each byte
image_out = Image.new("RGB", (width, height))
data_out = image_out.load()

for y in range(height):
  for x in range(width):
    r = ppm_file[index]
    g = ppm_file[index+1]
    b = ppm_file[index+2]
    index += 3
    data_out[x,y] = (r,g,b)

image_out.save("p6.png")
