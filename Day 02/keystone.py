from PIL import Image

image = Image.open("stoat.jpg")
data = image.load()

image_out = Image.new("RGB", (image.width, image.height))
data_out = image_out.load()

for y in range(image.height):
    for x in range(image.width):

        # Generic matrix operation
        a = 1
        b = 0
        c = 0
        d = .1
        e = 1
        f = 0

        x_1 = a*x+b*y + c
        y_1 = d*x + e*y + f


        # Override to do key stoning
        x_1 = (x-image.width/2)*((y)/image.height/2 + 1/2)+image.width/2
        y_1 = y

        # Note that I am pushing pixels, not pulling like we *should*
        if 0<=x_1<image.width and 0<=y_1<image.height:
            data_out[x_1,y_1] = data[x,y]
        else:
            data_out[x,y] = (0,0,0)


image_out.save("done.png")
