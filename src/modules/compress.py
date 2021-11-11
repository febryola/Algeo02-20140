import os
import argparse
# import time
import numpy as np
from PIL import Image, ImageFilter
from svdutils import toscale, clamp, tsvd

# Usage : py compress.py input_file compression_rate
argparser = argparse.ArgumentParser()
argparser.add_argument("input")
argparser.add_argument("rate")
args = argparser.parse_args()


# Constants
input_filename = args.input
# TODO: adjust chunk_size and rank based on args.rate
chunk_size = 32
rank = toscale(chunk_size, 0.05)

# File extension
[filename, ext] = os.path.splitext(input_filename)

# Create a new Image
image = Image.open(input_filename)
image_array = np.array(image)

# Channels
has_alpha = False
r = image_array[:, :, 0].astype("float64")
g = image_array[:, :, 1].astype("float64")
b = image_array[:, :, 2].astype("float64")
if (image_array.shape[2] == 4):
    a = image_array[:, :, 3]
    has_alpha = True

# Dimension
m, n = r.shape

# Used for debug purpose
# vchunksize = np.ceil(m / 64)
# hchunksize = np.ceil(n / 64)
# start = time.time()

# Split color matrices into separate chunks
# Compress each chunk with truncated SVD
# Then reconstruct the color matrices

for i in range(0, m, chunk_size):
    hb = i + chunk_size if i + chunk_size <= m else m
    for j in range(0, n, chunk_size):
        vb = j + chunk_size if j + chunk_size <= n else n
        chunk = r[i:hb, j:vb]
        cols = clamp(rank, 0, chunk.shape[1])
        # u, s, vt = rsvd(chunk, clamp(rank, 0, chunk.shape[1]))
        u, s, vt = tsvd(chunk, cols)
        sub = u.dot(np.diag(s)).dot(vt)
        r[i:hb, j:vb] = sub

for i in range(0, m, chunk_size):
    hb = i + chunk_size if i + chunk_size <= m else m
    for j in range(0, n, chunk_size):
        vb = j + chunk_size if j + chunk_size <= n else n
        chunk = g[i:hb, j:vb]
        cols = clamp(rank, 0, chunk.shape[1])
        # u, s, vt = rsvd(chunk, clamp(rank, 0, chunk.shape[1]))
        u, s, vt = tsvd(chunk, cols)
        sub = u.dot(np.diag(s)).dot(vt)
        g[i:hb, j:vb] = sub

for i in range(0, m, chunk_size):
    hb = i + chunk_size if i + chunk_size <= m else m
    for j in range(0, n, chunk_size):
        vb = j + chunk_size if j + chunk_size <= n else n
        chunk = b[i:hb, j:vb]
        cols = clamp(rank, 0, chunk.shape[1])
        # u, s, vt = rsvd(chunk, clamp(rank, 0, chunk.shape[1]))
        u, s, vt = tsvd(chunk, cols)
        sub = u.dot(np.diag(s)).dot(vt)
        b[i:hb, j:vb] = sub


# Correct floating point values to unit8 types
red_channel = r.astype("uint8")
green_channel = g.astype("uint8")
blue_channel = b.astype("uint8")

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

# Smooth filter to correct chunk borders
image = image.filter(ImageFilter.SMOOTH_MORE)

# Save the result image
image.save(f"{filename}-compressed{ext}", optimize=True)

# Used for debug purpose
# end = time.time()
# print(f"{end - start} seconds")
