def get_palette(image, data):
  palette_colors = dict()

  for y in range(image.height):
    for x in range(image.width):
      pixel = data[x,y]
      if pixel in palette_colors.keys():
        palette_colors[pixel] = palette_colors[pixel]+1
      else:
        palette_colors[pixel] = 1


  palette = sorted(palette_colors.items(), key=lambda pair:pair[1], reverse=True)
  return palette