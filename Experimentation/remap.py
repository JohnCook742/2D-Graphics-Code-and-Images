from PIL import Image
import math

def color_distance(one, two):
  diff_r = one[0] - two[0]
  diff_g = one[1] - two[1]
  diff_b = one[2] - two[2]

  return math.sqrt(diff_r**2+diff_g**2+diff_b**2)

def remap(image, data, palette, filename):
  temp_image = Image.new("RGB", (image.width, image.height))
  temp_data = temp_image.load()

  raw_palette_size = len(palette)
  palette = list(set(palette))
  new_palette_size = len(palette)
  print(f"Palette size reduced from {raw_palette_size} to {new_palette_size}")

  prev_color = palette[0]
  prev_pixel = None
  for y in range(temp_image.height):
    # print(y)
    for x in range(temp_image.width):
      pixel = data[x,y]

      # Neighbor Optimization Check
      if pixel == prev_pixel:
        temp_data[x,y] = prev_color
        # print(".", end = " ")


      min_distance = 10000
      min_index = 0
      for i,color in enumerate(palette):
        center_to_center_distance = color_distance(color,palette[min_index])
        if center_to_center_distance > 2 * min_distance:
          continue

        distance = color_distance(color, pixel)
        if distance < min_distance:
          min_distance = distance
          min_index = i

          prev_color = color
          prev_pixel = pixel
      
      temp_data[x,y] = palette[min_index]

      
  temp_image.save(filename)

def remap_dither(image, data, palette, filename):
  temp_image = Image.new("RGB", (image.width, image.height))
  temp_data = temp_image.load()

  raw_palette_size = len(palette)
  palette = list(set(palette))
  new_palette_size = len(palette)
  print(f"Palette size reduced from {raw_palette_size} to {new_palette_size}")

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
      
      temp_data[x,y] = palette[min_index]

      error = (pixel[0] - temp_data[x,y][0],
               pixel[1] - temp_data[x,y][1],
               pixel[2] - temp_data[x,y][2])
      
      error_scale = .2

      error_matrix[x+1][y]   = (error_matrix[x+1][y]  [0] + error[0] * error_scale,
                                error_matrix[x+1][y]  [1] + error[1] * error_scale,
                                error_matrix[x+1][y]  [2] + error[2] * error_scale)
      
      error_matrix[x+1][y+1] = (error_matrix[x+1][y+1][0] + error[0] * error_scale,
                                error_matrix[x+1][y+1][1] + error[1] * error_scale,
                                error_matrix[x+1][y+1][2] + error[2] * error_scale)
      
      error_matrix[x]  [y+1] = (error_matrix[x]  [y+1][0] + error[0] * error_scale,
                                error_matrix[x]  [y+1][1] + error[1] * error_scale,
                                error_matrix[x]  [y+1][2] + error[2] * error_scale)
      
      error_matrix[x-1][y+1] = (error_matrix[x-1][y+1][0] + error[0] * error_scale,
                                error_matrix[x-1][y+1][1] + error[1] * error_scale,
                                error_matrix[x-1][y+1][2] + error[2] * error_scale)

      

      
  temp_image.save(filename)