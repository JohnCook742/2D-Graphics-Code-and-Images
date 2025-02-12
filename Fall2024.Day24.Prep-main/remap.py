import math

def color_distance(one, two):
    r_diff = one[0] - two[0]
    g_diff = one[1] - two[1]
    b_diff = one[2] - two[2]

    # return abs(r_diff) + abs(g_diff) + abs(b_diff)
    return math.sqrt((r_diff)**2+(g_diff)**2+(b_diff)**2)


def remap(image, data, palette, filename):

  print("Building cluster distance matrix")
  palette_distances = []
  for color1 in palette:
      row = []
      for color2 in palette:
          distance = color_distance(color1, color2)
          row.append(distance)
      palette_distances.append(row)

  
  for y in range(image.height):
    for x in range(image.width):
      pixel = data[x,y]
      min_distance = 44200
      min_index = 0
      for i,color in enumerate(palette):

        palette_distance = palette_distances[min_index][i]
        if palette_distance > min_distance * 2:
           continue

        distance = color_distance(color, pixel)
        if distance < min_distance:
          min_distance = distance
          min_index = i
      
      data[x,y] = palette[min_index]

      
  image.save(filename)

def remap_dither(image, data, palette, filename):

  print("Building cluster distance matrix")
  palette_distances = []
  for color1 in palette:
      row = []
      for color2 in palette:
          distance = color_distance(color1, color2)
          row.append(distance)
      palette_distances.append(row)
  
  error_matrix = []
  for x in range(image.width+1):
    row = []
    for y in range(image.height+1):
      row.append((0,0,0))
    error_matrix.append(row)

  
  for y in range(image.height):
    for x in range(image.width):
      if x == 292 and y == 107:
        pass
      
      pixel = data[x,y]
      error = error_matrix[x][y]
      pixel = (pixel[0] + error[0], 
               pixel[1] + error[1],
               pixel[2] + error[2])
      min_distance = 442000
      min_index = 0
      for i,color in enumerate(palette):

        palette_distance = palette_distances[min_index][i]
        if palette_distance > min_distance * 2:
           continue

        distance = color_distance(color, pixel)
        if distance < min_distance:
          min_distance = distance
          min_index = i
      
      data[x,y] = palette[min_index]

      error = (pixel[0] - data[x,y][0],
               pixel[1] - data[x,y][1],
               pixel[2] - data[x,y][2])
      
      error_matrix[x+1][y]   = (error_matrix[x+1][y][0] + error[0] * .25,
                                error_matrix[x+1][y][1] + error[1] * .25,
                                error_matrix[x+1][y][2] + error[2] * .25)
      
      error_matrix[x+1][y+1] = (error_matrix[x+1][y+1][0] + error[0] * .25,
                                error_matrix[x+1][y+1][1] + error[1] * .25,
                                error_matrix[x+1][y+1][2] + error[2] * .25)
      
      error_matrix[x]  [y+1] = (error_matrix[x][y+1][0] + error[0] * .25,
                                error_matrix[x][y+1][1] + error[1] * .25,
                                error_matrix[x][y+1][2] + error[2] * .25)
      
      error_matrix[x-1][y+1] = (error_matrix[x-1][y+1][0] + error[0] * .25,
                                error_matrix[x-1][y+1][1] + error[1] * .25,
                                error_matrix[x-1][y+1][2] + error[2] * .25)

      

      
  image.save(filename)
