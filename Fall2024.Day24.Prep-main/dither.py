from PIL import Image

image = Image.open("fish2.png")
data = image.load()

error_matrix = []

for x in range(image.width+1):
    row = []
    for y in range(image.height+1):
        row.append(0)
    error_matrix.append(row)



for y in range(image.height):
    error = 0
    for x in range(image.width):
        pixel = data[x,y]
        k = (pixel[0] + pixel[1] + pixel[2])//3

        k += error_matrix[x][y]

        out = 0
        if k >= 128:
            out = 255

        error = k-out
        quarter_error = error/4
        error_matrix[x+1][y]    += quarter_error
        error_matrix[x-1][y+1]  += quarter_error
        error_matrix[x][y+1]    += quarter_error
        error_matrix[x+1][y+1]  += quarter_error
        
        k = out
        data[x,y] = (k,k,k)

image.save("fish2_fs.png")