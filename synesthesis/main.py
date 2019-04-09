#!/usr/bin/env python3

import argparse
from synesthesis.utils import load_image_file
from synesthesis.math import create_power_spectrum
from synesthesis.sound import play_sound, save_sound

def main(image_file_loc, outfile):
    image = load_image_file(image_file_loc)

    power_spectrum = create_power_spectrum(image)

    if isinstance(outfile, NoOutfile()):
        play_sound(power_spectrum)
    else:
        save_sound(power_spectrum, outfile)

class NoOutfile():
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image_file_loc', help='location of image file')
    parser.add_argument('-o', '--outfile', help='file to save sound to', default=NoOutfile())
    args = parser.parse_args()

    main(image, outfile)
