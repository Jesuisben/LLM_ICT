from PIL import Image

image_path = '../images/'
img = Image.open(image_path + "yangyang_skywalk.png")

max_size = 512
img.thumbnail((max_size, max_size))  # 비율 유지

img.save(image_path + "yangyang_skywalk_512.png")