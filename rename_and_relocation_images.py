from natsort import natsorted
from PIL import Image

import glob
import os
import shutil
import pprint

DRAFT_IMAGES_PATH = "./Output/draft-main/images/"
PROD_IMAGES_PATH = "./Output/prod/images/"

images = glob.glob(DRAFT_IMAGES_PATH + '*.png')
images = natsorted(images)

for image in images:
    shutil.move(image, PROD_IMAGES_PATH + image.split('/')[-1].split('-')[0] + '.png')
    # dist_image = Image.open(image)
    # dist_image.save(PROD_IMAGES_PATH + image.split('/')[-1].split('-')[0] + '.png')