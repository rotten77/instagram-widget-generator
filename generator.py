# imports
import instaloader
from PIL import Image
import pathlib
import os
from crop_to_aspect import Image

# config
INSTAGRAM_LOGIN = ''
INSTAGRAM_PASSWORD = ''
THUMBNAIL_SIZE = 60
OFFSET = 10
GRID = 4
BACKGROUND_COLOR = (255, 255, 255, 255)

# config check
if INSTAGRAM_LOGIN=='':
    print('Fill in INSTAGRAM_LOGIN')
    exit()

# data folder
data_folder = str(pathlib.Path(__file__).parent.absolute())

# download images from Instagram
file_list = []

L = instaloader.Instaloader(save_metadata=False)

if INSTAGRAM_PASSWORD!='':
    L.login(INSTAGRAM_LOGIN, INSTAGRAM_PASSWORD)

posts = instaloader.Profile.from_username(L.context, INSTAGRAM_LOGIN).get_posts()

counter=0
for post in posts:
    if counter==(GRID*GRID):
        break
    else:
        L.download_post(post, INSTAGRAM_LOGIN)
        file_list.append(str(post.date).replace(" ", "_").replace(":", "-"))
    counter += 1

# generate background image
background_size = (GRID * THUMBNAIL_SIZE) + (GRID * OFFSET) + OFFSET
print(background_size)
background = Image.new('RGBA',(background_size, background_size), BACKGROUND_COLOR)

row = 1
column = 1

# paste thumbnails on layout
for file in file_list:
    file_path = data_folder + "\\" + INSTAGRAM_LOGIN +"\\" + file + "_UTC.jpg"
    if not os.path.exists(file_path):
        file_path = data_folder + "\\" + INSTAGRAM_LOGIN +"\\" + file + "_UTC_1.jpg"
    
    if not os.path.exists(file_path):
        print("{} not found".format(file))
        break

    image = Image.open(file_path)
    image = image.crop_to_aspect(THUMBNAIL_SIZE, THUMBNAIL_SIZE)
    image.thumbnail([THUMBNAIL_SIZE, THUMBNAIL_SIZE], resample=3, )
    img_w, img_h = image.size

    offset_y = (OFFSET * row) + (THUMBNAIL_SIZE * (row-1) if row > 1 else 0)
    offset_x = (OFFSET * column) + (THUMBNAIL_SIZE * (column-1) if column > 1 else 0)
    offset = (offset_x, offset_y)
    background.paste(image, offset)

    column += 1
    if column > GRID:
        row += 1
        column = 1

# save file
background.save(data_folder + "\\" + INSTAGRAM_LOGIN + ".png")