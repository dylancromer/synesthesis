#!/usr/bin/env python3

import argparse
from synesthesis.utils import load_image_file
from synesthesis.sound import play_sound, save_sound

def main(image_file_loc, duration, outfile):
    image = load_image_file(image_file_loc)

    if isinstance(outfile, NoOutfile):
        play_sound(image, duration)
    else:
        save_sound(image, duration, outfile)

class NoOutfile():
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image_file_loc', help='location of image file')
    parser.add_argument('duration', help='duration in seconds of the sound', type=int)
    parser.add_argument('-o', '--outfile', help='file to save sound to', default=NoOutfile())
    args = parser.parse_args()

    main(args.image_file_loc, args.duration, args.outfile)
