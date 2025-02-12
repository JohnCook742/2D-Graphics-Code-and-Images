from PIL import Image

image = Image.open("Christmas.jpg")

for i in range(100, -10, -10):
  image.save(f"Christmas_{i}.jpg", quality=i)

# image.save("Christmas.png")
# image.save("Christmas.gif")