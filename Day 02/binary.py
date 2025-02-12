from PIL import Image

image = Image.open("car.jpg")
data = image.load()

for y in range (image.height):
    for x in range (image.width):
        r,g,b = data[x,y]

        mask = 128 + 32

        r = r & mask
        g = g & mask
        b = b & mask

        data[x,y] = (r,g,b)

image.save("binary-car.png")