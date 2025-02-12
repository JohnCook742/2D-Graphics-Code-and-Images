from PIL import Image

image = Image.open("car.jpg")

data = image.load()
print(image.width)
print(image.height)

for y in range(image.height):
    for x in range(image.width):
        pixel = data[x,y]

        red = pixel[0]
        green = pixel[1]
        blue = pixel[2]

        red_factor = .2
        green_factor = .7
        blue_factor = .1

        k = int(red * red_factor + 
                green * green_factor + 
                blue * blue_factor)
        
        v = max(red, green, blue)
        
        buffer = 0

        if(red > green + buffer and red > blue + buffer):
            data[x,y] = (red, green, blue)
        else:
             data[x,y] = (k,k,k)

        #data[x,y] = (v,v,v)

        #data[x,y] = (red,red,red)
        #data[x,y] = (green,green,green)
        #data[x,y] = (blue,blue,blue)


image.save("color iso.jpg")