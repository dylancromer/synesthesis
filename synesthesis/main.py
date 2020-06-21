#!/usr/bin/env python3

import argparse
from synesthesis.utils import load_image_file, load_sound_file
from synesthesis.sound import play_sound, save_sound
from synesthesis.image import save_image, save_animation


class NoOutfile():
    pass


def check_only_one_mode_set(*modes):
    if sum([int(m) for m in modes]) > 1:
        raise ValueError('cannot set more than one mode at once. Use only one of -i, -s, or -a')


def main():
    '''Convert image to sound file via inverse short-time Fourier transform, then play or save the resulting waveform.

    Arguments:
    image_file_loc -- the location of the image to be converted
    duration -- the desired length of the resulting waveform
    invert -- invert the image values (e.g. white pixels become black and vice-versa). Optional (default False)
    outfile -- location of file to output waveform, e.g. 'output.wav'. Optional.

    Be warned that the current version does not attempt to reduce the resolution of large images,
    if a very large image is used the program may become highly computationally expensive.
    '''
    #TODO add ability to reduce image resolution

    parser = argparse.ArgumentParser()
    parser.add_argument('input_file_loc', help='location of image file')
    parser.add_argument('-o', '--outfile', help='file to save sound to', default=NoOutfile())

    parser.add_argument('-i', '--image-mode', help='treat input as image, output sound', action='store_true')
    parser.add_argument('-t', '--duration', help='duration in seconds of the sound', type=int)
    parser.add_argument('-inv', '--invert-image', help='invert image brightness', action='store_true')

    parser.add_argument('-s', '--sound-mode', help='treat input as sound, output image', action='store_true')
    parser.add_argument('-a', '--animation-mode', help='treat input as sound, output animation', action='store_true')
    parser.add_argument('-sf', '--sound-format', help='format of the input sound file')
    parser.add_argument('-wl', '--window-length', help='length of the window function to be used for stft', default=280, type=int)
    parser.add_argument('-ol', '--overlap-length', help='length of the overlap between windows', default=None, type=int)
    parser.add_argument('-smooth', '--smoothing_factor', help='length of Gaussian window to use for convolutional smoothing', default=0, type=float)
    parser.add_argument('-az', '--azimuth', help='azimuth of viewing position in 3D plot', default=45, type=float)

    args = parser.parse_args()

    check_only_one_mode_set(args.sound_mode, args.image_mode, args.animation_mode)

    if args.image_mode:
        image = load_image_file(args.input_file_loc, args.invert_image)

        if isinstance(args.outfile, NoOutfile):
            play_sound(image, args.duration)
        else:
            save_sound(image, args.duration, args.outfile)

    elif args.sound_mode:
        sampling_rate, sound = load_sound_file(args.input_file_loc, args.sound_format)

        if not isinstance(args.outfile, NoOutfile):
            save_image(sampling_rate, sound, args.window_length, args.overlap_length, args.smoothing_factor, args.azimuth, args.outfile)
        else:
            raise ValueError('sound mode requires an output file to be specified')

    elif args.animation_mode:
        sampling_rate, sound = load_sound_file(args.input_file_loc, args.sound_format)

        if not isinstance(args.outfile, NoOutfile):
            save_animation(
                sampling_rate,
                sound,
                args.window_length,
                args.overlap_length,
                args.smoothing_factor,
                args.outfile,
            )
        else:
            raise ValueError('sound mode requires an output file to be specified')

    else:
        raise ValueError('Mode must be set with either the -i (--image-mode), the -s (--sound-mode), or the -a (--animation-mode) flag')


if __name__ == '__main__':
    main()
