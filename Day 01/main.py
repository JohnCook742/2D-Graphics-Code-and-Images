from PIL import Image

image = Image.open("images.jpg")

data = image.load()
print(image.width)
print(image.height)

for y in range(image.height):
    for x in range(image.width):
        pixel = data[x,y]

        red = pixel[0]
        green = pixel[1]
        blue = pixel[2]
        clip = 200

        data[x,y] = (red%clip,green%clip,blue%clip)


image.save("aye-aye.jpg")