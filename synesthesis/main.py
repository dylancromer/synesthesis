#!/usr/bin/env python3

import argparse
from synesthesis.utils import load_image_file
from synesthesis.sound import play_sound, save_sound

class NoOutfile():
    pass

def main():
    """Convert image to sound file via inverse short-time Fourier transform, then play or save the resulting waveform.

    Arguments:
    image_file_loc -- the location of the image to be converted
    duration -- the desired length of the resulting waveform
    invert -- invert the image values (e.g. white pixels become black and vice-versa). Optional (default False)
    outfile -- location of file to output waveform, e.g. 'output.wav'. Optional.

    Be warned that the current version does not attempt to reduce the resolution of large images,
    if a very large image is used the program may become highly computationally expensive.
    """
    #TODO add ability to reduce image resolution

    parser = argparse.ArgumentParser()
    parser.add_argument('image_file_loc', help='location of image file')
    parser.add_argument('duration', help='duration in seconds of the sound', type=int)
    parser.add_argument('-i', '--invert', help='invert image brightness', action='store_true')
    parser.add_argument('-o', '--outfile', help='file to save sound to', default=NoOutfile())
    args = parser.parse_args()

    image = load_image_file(args.image_file_loc, args.invert)

    if isinstance(args.outfile, NoOutfile):
        play_sound(image, args.duration)
    else:
        save_sound(image, args.duration, args.outfile)

if __name__ == '__main__':
    main()
