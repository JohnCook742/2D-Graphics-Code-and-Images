from PIL import Image

image = Image.open("lambo.jpg")

data = image.load()
width = image.width
height = image.height
print(image.width)
print(image.height)

for y in range(height):
    for x in range(width):
        pixel = data[x,y]

        red = pixel[0]
        green = pixel[1]
        blue = pixel[2]

        red_factor = .2
        green_factor = .7
        blue_factor = .1

        gray_scale = int(red * red_factor + 
                         green * green_factor + 
                         blue * blue_factor)
            
        data[x,y] = (gray_scale, gray_scale, gray_scale)

image.save("lambo bw.jpg")