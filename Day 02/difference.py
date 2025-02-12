from PIL import Image

image1 = Image.open("done.png")
data1 = image1.load()
image2 = Image.open("stoat.jpg")
data2 = image2.load()

image3 = Image.new("RGB", (image1.width, image1.height))
data3 = image3.load()

sum_error = 0
for y in range(image1.height):
    for x in range(image1.width):
        data3[x,y] = tuple(map(lambda a,b:abs(a-b), data1[x,y], data2[x,y]))
        sum_error += data3[x,y][0]+data3[x,y][1]+data3[x,y][2]

print(sum_error/(image1.width*image1.height))

image3.save("difference.png")