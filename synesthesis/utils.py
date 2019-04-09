import imageio as imio
import numpy as np

def load_image_file(image_file_location):
    image_array = imio.imread(image_file_location)

    if len(image_array.shape) > 2:
        image_blackwhite = image_array.mean(axis=2)
    else:
        image_blackwhite = image_array

    return image_blackwhite

def _save_image(image, outfile):
    imio.imwrite(outfile, image)
    print("Saved image!")
