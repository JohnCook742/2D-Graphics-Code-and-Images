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
        
        clip = 10
        top_cutoff = 2110

        data[x,y] = (255-red, 255-green, 255-blue)
        # if (y < top_cutoff):
        #     # data[x,y] = (gray_scale, gray_scale, gray_scale)
        #     data[x,y] = (red, green, blue)
            
        # else:
        #     if (green > clip and blue > clip and red < blue):
        #         data[x,y] = (255-red, 255-green, 255-blue)
        #     else:
        #         # data[x,y] = (gray_scale, gray_scale, gray_scale)
        #         data[x,y] = (red, green, blue)

image.save("lambo color invert.jpg")
        
