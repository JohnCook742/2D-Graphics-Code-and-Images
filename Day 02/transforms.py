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

def rotate_90(original_image):
    temp_image = Image.new("RGB", (original_image.height, original_image.width))
    temp_data = temp_image.load()
    original_data = original_image.load()

    for y in range(original_image.height):
        for x in range(original_image.width):
            pixel = original_data[x,y]
            temp_data[-y+original_image.height-1, x] = pixel
    
    return temp_image


def translate(original_image, dx, dy):
    temp_image = Image.new("RGB", (original_image.width + dx, original_image.height + dy))
    temp_data = temp_image.load()
    original_data = original_image.load()

    for y in range(original_image.height):
        for x in range(original_image.width):
            pixel = original_data[x,y]
            temp_data[x+dx, y+dy] = pixel
    
    return temp_image

def transform(original_image, 
              a,b,c,
              d,e,f):
    temp_image = Image.new("RGB", (original_image.width, original_image.height))
    temp_data = temp_image.load()
    original_data = original_image.load()

    for y in range(original_image.height):
        for x in range(original_image.width):
            pixel = original_data[x,y]
            new_x = x * a + y * b + 1 * c
            new_y = x * d + y * e + 1 * f
            temp_data[new_x, new_y] = pixel
    
    return temp_image

flipped_image_horizontal = rotate_90(image)
flipped_image_horizontal.save("rotate_90.png")

flipped_image_horizontal = translate(image, 20, 72)
flipped_image_horizontal.save("translate.png")

flipped_image_horizontal = transform(image, -1, 0, (image.width-1), 0, 1, 0)
flipped_image_horizontal.save("transform.png")
