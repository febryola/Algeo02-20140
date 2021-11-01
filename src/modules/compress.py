import os
import argparse
import math
import numpy as np
from PIL import Image

# Usage : py compress.py input_file output_file
argparser = argparse.ArgumentParser()
argparser.add_argument("input")
argparser.add_argument("rate")
args = argparser.parse_args()

# Constants
input_filename = args.input
rate = float(args.rate)

# File extension
[filename, ext] = os.path.splitext(input_filename)

# Create a new Image
image = Image.open(input_filename)
image_array = np.array(image)

# Channels
has_alpha = False
r = image_array[:, :, 0]
g = image_array[:, :, 1]
b = image_array[:, :, 2]
if (image_array.shape[2] == 4):
    a = image_array[:, :, 3]
    has_alpha = True

# TODO: implements custom svd algorithm
ur, sr, vtr = np.linalg.svd(r)
ug, sg, vtg = np.linalg.svd(g)
ub, sb, vtb = np.linalg.svd(b)

# TODO : implements accurate calculation of singular
#        values taken based on compression rate
l = math.floor(len(sr) * rate * rate)
l = 1 if l == 0 else l

# Calculate new color matrices
ur_sub = ur[:, 0:l]
vtr_sub = vtr[0:l, :]
r_singulars = np.diag(sr)[0:l, 0:l]

ug_sub = ug[:, 0:l]
vtg_sub = vtg[0:l, :]
g_singulars = np.diag(sg)[0:l, 0:l]

ub_sub = ub[:, 0:l]
vtb_sub = vtb[0:l, :]
b_singulars = np.diag(sb)[0:l, 0:l]

red_channel = np.matmul(
    np.matmul(ur_sub, r_singulars), vtr_sub).astype("uint8")
green_channel = np.matmul(
    np.matmul(ug_sub, g_singulars), vtg_sub).astype("uint8")
blue_channel = np.matmul(
    np.matmul(ub_sub, b_singulars), vtb_sub).astype("uint8")

# Reform color channels to an image
image_red = Image.fromarray(red_channel, mode=None)
image_green = Image.fromarray(green_channel, mode=None)
image_blue = Image.fromarray(blue_channel, mode=None)

# Merge the images
if (has_alpha):
    image_alpha = Image.fromarray(a, mode=None)
    image = Image.merge(
        "RGBA", (image_red, image_green, image_blue, image_alpha))
else:
    image = Image.merge("RGB", (image_red, image_green, image_blue))

# Save the result image
image.save(f"{filename}-compressed{ext}", optimize=True)
