from PIL import Image

image = Image.open("car.jpg")

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

packed_int = 0

packed_int += red << 16
packed_int += green << 8
packed_int += blue << 0

print(packed_int)

packed_temp = packed_int
unpacked_red = 0
unpacked_green = 0
unpacked_blue = 0

# unpacked_blue = packed_temp % 256
# packed_temp -= unpacked_blue
# packed_temp /= 256
# unpacked_green = packed_temp % 256
# packed_temp -= unpacked_green
# packed_temp /= 256
# unpacked_red = packed_temp % 256

unpacked_blue = packed_temp & 255
packed_temp >>= 8
unpacked_green = packed_temp & 255
packed_temp >>= 8
unpacked_red = packed_temp & 255

print(unpacked_red)
print(unpacked_green)
print(unpacked_blue)

def flip_horizontal(original_image):
    temp_image = Image.new("RGB", (original_image.width, original_image.height))
    temp_data = temp_image.load()
    original_data = original_image.load()

    for y in range(image.height):
        for x in range(image.width):
            pixel = original_data[x,y]
            temp_data[(image.width-1) - x,y] = pixel
    
    return temp_image

def flip_vertical(original_image):
    temp_image = Image.new("RGB", (original_image.width, original_image.height))
    temp_data = temp_image.load()
    original_data = original_image.load()

    for y in range(image.height):
        for x in range(image.width):
            pixel = original_data[x,y]
            temp_data[x,(image.height-1) - y] = pixel
    
    return temp_image

flipped_image_horizontal = flip_horizontal(image)
flipped_image_horizontal.save("flipped_horizontal.png")

flipped_image_vertical = flip_vertical(image)
flipped_image_vertical.save("flipped_vertical.png")
