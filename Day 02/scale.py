from PIL import Image

image = Image.open("flying squirrel.jpg")

data = image.load()
print(image.width)
print(image.height)

pixel = data[0,0]
print(pixel)
print(pixel[0])
print(pixel[1])
print(pixel[2])

red = pixel[0]
green = pixel[1]
blue = pixel[2]

def scale(original_image, amount):
    temp_image = Image.new("RGB", (int(original_image.width * amount), int(original_image.height * amount)))
    temp_data = temp_image.load()
    original_data = original_image.load()

    for y in range(temp_image.height):
        for x in range(temp_image.width):

            current_x = x
            current_y = y

            pixel = original_data[int(current_x/amount), int(current_y/amount)]

            temp_data[x,y] = pixel
    
    return temp_image

flipped_image_horizontal = scale(image, 1.5)
flipped_image_horizontal.save("scale.png")
