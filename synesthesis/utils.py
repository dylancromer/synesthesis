import imageio as imio
import numpy as np




def load_image_file(image_file_location, invert):
    """Loads image from file location, can optionally invert image brightness levels.

    Arguments:
    image_file_location -- location of image file to load (string)
    invert -- if true perform invesion of image brightness (bool)

    returns greyscale version of image (optionally inverted, numpy.ndarray)
    """

    image_array = imio.imread(image_file_location)

    if len(image_array.shape) > 2:
        image_blackwhite = image_array.mean(axis=2)
    else:
        image_blackwhite = image_array

    if invert:
        image_blackwhite = 255 - image_blackwhite

    return image_blackwhite


def _save_image(image, outfile):
    """Saves image to desired outfile. Thin wrapper around imageio imwrite."""
    imio.imwrite(outfile, image)
    print("Saved image!")
