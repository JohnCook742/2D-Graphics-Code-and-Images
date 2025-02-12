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
        
        cyan_clip = 10
        orange_clip = 150
        top_cutoff = 2110
        # bottom_cutoff = 3200

        if (y < top_cutoff):
            data[x,y] = (gray_scale, gray_scale, gray_scale)
            # data[x,y] = (0, 0, 0)

        else:
            if ((red + cyan_clip < green + blue and red < green) or 
                (red + green > orange_clip and blue < green)):
                data[x,y] = (red, green, blue)
                # data[x,y] = (255, 0, 255)

            else:
                data[x,y] = (gray_scale, gray_scale, gray_scale)
        
            
        # data[x,y] = (gray_scale, gray_scale, gray_scale)

image.save("lambo color iso.jpg")