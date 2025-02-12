from PIL import Image

image_original = Image.open("car.jpg")
image_shift = Image.open("hsv_shift.png")
image_mult = Image.open("hsv_mult.png")
image_pow = Image.open("hsv_pow.png")
image_root = Image.open("hsv_root.png")
image_crush = Image.open("hue_crush.png")
image_bulge = Image.open("bulge.png")
image_bulge_smooth = Image.open("bulge_smooth.png")

def difference(image1, image2):
    data1 = image1.load()
    data2 = image2.load()

    image3 = Image.new("RGB", (image1.width, image1.height))
    data3 = image3.load()
    sum_error = 0
    for y in range(image1.height):
        for x in range(image1.width):
            data3[x,y] = tuple(map(lambda a,b:abs(a-b), data1[x,y], data2[x,y]))
            sum_error += data3[x,y][0]+data3[x,y][1]+data3[x,y][2]

    print(sum_error/(image1.width*image1.height))

    return image3

# dif_image = difference(image_shift, image_original)
# dif_image.save("difference_shift.png")

# dif_image = difference(image_mult, image_original)
# dif_image.save("difference_mult.png")

dif_image = difference(image_pow, image_original)
dif_image.save("difference_pow.png")

dif_image = difference(image_root, image_original)
dif_image.save("difference_root.png")

# dif_image = difference(image_crush, image_original)
# dif_image.save("difference_crush.png")

# dif_image = difference(image_bulge, image_original)
# dif_image.save("difference_bulge.png")

# dif_image = difference(image_bulge_smooth, image_original)
# dif_image.save("difference_bulge_smooth.png")

# dif_image = difference(image_bulge_smooth, image_bulge)
# dif_image.save("difference_bulges.png")